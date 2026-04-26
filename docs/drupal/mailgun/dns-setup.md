---
description: Configure SPF, DKIM, DMARC, and MX DNS records for a Mailgun sending subdomain.
tldr: Set up a subdomain (e.g., mg.example.com) with SPF TXT record, two DKIM CNAMEs via Automatic Sender Security, and a DMARC TXT at the organizational root; start DMARC at p=none and escalate only after monitoring.
drupal_version: "11.x"
---

# DNS Setup

## When to Use

> Use this before sending any email through Mailgun. DNS records authenticate your sender identity (SPF, DKIM, DMARC) and enable inbound mail routing if needed (MX). Records propagate within minutes to 48 hours.

## Decision

| Question | Choose | Why |
|----------|--------|-----|
| Subdomain or root domain? | **Subdomain** (`mg.example.com`) | Isolates transactional sender reputation from marketing; avoids MX conflict with real inbound mail |
| Manual DKIM or Automatic Sender Security? | **Automatic** (default) | Auto-rotates 2048-bit keys every 120 days via two CNAMEs (`pdk1`, `pdk2`) |
| DMARC `p=none`, `quarantine`, `reject`? | Start `p=none`, escalate after monitoring | `p=reject` immediately can drop legitimate mail before alignment is confirmed |
| Add MX records? | Only if receiving inbound | Mailgun routes inbound when MX points to `mxa.mailgun.org`/`mxb.mailgun.org` |

## Pattern

#### Required records (subdomain `mg.example.com`)

| Type | Host | Value | Purpose |
|------|------|-------|---------|
| TXT | `mg.example.com` | `v=spf1 include:mailgun.org ~all` | SPF |
| CNAME | `pdk1._domainkey.mg.example.com` | `pdk1._domainkey.<UNIQUE>.dkim1.mailgun.com` | DKIM key 1 |
| CNAME | `pdk2._domainkey.mg.example.com` | `pdk2._domainkey.<UNIQUE>.dkim1.mailgun.com` | DKIM key 2 (rotation buffer) |
| CNAME | `email.mg.example.com` | `mailgun.org` | Click/open tracking links |
| MX | `mg.example.com` (priority 10) | `mxa.mailgun.org` | Inbound (optional) |
| MX | `mg.example.com` (priority 10) | `mxb.mailgun.org` | Inbound (optional) |

Exact values come from Mailgun's "Domain Verification" page after adding the domain.

#### DMARC (required for Gmail/Yahoo bulk-sender compliance since 2024)

Add at the **organizational root** (`example.com`), NOT the subdomain:

```
_dmarc.example.com  TXT  "v=DMARC1; p=none; rua=mailto:dmarc@example.com; pct=100; adkim=s; aspf=s"
```

Phased rollout: `p=none` (2-4 weeks) → `p=quarantine` (2-4 weeks) → `p=reject`.

#### Verifying records

```bash
dig +short TXT mg.example.com | grep spf
dig +short CNAME pdk1._domainkey.mg.example.com
dig +short CNAME pdk2._domainkey.mg.example.com
dig +short TXT _dmarc.example.com
```

## Common Mistakes

- **Wrong**: Using root domain (`example.com`) for transactional → **Right**: Use subdomain. MX on root would override your real inbound mail.
- **Wrong**: Using manual DKIM and never rotating → **Right**: Automatic Sender Security rotates every 120 days.
- **Wrong**: Going straight to `p=reject` → **Right**: Phased DMARC rollout; sites have lost legitimate mail to immediate `p=reject`.
- **Wrong**: Placing the `_dmarc` record on the sending subdomain → **Right**: DMARC must be at the organizational root for the subdomain to inherit policy.

## See Also

- [Region Selection](region-selection.md)
- [Verification & Testing](verification-testing.md)
- Reference: [Mailgun DKIM Security docs](https://documentation.mailgun.com/docs/mailgun/user-manual/domains/dkim_security)
- Reference: [Mailgun domain verification](https://documentation.mailgun.com/docs/mailgun/user-manual/domains/)
