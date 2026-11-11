"""A ~100-line agent that understands Agent Skills, running on a local model via Ollama.

It shows progressive disclosure:
  1. at startup only each skill's name + description go into the system prompt
  2. the model calls load_skill(name) to read the full SKILL.md when it needs it
  3. the model calls run_script / read_file to use the skill's bundled files

    ollama pull qwen3:4b          # any local model with tool calling
    python mini_skills_agent.py "Review my draft at sample_draft.md"
"""
import re, subprocess, sys
from pathlib import Path
import ollama, yaml

MODEL = "qwen3:4b"
SKILLS_DIR = Path(__file__).parent / "skills"


def discover_skills():
    skills = {}
    for md in SKILLS_DIR.glob("*/SKILL.md"):
        front = re.match(r"^---\n(.*?)\n---", md.read_text(encoding="utf-8"), re.S).group(1)
        meta = yaml.safe_load(front)
        skills[meta["name"]] = {"description": meta["description"], "dir": md.parent}
    return skills


SKILLS = discover_skills()


def inside(skill, rel):
    root = SKILLS[skill]["dir"].resolve()
    p = (root / rel).resolve()
    if root not in p.parents and p != root:
        raise ValueError("path escapes the skill folder")
    return p


# ---------- tools the model can call ----------
def load_skill(name: str) -> str:
    """Load the full instructions (SKILL.md) of a skill by name."""
    if name not in SKILLS:
        return f"No skill named {name}. Available: {list(SKILLS)}"
    return (SKILLS[name]["dir"] / "SKILL.md").read_text(encoding="utf-8")


def read_file(skill: str, path: str) -> str:
    """Read a file bundled with a skill, e.g. references/medium-checklist.md."""
    return inside(skill, path).read_text(encoding="utf-8")


def run_script(skill: str, script: str, args: str = "") -> str:
    """Run a Python script bundled with a skill, e.g. scripts/check_post.py, with arguments."""
    cmd = [sys.executable, str(inside(skill, script)), *args.split()]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return (out.stdout + out.stderr)[-6000:]


TOOLS = {f.__name__: f for f in (load_skill, read_file, run_script)}


def system_prompt():
    listing = "\n".join(f"- {n}: {s['description']}" for n, s in SKILLS.items())
    return ("You are a helpful assistant with access to skills.\n"
            "Available skills (name: when to use):\n" + listing + "\n\n"
            "If a skill matches the task, FIRST call load_skill(name) and follow its instructions. "
            "Paths in a skill are relative to that skill's folder.")


def chat(user_msg, max_steps=8):
    messages = [{"role": "system", "content": system_prompt()},
                {"role": "user", "content": user_msg}]
    for _ in range(max_steps):
        r = ollama.chat(model=MODEL, messages=messages, tools=list(TOOLS.values()),
                        options={"num_ctx": 8192, "temperature": 0})
        msg = r.message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content
        for call in msg.tool_calls:
            name, args = call.function.name, call.function.arguments
            print(f"  🔧 {name}({args})")
            try:
                result = TOOLS[name](**args)
            except Exception as e:
                result = f"error: {e}"
            messages.append({"role": "tool", "content": str(result), "tool_name": name})
    return "Stopped: too many steps."


if __name__ == "__main__":
    print(f"Skills found: {list(SKILLS)}\n")
    print(chat(" ".join(sys.argv[1:]) or "Review my draft at sample_draft.md"))
