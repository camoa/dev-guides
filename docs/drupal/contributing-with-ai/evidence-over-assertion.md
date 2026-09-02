---
description: "Evidence over assertion — gates in AI-assisted contribution pass only on captured artifacts (command output, test results, live pipeline status), never on AI claims"
tldr: "Every contribution gate must be satisfied by a produced artifact — captured phpcs/phpunit output, verified API docs, actual pipeline status. AI saying 'this passes' or 'this is secure' is never sufficient. Any code change after a gate passed requires that gate to be re-run."
drupal_version: "11.x"
---

# Evidence Over Assertion

## When to Use

> When deciding whether a gate has been satisfied — whether your AI-assisted contribution is ready to advance to the next step. This section describes the principle that gates pass only on captured artifacts (command output, test results, a live pipeline result), never on AI claiming "done," "passes," or "should work."

## Decision: Artifacts vs. Claims

Every check in the AI-assisted contribution workflow must be satisfied by a **produced artifact** — not by AI asserting that the check passes. The recurring failure this prevents: AI confidently stating correctness it has never actually verified.

| Gate | Required Artifact | NOT Sufficient |
|---|---|---|
| Coding standards pass | Captured `phpcs` output showing zero errors | AI saying "this follows Drupal coding standards" |
| Tests pass | Captured `phpunit` output showing zero failures/warnings | AI saying "the tests should pass" |
| API exists | Verified against drupal.org API docs or core source | AI saying "this function exists in Drupal 11" |
| Security reviewed | Traced data flow from input to output in code | AI saying "this is secure" |
| Pipeline green | Actual GitLab pipeline status fetched via API | Local green + "CI should pass" |
| Understanding confirmed | You can answer the six "Senior Developer" questions (see [Human Review Requirements](human-review-requirements.md)) | "I reviewed the code" without specifics |

## Pattern: The No-Guessing Rule for External Facts

Any fact that lives outside the AI session — an SDK symbol, API signature, library version behavior, drupal.org issue status — must be verified against an authoritative source or a live probe. Model memory and changelog lines are *leads*, never facts.

```
External fact (e.g., "does \Drupal\Core\Cache\CacheableMetadata::createFromObject() exist?")
  → Verify against: drupal.org API docs, or core source file
  → Unverified = blocker — do not submit code that depends on unverified API existence

External fact (e.g., "is issue #3565917 the live AI policy?")
  → Verify against: drupal.org directly
  → Result: It is Postponed; the live policy is the separate adopted document
```

If the AI cannot verify a fact through a tool call or file read, the fact is **unverified**. Unverified external facts are blockers, not guesses to proceed with.

## Pattern: Re-Verification After Post-Gate Changes

Any code edited after a gate was satisfied re-requires that gate to pass again. This is the most common escape hatch for unverified code:

1. Tests pass (gate satisfied)
2. You add a new function at a reviewer's request
3. The new function is not covered by the passing tests
4. Result: tests were green for a codebase that no longer includes the new function

**Rule:** If you change a file after its gate passed, re-run that gate for the changed path before marking the contribution ready.

## Common Mistakes

- **"AI verified it"** — AI cannot run commands. It can describe what a command would do. The output of an actual tool call is the artifact; AI's description of what the output "should be" is not.
- **Interpreting a green pipeline as "linting passes"** — Linting jobs in drupalci are non-blocking by default. A green overall pipeline does not mean phpcs or phpstan passed. Check the individual job status.
- **Skipping re-verification after changes** — A post-feedback code change that introduces a new function, new dependency, or new route resets the gate for that area.
- **Treating model memory as documentation** — AI may have accurate recall of a Drupal 9 API that was removed in Drupal 11. Verify against the target version's docs.

## See Also

- [Drupal AI Policy](drupal-ai-policy.md) — the contributor bears full responsibility for submitted output
- [Human Review Requirements](human-review-requirements.md) — the six questions that confirm understanding
- [Merge Request Workflow](merge-request-workflow.md) — pipeline interpretation and CI non-blocking behavior
- [AI Code Review Checklist](ai-code-review-checklist.md) — the artifact-based pre-submission checklist
