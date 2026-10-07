---
name: source-triage
description: Dedupe and tier a pasted URL list, bibliography, or search dump. Not a ranker tool.
version: 2.0.0
metadata:
  hermes:
    tags: [Research, Sources, Triage]
    requires_toolsets: [hdr]
    requires_tools: [evidence_add, evidence_search]
    related_skills: [deep-research-run, literature-sweep, web-fallback-fetch]
---

# Source triage

Turn a pile of URLs into a deduped, tiered ledger. This skill is a recipe. It is not a ranking tool.

## When to Use

Use this when the user pasted URLs, a bibliography, or a search dump.
Do not use this to start a full research loop (use deep-research-run).

## Quick Reference

```bash
python "${HERMES_SKILL_DIR}/scripts/dedupe_urls.py" urls.txt
```

Then `evidence_add` each surviving URL. Call `evidence_search` to review cards.

## Procedure

Write the raw URLs to `sources/urls.txt`.
Run `${HERMES_SKILL_DIR}/scripts/dedupe_urls.py`. Tracking query params and mobile mirrors collapse.
For each remaining URL, `evidence_add` with whatever snippet you have. If you have full text, pass `text` so the corpus fills.
Tiering is computed by the store. Do not invent a score.
Prefer primary sources. Two copies of one press release are one source.
Use `web_search` / `web_extract` only to fill `needs_backfill` rows.
Do not call raw `mcp_*` tools.

## Pitfalls

Do not treat this skill as a substitute for `gap_scan`.
Do not keep UTM copies as distinct sources.

## Verification

`evidence_search` shows one card per canonical URL.
Backfill-needed rows are listed, not hidden.
