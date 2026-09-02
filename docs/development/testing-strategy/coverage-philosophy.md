---
description: "Coverage as a diagnostic signal, not a goal — line vs. branch coverage, mutation testing, and practical thresholds."
tldr: "Coverage tells you which lines were NOT executed, not whether tests verify correct behavior. 100% line coverage with vacuous assertions catches nothing. Use branch coverage over line coverage. Use mutation testing on critical modules to find checks that cannot fail at all, not as proof that the tests specify the right behavior. Goodhart's Law applies — coverage mandates without quality enforcement produce hollow test suites."
---

# Coverage Philosophy

## When to Use

> When evaluating whether your test suite is adequate, when setting team standards, or when you encounter coverage mandates. Coverage is a diagnostic tool, not a correctness guarantee.

## Goodhart's Law and Coverage

**Coverage percentage tells you which lines were executed during tests. It does not tell you whether those tests are useful.**

You can achieve 100% line coverage with tests that assert nothing. You can have 60% line coverage and catch every bug that matters. The number is a signal, not a goal.

Goodhart's Law: "When a measure becomes a target, it ceases to be a good measure." Coverage mandates without quality enforcement produce test suites that hit the number and catch nothing.

## What Coverage Tells You (and Doesn't)

**Coverage tells you:** which lines, branches, and paths were NOT executed during tests. Uncovered critical logic is a gap to address.

**Coverage does not tell you:**
- Whether tests verify the right behavior
- Whether tests catch real bugs (a test that always passes is worthless)
- Whether the system is correct
- Whether integration points work

## Line Coverage vs. Branch Coverage

Line coverage measures whether a line was executed. Branch coverage measures whether each branch (if/else, switch case, ternary) was taken in both directions.

```python
def categorize_score(score):
    if score >= 90:       # Branch: True / False
        return 'A'
    elif score >= 80:     # Branch: True / False
        return 'B'
    return 'C'

# 100% line coverage, 50% branch coverage:
test_categorize_score(95)  # hits line 1, 2; only True branches
test_categorize_score(75)  # hits line 1, 2, 3; only False branches of first two
# Missing: score=85 (second elif True)
```

**Prefer branch coverage (or condition coverage) over line coverage.** Most tools support it.

## Mutation Testing

Mutation testing verifies that tests actually catch bugs. A mutation testing tool introduces small deliberate faults (mutants) into the code — changing `>=` to `>`, `+` to `-`, removing a conditional — and checks whether at least one test fails for each mutation.

If a mutation survives (no test fails), your test suite has a gap at that point: nothing you have asserts on the behavior that mutant changed.

A high mutation score means the suite is **sensitive to the code as written**, and that is narrower than it sounds. Killing a mutant proves a test is coupled to the implementation — which is exactly what a test written from finished code already is. It does not prove the test states a promise anyone made, and it is never evidence that a test was written before the code. Mutation testing answers "can this check fail at all?". Whether the code does what was promised is a different question, and only a test authored from the contract answers it.

Tools: Stryker (JS/TS), PITest (Java), Infection (PHP), mutmut (Python).

Mutation testing is slow (runs the full suite per mutation) but it is the most reliable way to find checks that cannot fire at all. Use it on critical modules, not the full codebase.

## Practical Coverage Thresholds

These are starting points — not absolute rules. Context (risk level, team maturity, project stage) always overrides them.

| Threshold | Interpretation |
|---|---|
| < 60% | Insufficient for most projects; high risk of undetected bugs |
| 60–75% | Acceptable for many projects (Google considers 60% adequate) |
| 75–85% | Commendable; covers critical paths and most common branches |
| 85–90% | Excellent; diminishing returns begin here for typical code |
| > 90% | High investment, likely covering trivial code; only justified for safety-critical systems |

Set the threshold that reflects your risk profile, not the highest number you can achieve.

## Common Mistakes

- Enforcing 80% coverage without enforcing test quality → Teams write hollow tests; coverage passes, production breaks
- Treating line coverage as branch coverage → Line coverage misses uncovered branches; always measure branch coverage for logic-heavy code
- No coverage measurement at all → You are flying blind; add coverage tooling even if you set no mandates
- Gaming coverage with meaningless tests → `assert True` passes; coverage ticks up; value is zero
- Using coverage on generated/trivial code → DTOs, getters, config classes inflate coverage measurements without value; exclude them
- Treating a coverage drop as an instruction to write tests here and now → It is a signal to look. Adding tests inside an unrelated bug fix makes that change harder to review and to revert
- Reading a high mutation score as proof the suite specifies the right behavior → It proves the tests are coupled to the code, which a test written from the finished code always is
- Breaking working code to watch a test fail and recording that as test-first → That is mutation verification; it proves sensitivity, never authoring order

## See Also

- ← Previous: [Determinism and Flakiness](determinism-and-flakiness.md) | Next: [What to Test and What Not To](what-to-test-and-what-not.md) →
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — Test Coverage Strategy section
- Related: [What a Failing Test Proves](https://camoa.github.io/dev-guides/development/tdd-spec-driven/what-a-failing-test-proves/) — why a red run does not establish that a test came first
- Reference: Martin Fowler, [TestCoverage](https://martinfowler.com/bliki/TestCoverage.html)
