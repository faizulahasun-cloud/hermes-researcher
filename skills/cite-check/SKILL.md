---
name: cite-check
description: Audit any document for fabricated or unverifiable citations, unsupported legal assertions, and stale authority.
version: 1.0.0
metadata:
  hermes:
    tags: [Legal, Verification, Citations]
    requires_toolsets: [lex]
    requires_tools: [cite_check, authority_status, authority_read]
    related_skills: [authority-research, draft-document]
---

# Cite Check

## When to Use
Before delivering anything. Also on demand for a document someone else wrote —
including one produced by another AI system, which is the common case and the
reason this skill exists.

## Quick Reference
`cite_check text=<document>`. Treat `not_found` / `unresolved` as fabricated
until proven otherwise. Confirm support with `authority_read`. Check currency
with `authority_status`.

## Procedure
1. `cite_check text=<document>`. Every citation is extracted and resolved.
2. Triage the results:
   - `in_ledger` + `verified` — retrieved and real. Still confirm the
     proposition by opening it with `authority_read`.
   - `exists_not_retrieved` — the citation is real but nobody in this matter
     opened it. Retrieve it, or strike it.
   - `not_found` / `unresolved` — **treat as fabricated until proven otherwise.**
     A citation that no lookup can resolve does not go in a document.
3. For anything relied on heavily, run the external check:
   `python3 ${HERMES_SKILL_DIR}/../../plugins/lex/scripts/verify_citations.py <file>`
   (needs `COURTLISTENER_TOKEN`; exits non-zero if anything is unresolved).
4. `authority_status` each case: stale? unchecked? negative signals?
5. Read the `uncited_assertions` list. Each is a statement of law with no
   authority. Either cite it or cut it.
6. Report per citation: status, what it actually says, whether it supports the
   sentence it is attached to, and whether it is still good.

## Pitfalls
- **Real case, wrong proposition.** Resolution proves existence, not support.
  The second check is reading the opinion.
- **Correct citation, superseded statute.** Check the as-of date.
- **Parallel citations.** One case, several reporters. Do not report a
  parallel cite as a separate authority.
- **Assuming an unresolved cite is a lookup failure.** Sometimes it is. Say
  "unverified," never "verified."

## Verification
Zero unresolved citations and zero uncited assertions, or an explicit written
list of what could not be verified, delivered with the document.
