---
name: probe-knob
description: Answer one config, hook, or tool question from Context7 and official pages. Record accept / reject / default with a [DOC] / [INF] / [UNV] tag.
version: 1.0.0
metadata:
  hermes:
    tags: [Factory, Docs, Knob]
    requires_toolsets: [inception]
    requires_tools: [docs_resolve, docs_ask, probe_knob]
    related_skills: [plan-profile, author-profile, review-profile]
---

# Probe one knob

One question. One official answer. One ledger row.

## When to Use

Use this when the user asks "is this key real?", "what is the default?", or "can we depend on this hook?"
Do not use this to write a profile tree (use author-profile).
Do not use this for a full isolation review (use review-profile).

## Quick Reference

```bash
python "${HERMES_SKILL_DIR}/scripts/classify_tag.py" --has-url true --pages-agree true
```

Then call `docs_resolve`, `docs_ask`, and `probe_knob`.

## Procedure

1. Call `docs_resolve` with the library name (`Hermes Agent` or `Honcho`).
2. Call `docs_ask` with the returned library id and the one knob question.
3. If Context7 misses, call `web_extract` on the official URL from the playbook or `llms.txt`. Do not add a search tool.
4. Classify the tag with `${HERMES_SKILL_DIR}/scripts/classify_tag.py`.
5. Call `probe_knob` with `knob`, `decision`, `tag`, `reason`, and `url` when the tag is `[DOC]`.
6. If the tag is `[UNV]`, set `code_depends` false.

Do not call raw `mcp_*` tools. The inception plugin registers `docs_resolve` and `docs_ask`.

## Pitfalls

A `[DOC]` row without an `https://` URL is rejected.
Code that reads an `[UNV]` knob is a ship blocker.
Honcho questions stay on `/plastic-labs/honcho` plus the settled memory paragraph.

## Verification

`probe_knob` returns `"ok": true` and a probe id.
The reason is one sentence.
The tag matches the script output.
