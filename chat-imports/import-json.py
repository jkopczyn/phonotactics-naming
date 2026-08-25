#!/usr/bin/env python3
"""Convert a claude.ai share snapshot JSON (the /api/chat_snapshots/<uuid> response,
copied from the browser's Network tab) into Markdown.
Usage: import-json.py raw/<uuid>.json   ->  <uuid[:8]>-<slug>.md next to this script."""
import json, re, sys, pathlib, datetime

src = pathlib.Path(sys.argv[1]); d = json.loads(src.read_text())
name = d.get("snapshot_name") or "untitled"
slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60]
out = pathlib.Path(__file__).parent / f"{d['uuid'][:8]}-{slug}.md"
msgs = sorted(d["chat_messages"], key=lambda m: m["index"])

def render(m):
    parts = []
    for c in m["content"]:
        t = c["type"]
        if t == "text":
            if c["text"].strip(): parts.append(c["text"].strip())
        elif t == "tool_use":
            q = c.get("input"); q = "" if q in (None, {}) else f" `{json.dumps(q, ensure_ascii=False)[:300]}`"
            parts.append(f"*[tool_use: {c.get('name')}{q}]*")
        elif t == "tool_result":
            body = c.get("content") or []
            txt = " ".join(x.get("text", "") for x in body if isinstance(x, dict)).strip()
            parts.append(f"*[tool_result: {c.get('name')}]*" + (f"\n\n```\n{txt[:2000]}\n```" if txt else ""))
        else:
            parts.append(f"*[{t}]*")
    for a in m.get("attachments", []) + m.get("files", []):
        parts.append(f"*[attachment: {a.get('file_name') or a.get('name') or a}]*")
    return "\n\n".join(parts)

with out.open("w") as f:
    f.write(f"# {name}\n\nSource: https://claude.ai/share/{d['uuid']}  \n"
            f"Conversation dated {msgs[0]['created_at'][:10]}; imported {datetime.date.today()} from the share-snapshot JSON.\n\n---\n\n")
    for m in msgs:
        role = "User" if m["sender"] == "human" else "Claude"
        f.write(f"## {role}\n\n{render(m)}\n\n---\n\n")
print(out, len(msgs), "messages", sum(len(render(m)) for m in msgs), "chars")
