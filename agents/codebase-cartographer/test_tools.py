#!/usr/bin/env python3
"""Self-check for the hand-rolled tool functions. Run: python3 test_tools.py

These are the only things the model can do inside a cloned repository, so a path-traversal
bug here is the whole security model failing, not a minor defect.
"""

import sys
import tempfile
from pathlib import Path

from tools import make_tools


def build(repo: Path) -> tuple:
    docs_written: list[str] = []
    glob_files, read_file, grep, write_doc = make_tools(repo, docs_written)
    return glob_files, read_file, grep, write_doc, docs_written


def test_glob_and_read_see_files_inside_the_repo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "src").mkdir()
        (repo / "src" / "main.py").write_text("print('hi')\n")

        glob_files, read_file, _, _, _ = build(repo)
        assert glob_files("**/*.py") == ["src/main.py"]
        assert read_file("src/main.py") == "print('hi')\n"


def test_read_file_refuses_traversal_out_of_the_repo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        repo = root / "repo"
        repo.mkdir()
        (root / "secret.txt").write_text("nope\n")

        _, read_file, _, _, _ = build(repo)
        assert read_file("../secret.txt").startswith("error:")
        assert read_file("/etc/passwd").startswith("error:")


def test_read_file_refuses_a_symlink_escaping_the_repo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        repo = root / "repo"
        repo.mkdir()
        (root / "secret.txt").write_text("nope\n")
        (repo / "escape.txt").symlink_to(root / "secret.txt")

        _, read_file, _, _, _ = build(repo)
        assert read_file("escape.txt").startswith("error:")


def test_grep_finds_matches_with_line_numbers() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "a.py").write_text("x = 1\ndef foo():\n    return x\n")

        _, _, grep, _, _ = build(repo)
        hits = grep(r"def \w+")
        assert len(hits) == 1, hits
        assert hits[0].startswith("a.py:2:"), hits


def test_grep_reports_a_bad_pattern_instead_of_raising() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        _, _, grep, _, _ = build(Path(tmp))
        result = grep("(unclosed")
        assert result and result[0].startswith("error:"), result


def test_write_doc_accepts_only_the_docs_directory() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _, _, _, write_doc, docs_written = build(repo)

        refused = write_doc("README.md", "hello")
        assert refused.startswith("error:"), refused
        assert not (repo / "README.md").exists()

        ok = write_doc("docs/codebase-map/architecture.md", "# Architecture\n")
        assert "wrote" in ok, ok
        assert (repo / "docs" / "codebase-map" / "architecture.md").read_text() == "# Architecture\n"
        assert docs_written == ["docs/codebase-map/architecture.md"]


def test_write_doc_refuses_traversal_disguised_as_the_docs_directory() -> None:
    """docs/codebase-map/../../etc/passwd starts with the right prefix string-wise."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        repo = root / "repo"
        repo.mkdir()
        _, _, _, write_doc, _ = build(repo)

        result = write_doc("docs/codebase-map/../../../outside.md", "pwned")
        assert result.startswith("error:"), result
        assert not (root / "outside.md").exists()


def test_two_runs_do_not_share_docs_written() -> None:
    """Each run closes over its own list; nothing leaks between concurrent runs."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        _, _, _, write_doc_a, docs_a = build(repo)
        _, _, _, write_doc_b, docs_b = build(repo)
        write_doc_a("docs/codebase-map/a.md", "a")
        assert docs_a == ["docs/codebase-map/a.md"]
        assert docs_b == []


def main() -> None:
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
    print("all checks passed")


if __name__ == "__main__":
    main()
    sys.exit(0)
