---
description: Configuring Baseline browser support targets, understanding how the skill activates, invoking the CLI manually, and opting out of telemetry.
tldr: Set your Baseline target explicitly in CLAUDE.md — MWG defaults to Widely available if not set, which may be more conservative than your project allows. The skill activates automatically on relevant web tasks. If it misses a task, manually direct the agent to run modern-web-guidance search. Opt out of telemetry with DISABLE_TELEMETRY=1 in your shell profile.
drupal_version: ""
---

# Using It Effectively

## When to Use

> Read this section after installing. Covers Baseline configuration, how the skill activates, manual CLI invocation, and telemetry opt-out.

## Decision — Baseline Configuration

Baseline defines three browser support tiers: **Widely available** (≥30 months interoperable), **Newly available** (<30 months), and **Limited availability** (not yet interoperable). MWG uses your configured Baseline target to tailor guidance.

| If your project targets... | Add to CLAUDE.md or AGENTS.md |
|---|---|
| Widely available features only (safest, default) | No config needed |
| Features available since 2024 | `This project's Baseline target is Baseline 2024.` |
| Features available since 2023 | `This project's Baseline target is Baseline 2023.` |
| Cutting-edge / limited availability | Document explicitly; accept per-guide fallback burden |

**Pattern — AGENTS.md Baseline entry:**

```markdown
## AI Development Configuration
This project's Baseline target is Baseline 2024.
```

If no Baseline target is set, MWG defaults to **Baseline Widely available** — the most conservative option.

## Pattern

**How the skill activates:** On a relevant web development task, the agent runs:

```shell
modern-web-guidance search "animate a dialog modal backdrop"
modern-web-guidance retrieve "animate-to-from-top-layer"
```

Search runs **fully offline** using a local TensorFlow.js embedding model — no API keys, no network.

**Manual invocation:**

```shell
# Evaluate before installing
npx modern-web-guidance@latest search "INP optimization"
npx modern-web-guidance@latest retrieve "<guide-id>"
```

Or direct the agent: *"Run `modern-web-guidance search "INP optimization"` and use the result to improve this code."*

**Guidance coverage:**

| Area | Example use cases |
|---|---|
| Performance | INP, `scheduler.yield`, image priority, preloading |
| CSS / Layout | Container queries, `oklch`, anchor positioning, scroll-driven animations |
| Forms | `:user-invalid`, `field-sizing: content`, autofill attributes |
| Passkeys | Registration, authentication, conditional create, management |
| Accessibility | Screen reader operability, accessible form error feedback |
| Built-in AI | Language Detection API, Summarizer API, Translator API, Prompt API |

**Telemetry opt-out:**

```bash
# Add to ~/.bashrc or ~/.zshrc
export DISABLE_TELEMETRY=1
```

## Common Mistakes

- **Not setting a Baseline target** — MWG defaults to Widely available, which may be too conservative; set it explicitly
- **Treating the top search result as always correct** — check the `similarity` score; low similarity (< 0.5) means no guide is a strong match
- **Expecting MWG to activate for Drupal-specific tasks** — it covers the web platform layer; it will not activate for Drupal Form API or Twig questions

## See Also

- [Install for Other Agents](install-other-agents.md) — install commands
- [Relationship to Dev-Guides](relationship-to-dev-guides.md) — how MWG and dev-guides complement each other
- Reference: [Baseline project](https://github.com/web-platform-dx/web-features)
