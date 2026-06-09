---
description: How Modern Web Guidance and the dev-guides repo complement each other — MWG covers the web platform layer, dev-guides covers Drupal/Bootstrap/stack-specific implementation.
tldr: MWG and dev-guides are complementary, not redundant. MWG is the upstream source of truth for web platform patterns (automatic, 128 task guides). Dev-guides adapts the in-charter subset for Drupal/Bootstrap/our stack (explicit load, opinionated patterns). MWG will not activate for Drupal Form API; dev-guides will not replace MWG for cutting-edge CSS questions.
drupal_version: ""
---

# Relationship to Dev-Guides

## When to Use

> Read this section if you use both Modern Web Guidance and this dev-guides repo and want to understand how they interact. They are complementary — they operate at different layers and neither replaces the other.

## Decision

| Layer | Modern Web Guidance | This dev-guides repo |
|---|---|---|
| Scope | All modern web platform features — CSS, HTML, JS APIs | Stack-specific: Drupal, Bootstrap, Radix, Next.js |
| Depth | 128 task-oriented guides, fetched on demand | Opinionated, stack-adapted patterns with security/performance guidance |
| Activation | Automatic — agent invokes CLI on relevant web tasks | Explicit — loaded via CLAUDE.md references or dev-guides-navigator |
| Baseline data | Real-time — from Baseline project | Static — documented at guide publication time |
| Charter | "How to do X with the web platform" | "How to do X in Drupal/Bootstrap/our stack" |

**Where they converge:** MWG's web platform guidance is the upstream source of truth. This repo adapts the in-charter subset — performance patterns, accessibility, form patterns, passkey implementation — for our specific stack and project constraints.

**Where MWG covers more:** Chrome extension development, WebMCP, built-in AI APIs, advanced CSS animation outside our stack patterns.

**Where this repo covers more:** Drupal-specific implementation of web patterns (Drupal Form API with `:user-invalid`, Twig accessibility markup, Drupal route-based passkey integration). MWG does not know about Drupal.

## Pattern

**Recommended workflow:**
1. For a web platform task (animate a dialog, improve INP, add passkeys): MWG activates automatically — let it inject the guide
2. For a Drupal/stack-specific question: use dev-guides-navigator to load the relevant guide
3. When both activate: MWG provides the platform pattern; the dev-guide provides the Drupal integration wrapper

**Cross-guide references:**

| Topic | MWG guidance area | Dev-guides guide |
|---|---|---|
| Core Web Vitals, INP | Performance | Performance (when published) |
| Accessible forms, ARIA | Accessibility | Accessibility (when published) |
| Passkey registration, auth | Passkeys | [Passkeys](../../js/passkeys/index.md) |
| Form validation, autofill | Forms | [HTML Forms](../../js/forms/index.md) |

## Common Mistakes

- **Expecting MWG to replace dev-guides for Drupal-specific tasks** — it only covers the web platform, not the framework layer
- **Expecting dev-guides to replace MWG for cutting-edge CSS/JS questions** — dev-guides cover a smaller, more opinionated subset
- **Concern about context cost when both activate** — MWG injects on demand (minimal cost); dev-guides are explicit; having both is fine and often useful

## See Also

- [Using It Effectively](using-it-effectively.md) — Baseline configuration
- [Passkeys](../../js/passkeys/index.md) — dev-guides implementation of MWG passkey guidance
- [HTML Forms](../../js/forms/index.md) — dev-guides implementation of MWG forms guidance
- Reference: [GitHub — Modern Web Guidance](https://github.com/GoogleChrome/modern-web-guidance)
