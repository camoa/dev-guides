---
description: ATK release tracks — 2.0 stable, 2.1 beta (FedRAMP), 3.0 alpha (Drupal CMS), and how to pin the right one.
tldr: Use ATK 2.0.0 stable for production Drupal 11 sites. Use 2.1-beta only if you need FedRAMP tests, Feeds, or Tugboat support. Use 3.0-alpha only for Drupal CMS 2.x. The canonical source is git.drupalcode.org — GitHub PerformantLabs repos 404.
drupal_version: "11.x"
---

# ATK Versions & Compatibility

## When to Use

> Use this guide when picking the right ATK release track for your Drupal version and project requirements.

## Decision

| Track | Status | Drupal core | Drupal CMS | When |
|---|---|---|---|---|
| **2.0.0** stable | Released 2025-05-15 | 11.0–<12 | — | Default for D11 production sites |
| **2.1.0-beta5** | Beta (latest 2026-02-04) | 11.0–11.x | — | Need FedRAMP pack, Feeds test, Tugboat support, persistent sessions — willing to run beta |
| **3.0.0-alpha9** | Alpha (latest 2026-01-19) | 11.0–11.x | 2.x | Building on Drupal CMS 2.x |
| **1.3.0** legacy | Released 2024-11-30 | 10.x and 11 | — | Legacy D10 sites only |

Companion `automated_testing_kit_demo_recipe` mirrors the same tracks (2.0, 2.1, 3.0).

### Stable vs Beta

| Need | Track |
|---|---|
| Production-grade D11 with no FedRAMP | 2.0.0 stable |
| FedRAMP / Feeds / Tugboat sessions | 2.1.0-beta — accept beta status |
| Drupal CMS 2.x | 3.0.0-alpha — accept alpha status |
| D10 site that's not migrating yet | 1.3.0 (maintenance only, not active development) |

## Pattern

```bash
# 2.0 stable for D11 (recommended baseline)
composer require 'drupal/automated_testing_kit:^2.0'

# 2.1 beta — opt-in for FedRAMP track
composer require 'drupal/automated_testing_kit:^2.1@beta'

# 3.0 alpha — Drupal CMS 2.x
composer require 'drupal/automated_testing_kit:^3.0@alpha'
```

### Compatibility

| Aspect | Constraint |
|---|---|
| PHP | 8.3+ for Drupal 11 |
| Drupal core security policy | **Not covered** by Drupal Security Advisory Policy |
| Cypress | Latest stable |
| Playwright | Latest stable |

## Common Mistakes

- **Wrong**: Following stale URLs to `github.com/PerformantLabs/atk-cypress` → **Right**: those repos return 404; canonical source is `git.drupalcode.org/project/automated_testing_kit`
- **Wrong**: Running 1.3 against Drupal 11 → **Right**: designed for D10; use 2.0+ for D11
- **Wrong**: Treating FedRAMP track as stable → **Right**: 2.1 is beta; production use needs explicit acceptance of beta status

## See Also

- [FedRAMP & 2.1 Features](atk-fedramp.md)
- [Installation](atk-installation.md)
- Reference: https://www.drupal.org/project/automated_testing_kit/releases
