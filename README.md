# Researcher Profile Distribution

Evidence-first Hermes specialist for academic and web research.

## Responsibilities

- Find and prioritize primary sources.
- Search and inspect academic papers with Hermes' bundled `arxiv` skill.
- Build verifiable citation ledgers with the bundled `grounded-citations` skill.
- Use Hermes' built-in web tools for current web research.
- Write research notes to Obsidian when the bundled `obsidian` skill is configured.
- Hand off cited findings rather than pretending uncertain claims are established facts.

## Install

```bash
hermes profile install github.com/faizulahasun-cloud/hermes-researcher --alias
```

The distribution intentionally does **not** pin a paid model/provider or require an OpenRouter key. Select the desired free/local/cloud model after installation using normal Hermes profile configuration.

It also intentionally does not ship a machine-specific filesystem MCP. Hermes already has native file/terminal capabilities, and bundled skills should remain owned and updated by Hermes.

## Cron jobs

Two optional jobs are included but ship **disabled** so installation cannot unexpectedly create recurring model usage:

- `daily-ai-briefing` — weekdays at 08:00
- `weekly-paper-digest` — Mondays at 09:00

Review the prompts, delivery target, model/provider and local timezone before enabling them.

## Required installation verification

After installation:

1. Confirm the alias/profile resolves correctly.
2. Confirm `arxiv` and `grounded-citations` are available.
3. Run one small research task requiring at least two primary sources.
4. Verify the citations resolve to the claims they support.
5. Test Obsidian separately only if an Obsidian vault is configured.

Do not mark this profile polished until those runtime checks pass on the target Hermes installation.
