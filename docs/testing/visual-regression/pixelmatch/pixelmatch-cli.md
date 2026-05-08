---
description: Pixelmatch CLI for ad-hoc shell-script PNG diffing — syntax, exit codes, and limitations compared to the API.
tldr: Run npx pixelmatch img1.png img2.png diff.png threshold in shell scripts. Exit code 0 means match, 66 means diffs detected (not an error), 64/65 are real failures. Colors, diffMask, and alpha are API-only — write a Node script for those.
---

# Pixelmatch CLI

## When to Use

> Use the CLI for ad-hoc shell-script diffing without writing Node code. Use the API when you need custom colors, `diffMask`, or `alpha`.

## Decision

| Need | Use |
|---|---|
| Quick ad-hoc diff in a shell script | CLI |
| Custom diff colors or mask | API (Node script) |
| Parse result in CI pipeline | CLI — check exit code |
| Threshold + includeAA control | CLI — positional args |

## Pattern

```bash
npx pixelmatch image1.png image2.png [diff.png] [threshold] [includeAA]
```

```bash
npx pixelmatch baseline.png current.png diff.png 0.1
if [ $? -eq 66 ]; then
  echo "Diffs detected — see diff.png"
  exit 1
fi
```

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Images match (no diff) |
| `64` | Not enough arguments |
| `65` | Image dimensions do not match |
| `66` | Differences detected |

## CLI vs API Options

| Option | CLI | API |
|---|---|---|
| `threshold` | Yes (positional) | Yes |
| `includeAA` | Yes (positional) | Yes |
| `alpha` | No | Yes |
| `aaColor`, `diffColor`, `diffColorAlt` | No | Yes |
| `diffMask` | No | Yes |

## Common Mistakes

- **Wrong**: Reading exit code 66 as "error" — it means "diffs detected," which is the result you asked for; distinguish from 64/65 which are real failures
- **Wrong**: Expecting all options on the CLI — colors, mask, and alpha are API-only
- **Wrong**: Omitting the output PNG path — specify it explicitly; defaults vary

## See Also

- [API](pixelmatch-api.md) — full Node.js API with all options
- [Standalone Use](pixelmatch-standalone.md) — Node script patterns for custom pipelines
- Reference: [mapbox/pixelmatch](https://github.com/mapbox/pixelmatch)
