---
description: Installing Modern Web Guidance for Claude Code using the /plugin command interface — marketplace registration, install, and AutoUpdate configuration.
tldr: Three steps in Claude Code — /plugin marketplace add GoogleChrome/modern-web-guidance, /plugin install modern-web-guidance@googlechrome, /reload-plugins. Skipping /reload-plugins means the skill does not activate. Enable AutoUpdate through /plugin settings — MWG adds new guides frequently.
drupal_version: ""
---

# Install for Claude Code

## When to Use

> Follow this process when setting up Modern Web Guidance for the first time in a Claude Code environment. The `npx` universal installer (covered in [Install for Other Agents](install-other-agents.md)) also works for Claude Code.

## Decision

| Step | Command | Notes |
|---|---|---|
| 1. Add marketplace | `/plugin marketplace add GoogleChrome/modern-web-guidance` | Claude Code slash command, not a shell command |
| 2. Install plugin | `/plugin install modern-web-guidance@googlechrome` | |
| 3. Reload plugins | `/reload-plugins` | Skill does not activate until plugins are reloaded |
| 4. Enable AutoUpdate | Via `/plugin` settings UI | Keeps skill content current without manual updates |

## Pattern

Run inside a Claude Code session:

```
/plugin marketplace add GoogleChrome/modern-web-guidance
/plugin install modern-web-guidance@googlechrome
/reload-plugins
```

**Enable AutoUpdate:** After `/reload-plugins`, run `/plugin`. In the plugin manager UI: select the GoogleChrome marketplace, press Enter, then enable AutoUpdate for `modern-web-guidance`.

**Verify installation:** After `/reload-plugins`, ask the agent a modern web task (e.g., "animate a dialog exit"). If MWG is active, the agent will invoke `modern-web-guidance search` before generating code.

**Updating an existing install:**

```shell
npx modern-web-guidance@latest update
```

## Common Mistakes

- **Skipping `/reload-plugins`** — the skill does not activate until plugins are reloaded
- **Running the commands outside a Claude Code session** — these are Claude Code slash commands, not shell commands
- **Not enabling AutoUpdate** — MWG actively adds new guides; stale installs miss coverage for newly shipped features

## See Also

- [What Is Modern Web Guidance](what-is-modern-web-guidance.md) — skill vs. MCP distinction
- [Install for Other Agents](install-other-agents.md) — `npx` universal installer also works for Claude Code
- Reference: [Chrome Docs — Get Started](https://developer.chrome.com/docs/modern-web-guidance/get-started)
