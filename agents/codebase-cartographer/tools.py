"""Read-only filesystem tools for the mapping agent, plus a doc-writer.

Claude Code's own Read/Grep/Glob/Bash/Write tools do not exist outside Claude Code, so this
agent gets plain Python functions instead: no shell, no subprocess, nothing beyond glob,
regex search, and file read/write, each confined to the repository checkout. There is
deliberately no Bash-equivalent — the mapping skills read and search files, they do not
need to execute anything, and dropping shell access entirely is a smaller attack surface
than trying to sandbox one.

google-genai turns a plain function's type hints and docstring into a tool schema and calls
it automatically, so these are ordinary functions, not tool declarations.
"""

from __future__ import annotations

import re
from pathlib import Path

_MAX_READ_BYTES = 200_000
_MAX_GREP_HITS = 200
_MAX_GLOB_RESULTS = 500
_DOCS_PREFIX = ("docs", "codebase-map")


def _resolve_within(repo: Path, rel: str) -> Path:
    """Resolve `rel` against `repo`, refusing anything that resolves outside it.

    `resolve()` collapses `..` and follows symlinks before the containment check runs,
    so a symlink planted inside the checkout that points outside it is caught too.
    """
    target = (repo / rel).resolve()
    if target != repo and repo not in target.parents:
        raise ValueError(f"path escapes the repository: {rel}")
    return target


def make_tools(repo: Path, docs_written: list[str]) -> list:
    """Build this run's tool functions, closed over its own checkout and doc list."""
    # Resolved once, so every containment check below compares like with like. Without
    # this, a repo path that is itself a symlink (on macOS, /tmp -> /private/tmp is the
    # common case) fails every check: _resolve_within resolves the target but not repo,
    # so a perfectly legitimate path never compares equal to anything in target.parents.
    repo = repo.resolve()

    def glob_files(pattern: str) -> list[str]:
        """List files in the repository matching a glob pattern.

        Args:
            pattern: A glob pattern relative to the repository root, for example
                "**/*.py" or "src/**/*.ts".
        """
        try:
            matches = sorted(
                str(p.relative_to(repo)) for p in repo.glob(pattern) if p.is_file()
            )
        except (ValueError, OSError) as exc:
            return [f"error: {exc}"]
        return matches[:_MAX_GLOB_RESULTS]

    def read_file(path: str) -> str:
        """Read a text file from the repository.

        Args:
            path: File path relative to the repository root.
        """
        try:
            target = _resolve_within(repo, path)
        except ValueError as exc:
            return f"error: {exc}"
        if not target.is_file():
            return f"error: not a file: {path}"
        data = target.read_bytes()[:_MAX_READ_BYTES]
        return data.decode("utf-8", errors="replace")

    def grep(pattern: str, glob: str = "**/*") -> list[str]:
        """Search file contents for a regular expression.

        Args:
            pattern: A Python regular expression to search for, applied line by line.
            glob: Limit the search to files matching this glob pattern.
        """
        try:
            rx = re.compile(pattern)
        except re.error as exc:
            return [f"error: bad pattern: {exc}"]
        hits: list[str] = []
        for p in repo.glob(glob):
            if len(hits) >= _MAX_GREP_HITS:
                break
            if not p.is_file():
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                if rx.search(line):
                    snippet = line.strip()[:200]
                    hits.append(f"{p.relative_to(repo)}:{lineno}: {snippet}")
                    if len(hits) >= _MAX_GREP_HITS:
                        break
        return hits

    def write_doc(path: str, content: str) -> str:
        """Write a markdown doc. Only paths under docs/codebase-map/ are accepted.

        Args:
            path: Destination path relative to the repository root, for example
                "docs/codebase-map/architecture.md".
            content: The full file content to write.
        """
        rel_parts = Path(path).parts
        if rel_parts[: len(_DOCS_PREFIX)] != _DOCS_PREFIX:
            return f"error: refused, must be under docs/codebase-map/, got: {path}"
        try:
            target = _resolve_within(repo, path)
        except ValueError as exc:
            return f"error: {exc}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        docs_written.append("/".join(rel_parts))
        return f"wrote {len(content)} bytes to {path}"

    return [glob_files, read_file, grep, write_doc]
