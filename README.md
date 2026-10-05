# Researcher Profile Distribution

Autonomous research assistant with:
- **arXiv** — Search & retrieve academic papers
- **Grounded Citations** — Perplexity-style inline citations with verification
- **Web Search** — Exa/DuckDuckGo web research
- **Obsidian** — Read/write/search Obsidian vault
- **MCP Filesystem** — Local workspace access
- **Cron Jobs** — Daily AI briefing, weekly paper digest

## Install

```bash
hermes profile install github.com/faizulahasun-cloud/hermes-researcher --alias
```

## Setup

```bash
# 1. Fill in API keys
cp .env.EXAMPLE .env
# Edit .env with your keys

# 2. Configure Obsidian vault path (if using)
# Edit mcp.json filesystem path if needed

# 3. Start
researcher chat
```

## Cron Jobs (installed paused)

- `daily-ai-briefing` — Weekdays 08:00, local output
- `weekly-paper-digest` — Monday 09:00, local output

Enable with: `researcher cron resume <job-id>`

## Skills

Installed via `skills_install` in distribution.yaml:
- `official/research/arxiv`
- `official/research/grounded-citations`
- `official/research/web-search`
- `official/note-taking/obsidian`

These download from Skills Hub on first install.