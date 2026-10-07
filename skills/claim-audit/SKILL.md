---
name: claim-audit
description: Pre-publication pass. Extract claims from a draft and run claim_verify.
version: 2.0.0
metadata:
  hermes:
    tags: [Research, Verification, Audit]
    requires_toolsets: [hdr]
    requires_tools: [claim_verify, conflict_report, cite_source, citation_pass]
    related_skills: [deep-research-run, source-triage, literature-sweep]
---

# Claim audit

Check a draft before it ships. Exact spans. No lexical overlap.

## When to Use

Use this when the user says "check this draft" or asks for a pre-publication pass.
Do not use this to gather new sources (use deep-research-run).

## Quick Reference

```bash
python "${HERMES_SKILL_DIR}/scripts/extract_claims.py" briefs/draft.md
```

Then call `citation_pass` on the draft, or `claim_verify` on each claim. Call `conflict_report` once.

## Procedure

Extract claim sentences with `${HERMES_SKILL_DIR}/scripts/extract_claims.py`.
Call `citation_pass` with the draft text. It maps claims and runs `claim_verify`. If the host has no plugin LLM, the tool uses a deterministic sweep.
Unsupported claims are cut or sent back to depth. Do not keep a citation on an unsupported claim.
Call `conflict_report`. Name disagreements. Do not average them.
Call `cite_source` for the remaining `[S#]` markers.
Write the fixed brief under `briefs/` or `research/`.
Do not call raw `mcp_*` tools. `source_ledger_check` is gone. Do not look for it.
There is no `moa` toolset. For a second-model pass at `deep` or `exhaustive`, ask the operator to run `/moa` or `/model … --provider moa` on the top three load-bearing claims.

## Pitfalls

`claim_verify` proves a span exists. It does not prove the document is right.
A paraphrase with no exact span is unsupported. That is correct.

## Verification

- [ ] Zero `claim_verify` status `unsupported` on remaining cited claims.
- [ ] `conflict_report` is attached or explicitly empty.
- [ ] Every `[S#]` resolves.
- [ ] At `deep` or `exhaustive`: operator ran `/moa` or `/model … --provider moa` on the top three load-bearing claims. Leave unchecked until that happens.
