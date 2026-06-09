---
description: Modern Web Guidance install commands for Gemini CLI, GitHub Copilot, Goose, WebStorm, Vercel Agent Skills, Google Antigravity, and the cross-agent npx CLI.
tldr: The recommended cross-agent path is npx modern-web-guidance@latest install — runs an interactive wizard that detects your agent. Use --choose to install only the skill packs you need. Use --auto-update where available to keep guides current as MWG adds new content frequently.
drupal_version: ""
---

# Install for Other Agents and IDEs

## When to Use

> Use this catalog to find the install command for your agent or IDE. If unsure which agent you use, or you want the recommended cross-agent path, start with the **Modern Web Guidance CLI** entry.

## Decision

| Agent / IDE | Install command | Notes |
|---|---|---|
| Universal / cross-agent | `npx modern-web-guidance@latest install` | Interactive wizard; detects environment |
| Vercel Agent Skills | `npx skills add GoogleChrome/modern-web-guidance` | |
| GitHub CLI | `gh skill install GoogleChrome/modern-web-guidance` | |
| Gemini CLI | `gemini extensions install https://github.com/GoogleChrome/modern-web-guidance --auto-update` | |
| GitHub Copilot CLI | See two-step process below | No `/reload-plugins` needed |
| Goose | `goose plugin install https://github.com/GoogleChrome/modern-web-guidance --auto-update` | |
| Google Antigravity | `agy plugin install https://github.com/GoogleChrome/modern-web-guidance` | Also GUI: Settings > Customizations > Build with Google Plugins |
| JetBrains WebStorm | Settings > AI Assistant > Skills > Skill Manager | GUI-only |

## Pattern

**Modern Web Guidance CLI (recommended, cross-agent):**

```shell
# Install for detected agent(s) — interactive wizard
npx modern-web-guidance@latest install

# Install with skill pack selection
npx modern-web-guidance@latest install --choose

# Update existing install
npx modern-web-guidance@latest update
```

**GitHub Copilot CLI — two-step process:**

```shell
/plugin marketplace add GoogleChrome/modern-web-guidance
/plugin install modern-web-guidance@googlechrome
# No /reload-plugins required for Copilot
```

**WebStorm:**
1. Settings > AI Assistant > Skills
2. Open Skill Manager
3. Find "Modern Web Guidance" → click Install

## Common Mistakes

- **Using Claude Code `/plugin` steps for Copilot CLI** — commands are identical but Copilot does not need `/reload-plugins`
- **Installing via a path that does not include auto-update** — MWG adds new guides frequently; prefer `--auto-update` flags or AutoUpdate settings

## See Also

- [Install for Claude Code](install-claude-code.md) — Claude Code `/plugin` path
- [Using It Effectively](using-it-effectively.md) — Baseline configuration and manual CLI invocation
- Reference: [Chrome Docs — Get Started](https://developer.chrome.com/docs/modern-web-guidance/get-started)
