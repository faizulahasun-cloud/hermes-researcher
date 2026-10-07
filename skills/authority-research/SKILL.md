---
name: authority-research
description: Find, retrieve, and verify primary law for the open issues in a matter, in parallel, without loading opinions into context.
version: 1.0.0
metadata:
  hermes:
    tags: [Legal, Research, Authority]
    requires_toolsets: [lex, web]
    requires_tools: [authority_search, authority_read, issue_plan, worker_brief]
    related_skills: [cite-check, draft-document]
---

# Authority Research

## When to Use
A matter is open and you need law: elements of a claim, the text of a statute,
the controlling standard, a rule's deadline period, whether a clause is
enforceable.

## Quick Reference
| Need | Route |
| --- | --- |
| case law | `authority_search kind=case` (CourtListener) |
| federal regulation | `authority_search kind=regulation` (eCFR) |
| federal statute | `authority_search kind=statute` (govinfo) |
| court rule / local rule | `authority_search kind=court_rule`, then the forum's own site |
| state code | `authority_search`, then the state legislature site via `web_extract` |
| a specific opinion or CFR part | `python3 ${HERMES_SKILL_DIR}/../../plugins/lex/scripts/fetch_authority.py` |

## Procedure
1. `issue_plan action=create` — one entry per independently researchable
   question, with its elements and the authority each would need.
2. For 2+ issues: `worker_brief` per issue, then one `delegate_task(tasks=[...])`
   batch. Children retrieve and register; they return findings, never text.
3. For a single narrow question: `authority_search` inline.
4. Read before you cite. `authority_read auth_id=A7 find="<phrase>"` returns the
   actual text. **A card is not a source.** You may not quote from a card.
5. `authority_status` on every case you intend to rely on. The treatment check
   is a citing-opinion count, not a validity ruling — read the recent citing
   opinions if the proposition is load-bearing.
6. Statutes, regulations, and rules carry an as-of date. If `stale: true`,
   re-retrieve. An accurate quote of a superseded provision is a wrong answer.
7. Tag each authority with the proposition it supports or contradicts so
   `conflict_report` can find splits.

## Pitfalls
- **Secondary sources as support.** A treatise, a firm alert, or a summary page
  is a map. Follow it to the primary source and cite that.
- **Circuit shopping by accident.** Sister-circuit and out-of-state authority
  is persuasive. The jurisdiction fence will block binding language over it.
- **Headnotes.** Never quote or cite an editorial headnote as the holding.
- **Fan-out without boundaries.** Two children with overlapping mandates
  produce duplicate authority and a coverage hole somewhere else.

## Verification
`issue_plan action=status` lists issues with no authority attached. Every
element of every claim you intend to plead should map to at least one
in-jurisdiction authority you have actually opened.
