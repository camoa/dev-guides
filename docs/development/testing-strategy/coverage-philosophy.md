---
description: Coverage as a diagnostic signal, not a goal — line vs. branch coverage, mutation testing, and practical thresholds.
tldr: Coverage tells you which lines were NOT executed, not whether tests verify correct behavior. 100% line coverage with vacuous assertions catches nothing. Use branch coverage over line coverage. Prefer mutation testing for quality signals on critical modules. Goodhart's Law applies — coverage mandates without quality enforcement produce hollow test suites.
---

# Coverage Philosophy

## When to Use

> Use coverage as a diagnostic signal to find untested paths — not as a goal to hit. When evaluating test suite adequacy or setting team standards, focus on what coverage does not tell you as much as what it does.

## Decision

| Threshold | Interpretation |
|---|---|
| < 60% | Insufficient for most projects; high risk of undetected bugs |
| 60–75% | Acceptable for many projects (Google considers 60% adequate) |
| 75–85% | Commendable; covers critical paths and most common branches |
| 85–90% | Excellent; diminishing returns begin here for typical code |
| > 90% | High investment; only justified for safety-critical systems |

**Line coverage vs. branch coverage:** Line coverage measures whether a line was executed. Branch coverage measures whether each branch (if/else, switch case, ternary) was taken in both directions. Always prefer branch coverage for logic-heavy code.

**Mutation testing** — the most reliable quality signal: a mutation testing tool introduces small deliberate faults (mutants) into code and checks whether at least one test fails for each. High mutation score = tests genuinely verify behavior. Tools: Stryker (JS/TS), PITest (Java), Infection (PHP), mutmut (Python). Use on critical modules, not the full codebase.

## Pattern

```python
def categorize_score(score):
    if score >= 90:       # Branch: True / False
        return 'A'
    elif score >= 80:     # Branch: True / False
        return 'B'
    return 'C'

# 100% line coverage, but 50% branch coverage:
test_categorize_score(95)  # hits True branches only
test_categorize_score(75)  # hits False branches only
# Missing: score=85 (second elif True branch)
```

## Common Mistakes

- **Wrong**: Enforcing 80% coverage without enforcing test quality → **Right**: Teams write hollow tests; coverage passes, production breaks
- **Wrong**: Treating line coverage as branch coverage → **Right**: Line coverage misses uncovered branches; measure branch coverage for logic-heavy code
- **Wrong**: No coverage measurement at all → **Right**: Add coverage tooling even if you set no mandates; it reveals untested paths
- **Wrong**: Gaming coverage with meaningless assertions → **Right**: `assert True` adds zero value; coverage ticks up, signal goes down
- **Wrong**: Measuring coverage over generated/trivial code → **Right**: Exclude DTOs, getters, config classes; they inflate numbers without value
- **Wrong**: Treating a coverage drop as an instruction to write tests here and now → **Right**: It is a signal to look; adding tests inside an unrelated bug fix makes that change harder to review and to revert

## See Also

- [Determinism and Flakiness](determinism-and-flakiness.md) | Next: [What to Test and What Not To](what-to-test-and-what-not.md)
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — Test Coverage Strategy section
- Reference: Martin Fowler, [TestCoverage](https://martinfowler.com/bliki/TestCoverage.html)
