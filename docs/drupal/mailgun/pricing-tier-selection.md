---
description: "Select the right Mailgun pricing tier based on monthly email volume, log retention needs, and dedicated IP requirements."
tldr: "Go live on Free only with a CC on file (removes authorized-recipients restriction); upgrade to Basic ($15/10k) for volume or support needs, Foundation ($35/50k) when monthly sends exceed ~18k; skip dedicated IP until 100k+/month."
drupal_version: "10.3+/11/12"
---

# Pricing & Tier Selection

## When to Use

> At project planning, when growing past current tier, or during quarterly cost review.

## Decision

| Plan | Monthly | Included emails | Authorized-recipients only? | Notable |
|---|---|---|---|---|
| **Free** (no CC) | $0 | 100 emails/day (~3,000/mo) | **Yes** — real users can't receive mail | Useful only for sandbox/eval; cannot reach real users |
| **Free** (CC on file) | $0 | 100 emails/day (~3,000/mo) | No | Workable for personal sites & tiny volume; 1 day log retention |
| **Flex (PAYG)** | pay-as-you-go | — | No | $2.00 per 1,000 emails (raised Dec 2025) |
| **Basic** | $15 | 10k | No | Entry plan for serious production transactional |
| **Foundation** | $35 | 50k | No | 1,000 sending domains, 5-day log retention; overage $1.30/1k. Foundation 100k tier includes 1 dedicated IP |
| **Growth** | varies | 10k-50k tier | No | Dedicated IP option, subaccounts, < 24h support |
| **Scale** | $90 | 100k | No | Dedicated IPs, 5,000 validations, send-time optimization, live chat, 30-day log retention; overage ~$0.60/1k |

Additional dedicated IPs: $59/IP/month on Foundation 100k+, Growth, Scale.

**The "authorized-recipients only" restriction**: on Free without a credit card, every recipient must be pre-verified by clicking a verification email Mailgun sends them. Real users sign up and never receive your password reset, order confirmation, etc. Adding a CC removes this restriction even on Free.

## Pattern

#### Tier upgrade triggers

| Current tier | Upgrade to | When |
|---|---|---|
| Free (no CC) → Free (CC) or Basic | Add CC, OR Basic ($15/10k) | First production user signup. Without CC, recipient verification blocks real users |
| Free (CC) → Basic | Basic ($15/10k) | Volume exceeds 100/day, or you need multi-day log retention for support, or you want ticket support |
| Basic → Foundation | Foundation ($35/50k) | ~18,000 emails/month — Foundation $35/50k beats Basic $15/10k + overage there |
| Foundation → Scale | Scale ($90/100k) | Need >5-day log retention, send-time optimization, OR > 50k/month with low overage rate matters |
| Scale → custom/Enterprise | Talk to sales | Above ~1M emails/month or need multiple dedicated IPs cheaply |

#### Cost calculator example

For a Drupal site sending:
- 10k transactional/mo (order confirmations, password resets)
- 30k marketing/mo (weekly newsletter to 7,500 subs)

Total: 40k/mo.

| Plan | Cost |
|---|---|
| Basic + overage | $15 + (30k × $1.30/k) = **$54/mo** |
| Foundation | **$35/mo** flat |
| Foundation 100k | $80/mo (overhead, but headroom + 1 dedicated IP) |

Foundation is the right tier here.

#### Dedicated IP — when?

- Below ~100k/month: shared IP is fine; Mailgun manages reputation
- 100k-500k: dedicated IP starts paying off (your reputation, not shared with strangers)
- 500k+: definitely dedicated; consider IP pools (separate transactional from marketing)

Warming a dedicated IP requires 2-4 weeks of gradual volume increase. Plan ahead.

## Common Mistakes
- **Wrong**: Going live on Free without a credit card → **Right**: Add a CC (still $0/month) OR upgrade to Basic. Authorized-recipients restriction blocks real users until one of these is done.
- **Wrong**: Assuming Free is "for evaluation only" → **Right**: With CC on file, Free's 100 emails/day is enough for a personal site or low-volume blog. Upgrade when volume or features force it, not on principle.
- **Wrong**: Basic plan with 30k/month sends → **Right**: 30k - 10k included = 20k overage at $1.30/1k = $26 overage + $15 base = $41. Foundation at $35 is cheaper. Recalculate quarterly.
- **Wrong**: Provisioning dedicated IP at 5k/month → **Right**: Insufficient volume to maintain warmth; reputation actually worse than shared. Wait until 100k+.
- **Wrong**: Not checking Mailgun pricing page before quarterly budget review → **Right**: Pricing changes; PAYG was raised in Dec 2025. Verify current rates.

## See Also
- [Alternatives Comparison](alternatives-comparison.md)
- Reference: [Mailgun pricing page](https://www.mailgun.com/pricing/)
