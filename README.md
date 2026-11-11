# Agent Skills — code for the blog

A real Agent Skill (`medium-post-checker`) plus a ~100-line local agent that loads skills with progressive disclosure.

```
skills/medium-post-checker/
├── SKILL.md                      # name + description + instructions
├── scripts/check_post.py         # 10 checks on a Markdown draft -> JSON
└── references/medium-checklist.md
mini_skills_agent.py              # tiny skills agent on Ollama tool calling
validate_skill.py                 # checks SKILL.md against the spec rules
sample_draft.md                   # a deliberately weak draft to test with
```

## Run

```bash
pip install -r requirements.txt

# validate the skill (official tool: skills-ref validate ./skills/medium-post-checker)
python validate_skill.py skills/medium-post-checker

# run the script directly
python skills/medium-post-checker/scripts/check_post.py sample_draft.md

# run the agent on a local model (any Ollama model with tool calling; edit MODEL at the top)
ollama pull qwen3:4b
python mini_skills_agent.py "Review my draft at sample_draft.md"
```

## Use it in Pi

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent   # Node.js 22.19+
mkdir -p ~/.agents/skills && cp -r skills/medium-post-checker ~/.agents/skills/
```

Add Ollama to `~/.pi/agent/models.json`:

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [{ "id": "qwen3:4b" }]
    }
  }
}
```

In Pi: `/model` to pick it, then `/skill:medium-post-checker sample_draft.md`.
