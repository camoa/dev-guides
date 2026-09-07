---
description: "How to share a Playwright HTML report with teammates, designers, or CI reviewers."
tldr: "Share by zip+send, GitHub Actions artifact upload, static hosting, or port forwarding. Recipient always needs a real HTTP server (show-report) — never file://. For large reports with CDN-offloaded images, use attachmentsBaseURL with a trailing slash."
---

# Sharing Reports

## When to Use

> Letting a teammate, designer, or reviewer look at a report you generated.

## Pattern: Zip + Send

```bash
zip -r playwright-report.zip playwright-report/
```

Recipient extracts, then runs `npx playwright show-report ./playwright-report`. **A real HTTP server is needed** for traces — `file://` breaks trace iframes.

## Pattern: GitHub Actions Artifact (CI Standard)

```yaml
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: playwright-report
    path: playwright-report/
    retention-days: 30
```

Reviewers download from the run's Artifacts panel.

## Pattern: GitHub Pages (gh-pages Style)

Push `playwright-report/` to a `gh-pages` branch keyed by SHA or PR number; serve via Pages. Each PR gets a stable URL.

## Pattern: Static Hosting

Netlify drop, S3 + CloudFront, Cloudflare Pages, internal nginx — just upload the directory.

## Pattern: Port Forwarding

```bash
ssh -L 9323:localhost:9323 ci-host
# while show-report runs there
```

## Pattern: `attachmentsBaseURL` for CDN-Offloaded Images

For huge reports where you want the HTML/JS only and offload images/traces to object storage:

```ts
reporter: [['html', { attachmentsBaseURL: 'https://cdn.example.com/runs/123/' }]],
```

The report fetches `data/<file>` from that base URL instead of looking next to `index.html`. Trailing slash is required.

## Common Mistakes

- **Sharing via `file://`** — recipient sees a broken trace viewer
- **`attachmentsBaseURL` without trailing slash** — URL concatenation fails; "404 not found" on every attachment
- **Uploading `test-results/` instead of `playwright-report/`** — wrong artifact; report won't render

## See Also

- [Viewing](pw-report-viewing.md)
- [Running Modes](pw-report-running-modes.md)
- [Configuration Reference](pw-report-configuration.md)
