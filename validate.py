#!/usr/bin/env python3
"""Validate every skill in this repo against the Agent Skills specification.

Spec: https://agentskills.io/specification

Usage:
    python3 validate.py            # validate ./skills
    python3 validate.py path/to/skills
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("This validator needs PyYAML. Install it with: pip install pyyaml")

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#][^)]*)\)")
FENCE_RE = re.compile(r"^```.*?^```", re.S | re.M)
KNOWN_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
MAX_LINES = 500


def check_skill(skill_dir):
    """Return (errors, warnings) for one skill directory."""
    errors, warnings = [], []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        return [f"no SKILL.md in {skill_dir}"], []

    text = skill_md.read_text(encoding="utf-8")

    match = FRONTMATTER_RE.match(text)
    if not match:
        return ["SKILL.md does not start with YAML frontmatter delimited by ---"], []

    try:
        front = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return [f"frontmatter is not valid YAML: {exc}"], []

    if not isinstance(front, dict):
        return ["frontmatter must be a YAML mapping"], []

    # name
    name = front.get("name")
    if not name:
        errors.append("name is required")
    elif not isinstance(name, str):
        errors.append("name must be a string")
    else:
        if not 1 <= len(name) <= MAX_NAME:
            errors.append(f"name must be 1 to {MAX_NAME} characters, got {len(name)}")
        if not NAME_RE.match(name):
            errors.append(
                f"name {name!r} must be lowercase alphanumeric and hyphens, "
                "with no leading, trailing, or consecutive hyphens"
            )
        if name != skill_dir.name:
            errors.append(f"name {name!r} must match the directory name {skill_dir.name!r}")

    # description
    description = front.get("description")
    if not description:
        errors.append("description is required and must be non-empty")
    elif not isinstance(description, str):
        errors.append("description must be a string")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"description must be at most {MAX_DESCRIPTION} characters, got {len(description)}")

    # compatibility
    compatibility = front.get("compatibility")
    if compatibility is not None:
        if not isinstance(compatibility, str):
            errors.append("compatibility must be a string")
        elif not 1 <= len(compatibility) <= MAX_COMPATIBILITY:
            errors.append(f"compatibility must be 1 to {MAX_COMPATIBILITY} characters, got {len(compatibility)}")

    # metadata must be a flat map of string to string
    metadata = front.get("metadata")
    if metadata is not None:
        if not isinstance(metadata, dict):
            errors.append("metadata must be a mapping")
        else:
            for key, value in metadata.items():
                if not isinstance(value, str):
                    errors.append(f"metadata.{key} must be a string, got {type(value).__name__}")

    for field in set(front) - KNOWN_FIELDS:
        warnings.append(f"unknown frontmatter field {field!r}")

    # body length: progressive disclosure keeps SKILL.md small
    line_count = text.count("\n") + 1
    if line_count > MAX_LINES:
        errors.append(f"SKILL.md must be under {MAX_LINES} lines, got {line_count}")

    # Links inside fenced blocks are templates for generated output, not real links.
    prose = FENCE_RE.sub("", text)

    # relative links must resolve
    for target in LINK_RE.findall(prose):
        if "://" in target or target.startswith("mailto:"):
            continue
        path = (skill_dir / target.split("#", 1)[0]).resolve()
        if not path.exists():
            errors.append(f"broken relative link: {target}")

    # every reference link should state when to load the file
    for target in LINK_RE.findall(prose):
        if not target.startswith("references/"):
            continue
        line = next((ln for ln in prose.splitlines() if target in ln), "")
        if not re.search(r"\b(when|if|before|after|once)\b", line, re.I):
            warnings.append(
                f"reference link {target} does not say when to load it "
                "(progressive disclosure works best with a trigger condition)"
            )

    errors.extend(check_evals(skill_dir, name))
    return errors, warnings


def check_evals(skill_dir, skill_name):
    """Return errors for the skill's evals/evals.json, if present."""
    evals_path = skill_dir / "evals" / "evals.json"
    if not evals_path.is_file():
        return [f"missing {evals_path.relative_to(skill_dir)}"]

    try:
        data = json.loads(evals_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"evals/evals.json is not valid JSON: {exc}"]

    errors = []
    if data.get("skill_name") != skill_name:
        errors.append(f"evals/evals.json skill_name must be {skill_name!r}")

    cases = data.get("evals")
    if not isinstance(cases, list) or not cases:
        return errors + ["evals/evals.json needs a non-empty 'evals' array"]

    for case in cases:
        case_id = case.get("id", "?")
        for field in ("id", "prompt", "expected_output"):
            if not case.get(field):
                errors.append(f"eval {case_id} is missing {field}")
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            errors.append(f"eval {case_id} needs a non-empty 'assertions' array")
    return errors


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "skills").resolve()
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")

    skill_dirs = sorted(d for d in root.iterdir() if d.is_dir())
    if not skill_dirs:
        sys.exit(f"no skill directories found in {root}")

    failed = 0
    for skill_dir in skill_dirs:
        errors, warnings = check_skill(skill_dir)
        if errors:
            failed += 1
            print(f"FAIL  {skill_dir.name}")
            for message in errors:
                print(f"        error: {message}")
        else:
            print(f"ok    {skill_dir.name}")
        for message in warnings:
            print(f"        warn:  {message}")

    print(f"\n{len(skill_dirs) - failed}/{len(skill_dirs)} skills valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
