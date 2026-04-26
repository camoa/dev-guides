---
description: Compare Mailgun against SendGrid, Postmark, Brevo, AWS SES, and SMTP relay for Drupal transactional email in 2026.
tldr: Mailgun is the default developer-first choice for Drupal transactional email with EU region support and DKIM auto-rotation; choose Postmark for maximum deliverability on pure transactional, Brevo for budget or marketing-heavy sites, and SES only if already in the AWS ecosystem at scale.
drupal_version: "11.x"
---

# Alternatives Comparison

## When to Use

> Use this at project start (greenfield decision) or when reviewing an existing setup that's hitting Mailgun limits, deliverability issues, or pricing pressure.

## Decision

| Provider | Drupal contrib | 2026 free tier | Strength | Weakness |
|----------|---------------|----------------|----------|----------|
| **Mailgun** | drupal/mailgun 2.1.0 (mature) | 100/day, sandbox-restricted | Developer-first API, EU region, Auto Sender Security DKIM rotation | "Minimally maintained" module; free tier impractical |
| **SendGrid** | drupal/sendgrid_integration | Removed free plan late 2025 (60-day trial → paid) | Massive scale, marketing+transactional combined | Trial-only for new accounts |
| **Postmark** | community modules only | 100/month | Best-in-class transactional deliverability, fast | No marketing features; pricier per-email; weaker Drupal integration |
| **Brevo** (ex-Sendinblue) | drupal/brevo 1.0.6 (March 2026) | 300/day forever | Cheap; combines marketing + transactional + SMS | Slower API; less developer-focused |
| **AWS SES** | community SMTP module | First 62k/mo from EC2 free | Cheapest at scale ($0.10/1k) | Manual DKIM/reputation work; no built-in dashboard analytics |
| **Postfix / SMTP relay** | drupal/smtp | "Free" (own server cost) | Full control | You own deliverability, IP warmup, DKIM rotation, suppression |

## Pattern

#### Mailgun vs SendGrid

| Choose Mailgun | Choose SendGrid |
|----------------|----------------|
| Need EU data residency | Want bundled transactional + marketing campaigns |
| Want built-in DKIM rotation | Have existing SendGrid template library |

#### Mailgun vs Postmark

| Choose Mailgun | Choose Postmark |
|----------------|----------------|
| Mixed transactional + marketing | Pure transactional only |
| Need EU region | Best deliverability matters most |
| Cost-sensitive at scale | Drupal integration is custom anyway |

#### Mailgun vs Brevo

| Choose Mailgun | Choose Brevo |
|----------------|-------------|
| API/dev-first workflow | Marketing-heavy site, marketers in admin UI |
| Volume > 100k/mo | Tight budget, need 300/day free forever |

#### Mailgun vs AWS SES

| Choose Mailgun | Choose AWS SES |
|----------------|---------------|
| Want managed reputation, dashboards | Already in AWS ecosystem; cost-optimizing >100k/mo |
| Need event webhooks out of the box | OK with SNS-based event distribution |

#### When NOT to use Mailgun

- Pure transactional, < 10k/month, where Postmark's deliverability edge matters more than price
- Marketing-heavy site that wants list management + automation in the ESP
- Strict EU-only data residency with HSM-managed DKIM keys (Auto Sender Security stores keys with Mailgun)
- Free-tier-dependent personal projects (100/day is too restrictive for real users)
- Already running SES at scale; migration cost outweighs Mailgun's UX advantage

## Common Mistakes

- **Wrong**: Switching providers because of one bounce → **Right**: Diagnose deliverability first (DKIM alignment, content score, sender reputation). Provider is rarely the cause.
- **Wrong**: Picking based on free tier → **Right**: Free tiers in 2026 are too restrictive for production. Plan for paid tier from day one.
- **Wrong**: Running SMTP relay for "control" → **Right**: Unless you want to manage warmup, blocklists, and DKIM rotation yourself, ESP is worth the per-1k cost.

## See Also

- [Pricing & Tier Selection](pricing-tier-selection.md)
- Reference: [drupal/brevo](https://www.drupal.org/project/brevo)
- Reference: [drupal/sendgrid_integration](https://www.drupal.org/project/sendgrid_integration)
