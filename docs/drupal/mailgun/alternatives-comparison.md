---
description: "Compare Mailgun against SendGrid, Postmark, Brevo, AWS SES, and SMTP relay for Drupal transactional email in 2026."
tldr: "Mailgun is the default developer-first choice for Drupal transactional email with EU region support and DKIM auto-rotation; choose Postmark for maximum deliverability on pure transactional, Brevo for budget/marketing-heavy sites or no-CC-required free tier, and SES only if already in the AWS ecosystem at scale."
drupal_version: "10.3+/11/12"
---

# Alternatives Comparison

## When to Use

> At project start (greenfield decision) or when reviewing an existing setup that's hitting Mailgun limits, deliverability issues, or pricing pressure.

## Decision

| Provider | Drupal contrib | 2026 free tier | Strength | Weakness |
|---|---|---|---|---|
| **Mailgun** | drupal/mailgun 2.1.0 (mature) + Symfony bridge | 100/day; authorized-recipients-only without CC, unrestricted with CC on file | Developer-first API, EU region, native SPF alignment, Auto Sender Security DKIM rotation | "Minimally maintained" module status; Free tier requires CC for real recipients |
| **SendGrid** | drupal/sendgrid_integration | Removed free plan late 2025 (60-day trial → paid) | Massive scale, marketing+transactional combined | Trial-only for new accounts; shared-IP reputation mixed |
| **Postmark** | community modules only | 100/month | Best-in-class transactional deliverability, fast | No marketing features; pricier per-email; weaker Drupal integration |
| **Brevo** (ex-Sendinblue) | drupal/brevo 1.0.6 (March 2026) | 300/day forever | Cheap; combines marketing + transactional + SMS + chat | Slower API; less developer-focused |
| **AWS SES** | community SMTP module | First 62k/mo from EC2 free | Cheapest at scale ($0.10/1k); EC2 integration | Manual DKIM/reputation work; no built-in dashboard analytics |
| **Postfix / SMTP relay** | drupal/smtp | "Free" (own server cost) | Full control | You own deliverability, IP warmup, DKIM rotation, suppression — too much work |

## Pattern

#### Mailgun vs SendGrid

| Choose Mailgun | Choose SendGrid |
|---|---|
| Need EU data residency | Need free tier for indie/personal projects (rare in 2026) |
| Want clean dev-first API | Want bundled transactional + marketing campaigns |
| Want built-in DKIM rotation | Have existing SendGrid template library |

#### Mailgun vs Postmark

| Choose Mailgun | Choose Postmark |
|---|---|
| Mixed transactional + marketing | Pure transactional |
| Need EU region | Best deliverability matters most |
| Cost-sensitive at scale | Drupal integration is custom anyway |

#### Mailgun vs Brevo

| Choose Mailgun | Choose Brevo |
|---|---|
| API/dev-first workflow | Marketing-heavy site, marketers in admin UI |
| Transactional focus | Need SMS, chat, contact CRM bundled |
| Volume > 100k/mo | Tight budget, need 300/day free forever |

#### Mailgun vs AWS SES

| Choose Mailgun | Choose AWS SES |
|---|---|
| Want managed reputation, dashboards | Already in AWS ecosystem; cost-optimizing >100k/mo |
| Don't want to manage IP warmup | Have ops bandwidth for SES sandbox graduation, IP setup |
| Need event webhooks out of the box | OK with SNS-based event distribution |

## When NOT to use Mailgun

- Pure transactional, < 10k/month, where Postmark's deliverability edge matters more than price
- Marketing-heavy site that wants list management + automation in the ESP — pick Brevo or SendGrid
- Strict EU-only data residency with HSM-managed DKIM keys (Auto Sender Security stores keys with Mailgun)
- Personal projects unwilling to add a credit card to Mailgun (Free without CC is sandbox-only); Brevo's 300/day forever-free no-CC tier wins this niche
- Already running SES at scale; the migration cost outweighs Mailgun's UX advantage

## Common Mistakes
- **Wrong**: Switching providers because of one bounce → **Right**: Diagnose deliverability first (DKIM alignment, content score, sender reputation). Provider is rarely the cause.
- **Wrong**: Picking based on free tier → **Right**: Free tiers in 2026 are too restrictive for production. Plan for paid tier from day one.
- **Wrong**: Running SMTP relay for "control" → **Right**: Own your reputation? Want to manage warmup, blocklists, and DKIM rotation yourself? Probably not. ESP is worth the per-1k.

## See Also
- [Pricing & Tier Selection](pricing-tier-selection.md)
- Reference: [drupal/brevo](https://www.drupal.org/project/brevo)
- Reference: [drupal/sendgrid_integration](https://www.drupal.org/project/sendgrid_integration)
