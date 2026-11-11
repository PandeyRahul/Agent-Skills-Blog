---
name: medium-post-checker
description: Reviews a Markdown blog draft before publishing on Medium and gives a scored checklist (title, subtitle, hook, headings, images, code, length, links, tags). Use when the user asks to review, check, polish or improve a blog post, article or Medium draft, or asks why a post is not getting views.
license: MIT
metadata:
  author: rahul-pandey
  version: "1.0"
---

# Medium post checker

Use this skill to review a blog draft written in Markdown.

## Steps

1. Run the checker script on the draft and read its JSON output:
   `python scripts/check_post.py <path-to-draft.md>`
2. For every check with `"ok": false`, explain the problem in one line and suggest a concrete fix
   (rewrite the title, propose a subtitle, etc.). Do not just repeat the script output.
3. If the user wants deeper advice, read `references/medium-checklist.md` and apply the relevant points.
4. Finish with:
   - the overall score from the script (e.g. `7/10`)
   - the 3 most important fixes, in order
   - 5 suggested Medium tags

## Rules

- Never rewrite the whole post unless asked. Suggest changes.
- Keep the author's voice. Do not make the text more formal.
- If the file is not Markdown, say so and stop.
