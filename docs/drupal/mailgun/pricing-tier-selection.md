---
description: Select the right Mailgun pricing tier based on monthly email volume, log retention needs, and dedicated IP requirements.
tldr: Never use the Free tier in production — authorized-recipients restriction breaks real users; start at Basic ($15/10k) and upgrade to Foundation ($35/50k) when monthly volume exceeds ~18k; don't provision a dedicated IP until you reach 100k/month volume.
drupal_version: "11.x"
---

# Pricing & Tier Selection

## When to Use

> Use this at project planning, when growing past current tier, or during quarterly cost review.

## Decision

| Plan | Monthly | Included emails | Notable |
|------|---------|----------------|---------|
| **Free / Trial** | $0 | 100 emails/day (~3,000/mo) | Authorized recipients only on Free without CC; unusable for real users |
| **Flex (PAYG)** | pay-as-you-go | — | $2.00 per 1,000 emails (raised Dec 2025) |
| **Basic** | $15 | 10k | Entry plan for production transactional |
| **Foundation** | $35 | 50k | 1,000 sending domains, 5-day log retention; overage $1.30/1k |
| **Scale** | $90 | 100k | Dedicated IPs, 5,000 validations, send-time optimization, 30-day log retention; overage ~$0.60/1k |

Additional dedicated IPs: $59/IP/month on Foundation 100k+, Growth, Scale.

## Pattern

#### Tier upgrade triggers

| Current tier | Upgrade to | When |
|-------------|-----------|------|
| Free → Basic | Basic ($15/10k) | Going to production. Free's "authorized recipients only" makes it unusable for real users |
| Basic → Foundation | Foundation ($35/50k) | ~18,000 emails/month — Foundation $35 beats Basic $15 + overage |
| Foundation → Scale | Scale ($90/100k) | Need >5-day log retention, send-time optimization, OR > 50k/month |
| Scale → Enterprise | Talk to sales | Above ~1M emails/month or need multiple dedicated IPs cheaply |

#### Cost calculator example (40k/mo)

| Plan | Cost |
|------|------|
| Basic + overage | $15 + (30k × $1.30/k) = **$54/mo** |
| Foundation | **$35/mo** flat |

Foundation is the right tier here.

#### Dedicated IP — when?

- Below ~100k/month: shared IP is fine; Mailgun manages reputation
- 100k-500k: dedicated IP starts paying off (your reputation, not shared)
- 500k+: definitely dedicated; consider IP pools (separate transactional from marketing)

Warming a dedicated IP requires 2-4 weeks of gradual volume increase.

## Common Mistakes

- **Wrong**: Using Free tier in production → **Right**: Authorized-recipients restriction means real users won't receive mail. Pay $15 minimum.
- **Wrong**: Basic plan with 30k/month sends → **Right**: 30k - 10k included = 20k overage at $1.30/1k = $26 overage + $15 base = $41. Foundation at $35 is cheaper. Recalculate quarterly.
- **Wrong**: Provisioning dedicated IP at 5k/month → **Right**: Insufficient volume to maintain warmth; reputation actually worse than shared. Wait until 100k+.
- **Wrong**: Not checking Mailgun pricing page before quarterly budget review → **Right**: Pricing changes; PAYG was raised in Dec 2025.

## See Also

- [Alternatives Comparison](alternatives-comparison.md)
- Reference: [Mailgun pricing page](https://www.mailgun.com/pricing/)
