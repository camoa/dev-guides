---
description: Pixelmatch performance characteristics and when to switch to odiff for faster image diffing.
tldr: Pixelmatch is single-threaded pure JS — adequate for suites under 500 screenshots. For larger suites or 4K captures, odiff is ~6x faster via native SIMD. Never replace pixelmatch inside Playwright's toHaveScreenshot — its auto-retry stability is tied to it.
---

# Pixelmatch Performance

## When to Use

> Read this when evaluating whether pixelmatch is fast enough for your suite size, or when CI diff throughput is a bottleneck.

## Decision

| Situation | Action |
|---|---|
| Suite < 500 screenshots per run | Stay on pixelmatch — latency is invisible |
| Suite 500–2000 screenshots | Pixelmatch acceptable; profile to confirm |
| Suite > 2000 screenshots | Consider odiff |
| 4K+ captures | odiff pays back even at small suite sizes |
| Playwright inner loop | Keep pixelmatch — it's tied to the auto-retry stability check |
| Post-process diff in CI | odiff is fine — drop-in via `odiff-bin` |

## Pattern: pixelmatch for the inner loop, odiff for post-process

Don't replace pixelmatch inside Playwright's `toHaveScreenshot()` — its auto-retry stability mechanism is tied to it. If suite size warrants, run odiff after the test run on the same PNGs to catch finer-grained diffs faster.

## Benchmarks

Per odiff's published Hyperfine benchmarks:

| Image | pixelmatch | odiff | Speedup |
|---|---|---|---|
| Cypress.io full-page diff | 7.712 s | 1.168 s | ~6.67× |
| 8K image diff | 10.614 s | 1.951 s | ~5.5× |

Pixelmatch is pure single-threaded JS — no SIMD, no native bindings.

## Common Mistakes

- **Wrong**: Replacing pixelmatch in Playwright's internals — breaks the auto-retry stability mechanism
- **Wrong**: Profiling pixelmatch on tiny test images — performance only matters at scale
- **Wrong**: Switching to odiff before identifying the bottleneck — capture often dominates over diff time; profile first

## See Also

- [Limitations & Alternatives](pixelmatch-limitations.md) — full comparison of pixelmatch vs odiff vs looks-same
- Reference: [odiff (faster alternative)](https://github.com/dmtrKovalenko/odiff)
