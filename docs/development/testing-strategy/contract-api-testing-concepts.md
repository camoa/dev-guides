---
description: Contract and API testing — verifying service boundaries stay in sync as consumer and provider evolve independently.
tldr: Contract tests encode what a consumer expects from a provider, letting each deploy independently as long as the contract is honored. Justified when different teams own consumer and provider; overkill for same-repo services. Schema validation via OpenAPI is a simpler alternative.
---

# Contract & API Testing Concepts

## When to Use

> Use contract tests when consumer and provider are maintained by separate teams and deploy independently. For same-repo services, integration tests at the HTTP layer are sufficient.

## Decision

| Approach | What it verifies | When to use |
|---|---|---|
| Schema validation (OpenAPI/JSON Schema) | Response structure matches schema | Any HTTP API; easy to add; does not test behavior |
| Consumer-driven contract (Pact) | Consumer's actual usage pattern stays valid | When consumer and provider are maintained by separate teams |
| Integration test against a test server | Full request/response correctness | When consumer and provider are in the same repo/team |
| E2E with real services | Full system contract | Pre-production smoke tests only; too slow for CI |

Contract tests justify their cost when:
- Different teams own consumer and provider
- Provider deploys independently and could silently break consumers
- The API surface is large with many optional/versioned fields

## Pattern

```javascript
// Consumer side: records what the consumer expects (Pact-style)
const interaction = {
  description: 'a request for user profile',
  request: { method: 'GET', path: '/users/123' },
  response: {
    status: 200,
    body: {
      id: 123,
      name: Matchers.string('Alice'),
      email: Matchers.string('alice@example.com'),
    },
  },
};
// Consumer test runs against a mock provider using this contract.
// Contract is published; provider runs it against its real implementation.
```

**Simpler alternative:** OpenAPI schema validation — generate/maintain an OpenAPI spec, run `spectral lint` in CI, use the spec to generate a mock server, and validate API responses against the schema in integration tests.

## Common Mistakes

- **Wrong**: E2E tests across services instead of contract tests → **Right**: Requires both services live; slow; brittle; hard to isolate failures
- **Wrong**: Skipping contracts for "internal" APIs → **Right**: Internal APIs change and break consumers; contracts document the agreement
- **Wrong**: Over-specifying the contract (exact field values) → **Right**: Use type matchers, not exact values, where possible
- **Wrong**: No contract versioning strategy → **Right**: Breaking changes cause provider builds to fail without warning; version contracts

## See Also

- [Visual Regression Concepts](visual-regression-concepts.md) | Next: [Performance Testing Concepts](performance-testing-concepts.md)
- Reference: [Pact documentation — Consumer-Driven Contracts](https://docs.pact.io/)
- Reference: Martin Fowler, [ContractTest](https://martinfowler.com/bliki/ContractTest.html)
