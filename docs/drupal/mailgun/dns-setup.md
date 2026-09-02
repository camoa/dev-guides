---
description: "Configure SPF, DKIM, DMARC, and MX DNS records for a Mailgun sending subdomain."
tldr: "Set up a subdomain (e.g., mg.example.com) with SPF TXT record, two DKIM CNAMEs via Automatic Sender Security, and a DMARC TXT at the organizational root; start DMARC at p=none and escalate only after monitoring."
drupal_version: "10.3+/11/12"
---

# DNS Setup

## When to Use

> Before sending any email through Mailgun. DNS records authenticate your sender identity (SPF, DKIM, DMARC) and enable inbound mail routing if needed (MX). Records propagate within minutes to 48 hours.

## Decision

| Question | Choose | Why |
|---|---|---|
| Subdomain or root domain? | **Subdomain** (`mg.example.com`) | Isolates transactional sender reputation from marketing; avoids MX conflict with real inbound mail; lets you mix ESPs |
| Manual DKIM or Automatic Sender Security? | **Automatic** (default) | Auto-rotates 2048-bit keys every 120 days; uses two CNAMEs (`pdk1`, `pdk2`) so receivers verify against either during DNS-cache transitions |
| DMARC `p=none`, `quarantine`, `reject`? | Start `p=none`, escalate after monitoring | `p=reject` immediately can drop legitimate mail before alignment is confirmed |
| Add MX records? | Only if receiving inbound | Mailgun routes inbound when MX points to `mxa.mailgun.org`/`mxb.mailgun.org`. Skip for outbound-only |

## Pattern

#### Required records (subdomain `mg.example.com`)

| Type | Host | Value | Purpose |
|---|---|---|---|
| TXT | `mg.example.com` | `v=spf1 include:mailgun.org ~all` | SPF |
| CNAME | `pdk1._domainkey.mg.example.com` | `pdk1._domainkey.<UNIQUE>.dkim1.mailgun.com` | DKIM key 1 (Auto Sender Security) |
| CNAME | `pdk2._domainkey.mg.example.com` | `pdk2._domainkey.<UNIQUE>.dkim1.mailgun.com` | DKIM key 2 (rotation buffer) |
| CNAME | `email.mg.example.com` | `mailgun.org` | Click/open tracking links |
| MX | `mg.example.com` (priority 10) | `mxa.mailgun.org` | Inbound (optional) |
| MX | `mg.example.com` (priority 10) | `mxb.mailgun.org` | Inbound (optional) |

The exact values come from Mailgun's "Domain Verification" page after you add the domain in the Mailgun dashboard. Replace `<UNIQUE>` with the per-domain identifier Mailgun displays.

#### DMARC (recommended; required for Gmail/Yahoo bulk-sender compliance since 2024)

Add at the **organizational root** (`example.com`), NOT the subdomain:

```
_dmarc.example.com  TXT  "v=DMARC1; p=none; rua=mailto:dmarc@example.com; pct=100; adkim=s; aspf=s"
```

Phased rollout:
1. Deploy with `p=none` — monitor reports for 2-4 weeks
2. Confirm SPF + DKIM align across all sources (Mailgun, MX-only inbound, etc.)
3. Move to `p=quarantine` for 2-4 weeks
4. Final: `p=reject` only when confident

#### Verifying records

```bash
# SPF
dig +short TXT mg.example.com | grep spf

# DKIM (check both selectors)
dig +short CNAME pdk1._domainkey.mg.example.com
dig +short CNAME pdk2._domainkey.mg.example.com

# DMARC
dig +short TXT _dmarc.example.com
```

In Mailgun dashboard → Domains → `mg.example.com`, all records show green "Verified" once propagated. Click "Verify DNS Settings" if any are still pending.

## Common Mistakes
- **Wrong**: Using root domain (`example.com`) for transactional → **Right**: Use subdomain. MX on root would override your real inbound mail.
- **Wrong**: Using manual DKIM and never rotating → **Right**: Automatic Sender Security rotates every 120 days for you. Manual rotation requires DNS edits every cycle.
- **Wrong**: Going straight to `p=reject` → **Right**: Phased DMARC rollout; sites have lost legitimate mail to immediate `p=reject`.
- **Wrong**: Forgetting that the `_dmarc` record lives on the root domain, not the sending subdomain → **Right**: DMARC must be at the organizational root for the subdomain to inherit policy.

## See Also
- [Region Selection](region-selection.md)
- [Verification & Testing](verification-testing.md)
- Reference: [Mailgun DKIM Security docs](https://documentation.mailgun.com/docs/mailgun/user-manual/domains/dkim_security)
- Reference: [Mailgun domain verification](https://documentation.mailgun.com/docs/mailgun/user-manual/domains/)
