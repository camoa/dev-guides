---
description: How to share a Playwright HTML report with teammates, designers, or CI reviewers.
tldr: Share by zip+send, GitHub Actions artifact upload, static hosting, or port forwarding. Recipient always needs a real HTTP server (show-report) — never file://. For large reports with CDN-offloaded images, use attachmentsBaseURL with a trailing slash.
---

# Sharing Reports

## When to Use

> Use this when letting a teammate, designer, or reviewer look at a report you generated.

## Decision

| Approach | When |
|---|---|
| Zip + send | Quick teammate share |
| GitHub Actions artifact | Standard CI — retained per run |
| GitHub Pages / static hosting | Persistent URL per PR or SHA |
| Port forwarding | Give access to a report on a remote host |
| `attachmentsBaseURL` | Huge reports — offload images/traces to object storage |

## Pattern

Zip and send:

```bash
zip -r playwright-report.zip playwright-report/
```

Recipient extracts, then runs `npx playwright show-report ./playwright-report`.

GitHub Actions artifact (CI standard):

```yaml
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: playwright-report
    path: playwright-report/
    retention-days: 30
```

CDN-offloaded attachments:

```ts
reporter: [['html', { attachmentsBaseURL: 'https://cdn.example.com/runs/123/' }]],
```

The report fetches `data/<file>` from that base URL instead of next to `index.html`. Trailing slash is required.

## Common Mistakes

- **Wrong**: sharing via `file://` → **Right**: trace viewer breaks; recipient needs `show-report` or HTTP server
- **Wrong**: `attachmentsBaseURL` without trailing slash → **Right**: URL concatenation fails with 404 on every attachment
- **Wrong**: uploading `test-results/` instead of `playwright-report/` → **Right**: wrong artifact; report won't render

## See Also

- [Viewing](pw-report-viewing.md)
- [Running Modes](pw-report-running-modes.md)
- [Configuration Reference](pw-report-configuration.md)
