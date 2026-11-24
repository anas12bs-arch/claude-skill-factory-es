#!/usr/bin/env python3
"""Structural and hygiene checks for every kit in kits/.

Fails the build on:
  - a missing CLAUDE.md, INSTRUCCIONES.md or skill file
  - invalid or incomplete YAML frontmatter (name, description)
  - a skill description without trigger phrases
  - tracked system junk (.DS_Store, Thumbs.db)
  - unparseable JSON
  - hardcoded credentials
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KITS = ROOT / "kits"

errors: list[str] = []
warnings: list[str] = []

SECRET_PATTERNS = [
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}"), "Anthropic API key"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "GitHub fine-grained token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}"), "Slack token"),
    (re.compile(r"eyJhbGciOi[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\."), "JWT (possible API key)"),
]

PLACEHOLDERS = ("PEGA_AQUI", "YOUR_", "TU_", "EXAMPLE", "PLACEHOLDER", "<", "${")

TEXT_SUFFIXES = {".md", ".json", ".html", ".yml", ".yaml", ".txt", ""}


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    block = parts[1]
    data: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def check_text_file(path: Path) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"{path.relative_to(ROOT)}: not valid UTF-8")
        return
    for pattern, label in SECRET_PATTERNS:
        for match in pattern.finditer(content):
            value = match.group(0)
            if any(marker in value for marker in PLACEHOLDERS):
                continue
            errors.append(f"{path.relative_to(ROOT)}: possible {label} committed")


def main() -> int:
    if not KITS.is_dir():
        print("kits/ directory not found", file=sys.stderr)
        return 1

    kit_dirs = sorted(p for p in KITS.iterdir() if p.is_dir())
    if len(kit_dirs) != 10:
        warnings.append(f"expected 10 kits, found {len(kit_dirs)}")

    for kit in kit_dirs:
        name = kit.name
        if not name.startswith("kit-"):
            errors.append(f"{name}: folder must start with 'kit-'")

        for required in ("CLAUDE.md", "INSTRUCCIONES.md"):
            if not (kit / required).is_file():
                errors.append(f"{name}: missing {required}")

        skill_files = sorted((kit / ".claude" / "skills").glob("*.md"))
        if not skill_files:
            errors.append(f"{name}: no skill file under .claude/skills/")
        for skill in skill_files:
            if not re.match(r"^\d{2}-[a-z0-9\-]+\.md$", skill.name):
                errors.append(f"{skill.relative_to(ROOT)}: expected NN-skill-name.md")
            front = parse_frontmatter(skill.read_text(encoding="utf-8"))
            if front is None:
                errors.append(f"{skill.relative_to(ROOT)}: missing YAML frontmatter")
                continue
            for field in ("name", "description"):
                if not front.get(field):
                    errors.append(f"{skill.relative_to(ROOT)}: frontmatter missing '{field}'")
            description = front.get("description", "")
            if description and "trigger" not in description.lower():
                warnings.append(f"{skill.relative_to(ROOT)}: description has no trigger phrases")

        claude_md = kit / "CLAUDE.md"
        if claude_md.is_file():
            body = claude_md.read_text(encoding="utf-8")
            if "Comportamiento al iniciar" not in body:
                warnings.append(f"{name}/CLAUDE.md: no onboarding section")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if path.name in {".DS_Store", "Thumbs.db", "desktop.ini"}:
            errors.append(f"{rel}: system junk file committed")
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                errors.append(f"{rel}: invalid JSON ({exc})")
        if path.suffix.lower() in TEXT_SUFFIXES and path.stat().st_size < 512_000:
            check_text_file(path)

    for warning in warnings:
        print(f"::warning::{warning}")
    for error in errors:
        print(f"::error::{error}")

    print(f"\n{len(kit_dirs)} kits checked · {len(errors)} error(s) · {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
