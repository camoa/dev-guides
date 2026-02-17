---
description: Figma MCP rate limits by plan and seat type — daily and per-minute call limits, desktop server access requirements, and feature availability by server type
---

# Rate Limits and Access Tiers

### When to Use
Before committing to a workflow. Rate limits differ dramatically between plans — Starter plan users hit the monthly cap in a single session. Understanding your tier prevents mid-session failures.

### Items

#### Access by Plan and Seat Type

**Daily tool call limits:**
| Plan | Seat Type | Daily Limit |
|------|-----------|-------------|
| Enterprise | Full or Dev | 600 calls/day |
| Organization or Professional | Full or Dev | 200 calls/day |
| All plans | View or Collab | 6 calls/month |
| Starter | Any | 6 calls/month |

**Per-minute rate limits (for Full/Dev seats):**
| Plan | Per-minute limit |
|------|-----------------|
| Professional | 15 calls/min |
| Organization | 20 calls/min |
| Enterprise | Highest tier (contact Figma) |
| Starter / View / Collab | N/A (monthly cap applies instead) |

Per-minute limits follow the same tier as Figma's Tier 1 REST API. Figma reserves the right to change these limits.

#### Desktop Server Access
The desktop server (selection-based workflow) requires a **Dev or Full seat on any paid plan**. View and Collab seats cannot enable the desktop MCP server regardless of plan.

#### Feature Availability by Server Type
| Feature | Remote Server | Desktop Server |
|---------|--------------|----------------|
| All plans/seats | Yes | No (Dev/Full only) |
| Link-based workflow | Yes | Yes |
| Selection-based workflow | No | Yes |
| `whoami` tool | Yes | No |
| `generate_figma_design` tool | Yes | No |
| Code Connect toggle | Via file settings | Via inspect panel |

### Common Mistakes
- Running a full design system session on a Starter plan — 6 calls/month is exhausted by a single component generation (screenshot + context + variables = 3 calls minimum)
- Not checking `whoami` before a large session — verifies you're on the expected plan and seat type
- Exceeding per-minute limits with automated scripts — MCP is designed for interactive agent use; rate limiting is per-minute, not per-session

### See Also
- [Custom Agent Rules](custom-agent-rules.md) | [Best Practices and Patterns](best-practices-and-patterns.md)
- Reference: https://developers.figma.com/docs/figma-mcp-server/plans-access-and-permissions/
