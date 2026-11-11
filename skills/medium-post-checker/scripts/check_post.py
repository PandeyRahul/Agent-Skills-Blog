"""Score a Markdown blog draft against a simple Medium checklist. Prints JSON."""
import json, re, sys
from pathlib import Path

WPM = 238  # roughly Medium's reading speed


def check(path):
    text = Path(path).read_text(encoding="utf-8")
    lines = [l.rstrip() for l in text.splitlines()]
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    words = len(re.findall(r"\b\w+\b", body))
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), "")
    non_empty = [l for l in lines if l.strip()]
    after_title = non_empty[non_empty.index(next(l for l in non_empty if l.startswith("# "))) + 1] if title else ""
    headings = [l for l in lines if re.match(r"^#{2,3} ", l)]
    images = re.findall(r"!\[[^\]]*\]\([^)]+\)", text)
    code_blocks = len(re.findall(r"```", text)) // 2
    links = re.findall(r"(?<!!)\[[^\]]+\]\((https?://[^)]+)\)", text)
    first_para = next((l for l in non_empty if not l.startswith(("#", "!", ">"))), "")

    checks = [
        ("title_length", 40 <= len(title) <= 110, f"title is {len(title)} chars (aim 40-110)"),
        ("has_subtitle", after_title.startswith(("## ", "### ", "*", "_")), "line after title should be a subtitle"),
        ("hook", len(first_para.split()) <= 60, f"first paragraph is {len(first_para.split())} words (keep the hook short)"),
        ("headings", words / max(len(headings), 1) <= 400, f"{len(headings)} headings for {words} words (one per ~300)"),
        ("cover_image", bool(images) and text.find(images[0]) < len(text) * 0.15, "first image should appear near the top"),
        ("enough_images", len(images) >= max(1, words // 600), f"{len(images)} images (aim 1 per ~600 words)"),
        ("code", code_blocks >= 1, f"{code_blocks} code blocks"),
        ("length", 1000 <= words <= 3500, f"{words} words ≈ {round(words / WPM)} min read"),
        ("links", len(links) >= 2, f"{len(links)} links (link your code + related posts)"),
        ("closing", any(k in text.lower() for k in ("wrapping up", "conclusion", "takeaway", "lesson")), "has a wrap-up / takeaway section"),
    ]
    score = sum(ok for _, ok, _ in checks)
    return {"file": str(path), "words": words, "read_minutes": round(words / WPM),
            "score": f"{score}/{len(checks)}",
            "checks": [{"name": n, "ok": bool(ok), "detail": d} for n, ok, d in checks]}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python check_post.py <draft.md>")
    print(json.dumps(check(sys.argv[1]), indent=2, ensure_ascii=False))
