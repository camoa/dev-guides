---
description: Performance testing — types of perf tests, how to set budgets, and why performance assertions do not belong in the unit test suite.
tldr: Run performance tests in a dedicated CI stage on a stable environment, never in the unit suite. Set explicit budgets (P95 latency, Core Web Vitals — LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1) and enforce them. Always profile before optimizing.
---

# Performance Testing Concepts

## When to Use

> Use performance tests when the system must meet defined targets under realistic load. Run them in a dedicated CI stage on a stable environment — never in the unit test suite where CPU variance makes them non-deterministic.

## Decision

| Type | What it measures | Tools |
|---|---|---|
| Microbenchmark | A single function — ns/op, memory allocations | Go benchmarks, criterion (Rust), Benchmark.js |
| Load test | System behavior under expected concurrent users | k6, Locust, JMeter, Artillery |
| Stress test | System limits — at what load does it degrade? | Same tools as load; driven harder |
| Soak / endurance | Behavior over time — memory leaks, connection exhaustion | Long-running load test |
| Spike test | Response to sudden traffic bursts | Load test with step function |
| Performance budget | Front-end metric gates (Core Web Vitals + bundle size) | Lighthouse CI |

**Core Web Vitals (current as of 2024, INP replaced First Input Delay):**
- LCP (Largest Contentful Paint) ≤ 2.5 s
- INP (Interaction to Next Paint) ≤ 200 ms
- CLS (Cumulative Layout Shift) ≤ 0.1

## Pattern

```python
# Separate performance test file, not mixed with unit tests
@pytest.mark.performance
def test_search_meets_latency_budget(benchmark, db_with_10k_records):
    # benchmark.pedantic: runs N times, discards warmup
    result = benchmark.pedantic(
        db_with_10k_records.search,
        args=('alice',),
        rounds=100,
        warmup_rounds=5,
    )
    assert len(result) > 0
    assert benchmark.stats['mean'] < 0.050  # 50 ms budget
```

## Common Mistakes

- **Wrong**: Performance assertions in unit tests → **Right**: CI machines vary; results are non-deterministic and flaky
- **Wrong**: Measuring only single-user scenarios → **Right**: Test at realistic concurrency — APIs can be fast for one user and collapse under 100
- **Wrong**: Fixing performance without profiling → **Right**: Profile first; optimize the actual bottleneck, not a guess
- **Wrong**: No budget → **Right**: Performance regressions accumulate silently until they become a crisis
- **Wrong**: Load-testing a production database → **Right**: Always use a production-equivalent test environment

## See Also

- [Contract & API Testing Concepts](contract-api-testing-concepts.md) | Next: [Accessibility Testing Concepts](accessibility-testing-concepts.md)
- Reference: [web.dev Core Web Vitals](https://web.dev/articles/vitals)
- Reference: [k6 documentation — performance testing best practices](https://grafana.com/docs/k6/latest/testing-guides/)
