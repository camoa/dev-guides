---
description: Core security principles including defense in depth, least privilege, zero trust, and threat modeling basics using STRIDE.
---

# Security Mindset Overview

## When to Use

Every developer must adopt a security-first mindset from day one. Security is not a feature you add later — it's a fundamental requirement woven into every design decision, code commit, and deployment.

## Core Security Principles

| Principle | What It Means | Why It Matters |
|---|---|---|
| **Defense in Depth** | Multiple layers of security controls — if one fails, others protect | Single defenses fail; layered security reduces breach impact |
| **Least Privilege** | Grant minimum permissions needed for functionality | Compromised accounts/processes cause less damage with minimal access |
| **Zero Trust** | Never trust, always verify — validate every request regardless of source | Network perimeter defense is dead; assume breach and verify everything |
| **Fail Securely** | System failures should deny access, not grant it | Bugs and errors happen; secure defaults prevent accidental exposure |
| **Complete Mediation** | Check every access to every resource every time | Cached permissions become stale; re-validate on each request |
| **Separation of Duties** | Critical operations require multiple independent parties | Prevents single person from compromising system (insider threats) |

## Threat Modeling Basics

**Before writing code, ask:**

1. What are we building? (Data flow diagrams, architecture)
2. What can go wrong? (STRIDE analysis)
3. What are we doing about it? (Mitigations, controls)
4. Did we do a good job? (Testing, verification)

**STRIDE Threat Categories:**

- **S**poofing identity — attacker pretends to be someone else
- **T**ampering with data — unauthorized modification of data
- **R**epudiation — denying actions without proof otherwise
- **I**nformation disclosure — exposing data to unauthorized users
- **D**enial of service — making system unavailable
- **E**levation of privilege — gaining unauthorized permissions

## Pattern

```text
Security Decision Framework:
1. Identify assets worth protecting (data, services, users)
2. Map trust boundaries (user → web server → database)
3. Enumerate threats at each boundary (STRIDE)
4. Prioritize by risk = likelihood × impact
5. Apply controls: Prevent → Detect → Respond → Recover
```

## Common Mistakes

- **Security theater over real security** — Focus on actual risk reduction, not checkbox compliance. A 16-character password requirement with no rate limiting is worse than 8 characters with proper account lockout
- **Trusting the client** — All client-side validation is UX, not security. Attackers control their HTTP requests completely. Server-side validation is mandatory
- **Obscurity as security** — Hiding implementation details slows attackers but doesn't stop them. Use cryptography and access controls, not obfuscation
- **Not updating threat models** — Threats evolve (2025 saw first self-replicating npm malware). Review and update threat models quarterly
- **Ignoring insider threats** — 34% of breaches involve insiders. Design systems assuming some users are malicious

## See Also

- Next: [OWASP Top 10](owasp-top-10.md)
- Reference: [OWASP Threat Modeling Process](https://owasp.org/www-community/Threat_Modeling_Process)
- Reference: [Microsoft STRIDE](https://www.practical-devsecops.com/what-is-stride-threat-model/)
