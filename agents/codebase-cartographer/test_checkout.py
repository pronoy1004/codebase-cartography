#!/usr/bin/env python3
"""Self-check for the input validation. Run: python3 test_checkout.py

This is the file that decides what the service will fetch and read, so it is the file
worth testing. Everything past it hands a directory to a model with Bash.
"""

import os
import sys
import tempfile
from pathlib import Path

import checkout
from checkout import CheckoutError


def refuses(fn, *args) -> str:
    try:
        fn(*args)
    except CheckoutError as exc:
        return str(exc)
    raise AssertionError(f"{fn.__name__}{args} should have been refused")


def test_only_http_schemes_are_cloned() -> None:
    for url in (
        "file:///etc/passwd",
        "ssh://git@github.com/o/r",
        "git://github.com/o/r",
        "ext::sh -c 'touch /tmp/pwned'",
        "/etc/passwd",
        "",
    ):
        refuses(checkout.clone, url)


def test_refs_that_could_be_read_as_options_are_refused() -> None:
    for ref in ("--upload-pack=touch /tmp/pwned", "-x", "a b", "a;b", "a$(id)", "a" * 300, ""):
        refuses(checkout.clone, "https://example.com/o/r", ref)


def test_local_paths_refused_when_no_allowlist_is_configured() -> None:
    os.environ.pop(checkout.ALLOWED_ROOTS_ENV, None)
    msg = refuses(checkout.resolve_local, "/tmp")
    assert checkout.ALLOWED_ROOTS_ENV in msg, msg


def test_local_paths_inside_the_allowlist_resolve() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        (root / "project").mkdir()
        os.environ[checkout.ALLOWED_ROOTS_ENV] = str(root)
        assert checkout.resolve_local(str(root / "project")) == root / "project"
        assert checkout.resolve_local(str(root)) == root


def test_traversal_out_of_the_allowlist_is_refused() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        (root / "project").mkdir()
        os.environ[checkout.ALLOWED_ROOTS_ENV] = str(root / "project")
        refuses(checkout.resolve_local, str(root / "project" / ".." / ".."))
        refuses(checkout.resolve_local, "/etc")


def test_symlink_escaping_the_allowlist_is_refused() -> None:
    """The reason resolve_local resolves before comparing, not after."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        inside = root / "allowed"
        outside = root / "secret"
        inside.mkdir()
        outside.mkdir()
        (inside / "escape").symlink_to(outside, target_is_directory=True)
        os.environ[checkout.ALLOWED_ROOTS_ENV] = str(inside)
        refuses(checkout.resolve_local, str(inside / "escape"))


def test_sibling_prefix_is_not_treated_as_inside() -> None:
    """/srv/repos-private must not pass an allowlist of /srv/repos."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        (root / "repos").mkdir()
        (root / "repos-private").mkdir()
        os.environ[checkout.ALLOWED_ROOTS_ENV] = str(root / "repos")
        refuses(checkout.resolve_local, str(root / "repos-private"))


def main() -> None:
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
    print("all checks passed")


if __name__ == "__main__":
    main()
    sys.exit(0)
