---
description: "Performance testing — types of perf tests, how to set budgets, and why performance assertions do not belong in the unit test suite."
tldr: "Run performance tests in a dedicated CI stage on a stable environment, never in the unit suite. Set explicit budgets (P95 latency, Core Web Vitals — LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1) and enforce them. Always profile before optimizing."
---

# Performance Testing Concepts

## When to Use

> When you need to verify that the system meets defined performance targets — response time, throughput, or memory usage — under realistic load. Performance testing is a specialized discipline separate from correctness testing; it requires different tools, different environments, and different metrics.

## Types of Performance Tests

| Type | What it measures | Tools |
|---|---|---|
| **Microbenchmark** | A single function or algorithm — ns/op, memory allocations | Go benchmarks, criterion (Rust), JMH (Java), Benchmark.js |
| **Load test** | System behavior under expected concurrent users | k6, Locust, JMeter, Artillery |
| **Stress test** | System limits — at what load does it degrade? | Same tools as load; driven harder |
| **Soak / endurance** | Behavior over time — memory leaks, connection exhaustion | Long-running load test |
| **Spike test** | Response to sudden traffic bursts | Load test with step function |
| **Performance budget** | Front-end metric gates (Core Web Vitals + bundle size) | Lighthouse CI, web.dev/measure |

## Performance Budgets

A **performance budget** turns a "feels fast" aspiration into a testable assertion:

- API endpoint P95 response time ≤ 200 ms under 100 concurrent users
- The three Core Web Vitals (current as of 2024, when INP replaced First Input Delay):
  - **LCP** (Largest Contentful Paint, loading) ≤ 2.5 s
  - **INP** (Interaction to Next Paint, interactivity) ≤ 200 ms
  - **CLS** (Cumulative Layout Shift, visual stability) ≤ 0.1
- JS bundle size ≤ 150 KB gzipped
- Database query count per page request ≤ 10 (no N+1)

Budgets are only useful if they are enforced in CI. A budget that no one checks is not a budget.

## Where Performance Testing Lives

**Do not** put performance tests in the unit test suite. Performance assertions in unit tests are:
- Non-deterministic (CI machines have different CPUs, load, and memory)
- Slow to run (benchmarks need many iterations to be statistically meaningful)
- Brittle (a CI runner with extra load will fail them spuriously)

**Do** run performance tests:
- In a dedicated CI stage on a stable environment
- Against a staging/performance environment that mirrors production
- On a schedule (nightly) rather than on every commit — unless you have a fast performance gate

## Common Pitfalls

- **Benchmarking without warmup** — JIT-compiled runtimes (JVM, V8, .NET CLR) run slower on the first few iterations; always include warmup iterations before recording
- **Testing a single thread for a concurrent-access system** — your API may be fast for one user but collapse under 100; always test at realistic concurrency
- **Ignoring the database** — application code benchmarks look fast, but the real bottleneck is usually N+1 queries or missing indexes; profile the full stack
- **No baseline to compare against** — a benchmark number means nothing without a historical series; track metrics over time to detect regressions

## Pattern

```python
# Separate performance test file, not mixed with unit tests
# Uses pytest-benchmark or similar

@pytest.mark.performance
def test_search_meets_latency_budget(benchmark, db_with_10k_records):
    # benchmark.pedantic runs the function N times, discards warmup
    result = benchmark.pedantic(
        db_with_10k_records.search,
        args=('alice',),
        rounds=100,
        warmup_rounds=5,
    )
    assert len(result) > 0
    # pytest-benchmark reports mean, std, min, max — fail in CI if mean > threshold
    assert benchmark.stats['mean'] < 0.050  # 50 ms budget
```

## Common Mistakes

- Writing performance assertions in unit tests → Brittle, non-deterministic, wrong tool for the job
- Measuring only single-user scenarios → Does not reveal concurrency bugs or resource exhaustion
- Fixing performance without first profiling → Profile first; optimize the actual bottleneck, not a guess
- Setting no budget → Without a budget, performance regressions accumulate silently until they become a crisis
- Load-testing a production database → Always use a production-equivalent test environment; load tests can corrupt or overwhelm production data

## See Also

- ← Previous: [Contract & API Testing Concepts](contract-api-testing-concepts.md) | Next: [Accessibility Testing Concepts](accessibility-testing-concepts.md) →
- Reference: [web.dev Core Web Vitals](https://web.dev/articles/vitals)
- Reference: [k6 documentation — performance testing best practices](https://grafana.com/docs/k6/latest/testing-guides/)
