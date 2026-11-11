"""Tiny validator for the Agent Skills spec (agentskills.io/specification).
For the official one:  skills-ref validate ./my-skill
"""
import re, sys
from pathlib import Path
import yaml

ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def validate(skill_dir):
    d = Path(skill_dir); errors = []
    md = d / "SKILL.md"
    if not md.exists():
        return ["SKILL.md is missing"]
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return ["SKILL.md must start with YAML frontmatter between --- lines"]
    meta, body = yaml.safe_load(m.group(1)) or {}, m.group(2)
    name, desc = meta.get("name", ""), meta.get("description", "")
    if extra := set(meta) - ALLOWED: errors.append(f"unknown frontmatter fields: {sorted(extra)}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or "") or len(name) > 64:
        errors.append("name: 1-64 chars, lowercase letters/numbers/single hyphens, no leading/trailing hyphen")
    if name != d.name: errors.append(f"name '{name}' must match folder name '{d.name}'")
    if not (1 <= len(desc) <= 1024): errors.append("description must be 1-1024 characters")
    if "compatibility" in meta and not (1 <= len(meta["compatibility"]) <= 500):
        errors.append("compatibility must be 1-500 characters")
    if "metadata" in meta and not all(isinstance(k, str) and isinstance(v, str) for k, v in meta["metadata"].items()):
        errors.append("metadata must map strings to strings")
    if len(body.splitlines()) > 500: errors.append("keep SKILL.md under 500 lines (move detail to references/)")
    return errors


if __name__ == "__main__":
    for p in sys.argv[1:] or ["skills/medium-post-checker"]:
        errs = validate(p)
        print(f"{'✅' if not errs else '❌'} {p}")
        for e in errs: print("   -", e)
