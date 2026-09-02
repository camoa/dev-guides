---
description: "Contract and API testing — verifying service boundaries stay in sync as consumer and provider evolve independently."
tldr: "Contract tests encode what a consumer expects from a provider, letting each deploy independently as long as the contract is honored. Justified when different teams own consumer and provider; overkill for same-repo services. Schema validation via OpenAPI is a simpler alternative."
---

# Contract & API Testing Concepts

## When to Use

> When you have a boundary between services — a REST API, GraphQL endpoint, or message contract — and you need to verify that the consumer's expectations and the provider's behavior stay in sync as both evolve independently. Contract tests sit between integration tests and E2E tests on the cost/confidence curve; they are the right tool for service-oriented architectures.

## What Contract Testing Is

A **contract test** encodes the expectations one service has of another. There are two parties:

- **Consumer** — the service that calls the API; writes tests that define what it expects (request/response shape, status codes, field presence)
- **Provider** — the service that serves the API; runs the consumer's contract tests against its own implementation to verify it still satisfies them

The key insight: you do not need a live integration between services to verify the contract. The consumer tests describe the contract; the provider verifies the contract independently. Both can develop and deploy independently as long as contracts are honored.

## Types of Contract / API Verification

| Approach | What it verifies | When to use |
|---|---|---|
| **Schema validation** (OpenAPI/JSON Schema) | Response structure matches schema | Any HTTP API; easy to add; does not test behavior |
| **Consumer-driven contract** (Pact) | Consumer's actual usage pattern stays valid | When consumer and provider are maintained by separate teams |
| **Integration test against a test server** | Full request/response correctness | When consumer and provider are in the same repo/team |
| **E2E with real services** | Full system contract | Pre-production smoke tests only; too slow for CI |

## When Contract Tests Are Worth the Investment

Contract tests justify their cost when:
- Different teams own the consumer and provider
- Provider deploys independently and could silently break consumers
- The API surface is large with many optional/versioned fields
- You are migrating from a monolith to microservices and need a safety net

Contract tests are overkill when:
- Consumer and provider are in the same repository and deploy together
- A single developer owns both sides
- The API surface is tiny and already covered by integration tests

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

## API Schema Testing (Simpler Alternative)

If full consumer-driven contracts are overkill, schema validation via OpenAPI is a useful middle ground:

- Generate/maintain an OpenAPI spec for the API
- Run `spectral lint` or similar in CI to verify the spec itself
- Use the spec to generate a mock server for consumer tests
- Validate API responses against the schema in integration tests

This catches schema drift without requiring a full Pact infrastructure.

## Common Mistakes

- Using E2E tests across services in place of contract tests → Requires both services live; slow; brittle; hard to isolate failures
- Skipping contracts entirely for "internal" APIs → Internal APIs change and break consumers; contracts document the agreement
- Over-specifying the contract (exact field values) → Contract becomes brittle; use type matchers, not exact values, where possible
- No contract versioning strategy → Breaking contract changes cause provider builds to fail without warning; version contracts and communicate changes

## See Also

- ← Previous: [Visual Regression Concepts](visual-regression-concepts.md) | Next: [Performance Testing Concepts](performance-testing-concepts.md) →
- Reference: [Pact documentation — Consumer-Driven Contracts](https://docs.pact.io/)
- Reference: [Martin Fowler, ContractTest](https://martinfowler.com/bliki/ContractTest.html)
