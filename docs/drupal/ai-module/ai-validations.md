---
description: AI Validations — AI-powered field validation using XTRUE/XFALSE protocol and image classification
tldr: "**Status: DEPRECATED** — moving to standalone `drupal/ai_validations` (1.0.0-alpha1, pre-stable as of Jun 2026; keep using in-core until stable). Use when you need AI-powered field validation constraints with the Field Validation module (>=3.0.0-beta3)."
drupal_version: "11.x"
---

# AI Validations

## When to Use

> Use when you need AI-powered field validation constraints with the Field Validation module.

**Status:** DEPRECATED in AI Core — moving to standalone `drupal/ai_validations`. The standalone exists but is **1.0.0-alpha1** only (pre-stable as of Jun 2026); keep using the in-core submodule until a stable tag lands.
**Dependencies:** `ai`, `field_validation` (>=3.0.0-beta3)

Adds AI-powered field validation using Symfony constraints.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Validate text content with AI | `AiTextPrompt` constraint | LLM evaluates text via XTRUE/XFALSE |
| Validate uploaded image with AI | `AiImagePrompt` constraint | LLM evaluates image |
| Block images by content type | `AiImageClassification` constraint | Deny-list by classification tag |

## Validation Types

| Type | Constraint | Input | Protocol |
|------|-----------|-------|----------|
| Text prompt | `AiTextPrompt` | Text field value | XTRUE/XFALSE |
| Image prompt | `AiImagePrompt` | Image file | XTRUE/XFALSE |
| Image classification | `AiImageClassification` | Image file | Deny-list (block matching tags) |

## Critical: XTRUE/XFALSE Protocol

For text and image prompt constraints, the prompt **MUST** instruct the LLM to respond with exactly `XTRUE` (pass) or `XFALSE` (fail). The validator uses `str_contains()` — any other response format causes validation failure.

**Example prompt:**

```
You can only answer with XTRUE or XFALSE.
Take the following input and check if it mentions Drupal.
If it does, answer XTRUE. If it doesn't, answer XFALSE.
```

## Image Classification

Works as a **deny-list**: blocks images that match a classification tag above a confidence threshold. Example: block images classified as "violence" with >0.8 confidence.

## Setup

1. Install `ai_validations` + `field_validation`
2. Configure a Chat provider
3. Add validation rules via Field Validation UI
4. Write prompts following XTRUE/XFALSE protocol

## Common Mistakes

- **Wrong**: Prompt that returns "yes"/"no" or "true"/"false" → **Right**: The validator looks for `XTRUE`/`XFALSE` via `str_contains()` — any other format fails validation
- **Wrong**: Using `AiImageClassification` as an allow-list → **Right**: It is a deny-list — it blocks images that match the specified tags, not images that don't match

## See Also

- [AI Module Core Architecture](core-architecture.md)
- Reference: `web/modules/contrib/ai/modules/ai_validations/`
