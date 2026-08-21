---
description: All user-facing text must be CMS-editable — section headings come from block labels or view titles, never from Twig.
drupal_version: "11.x"
tldr: "All user-facing text must be CMS-editable. Section headings come from block labels or view titles — never from Twig. Exception: structural labels like \"by\" or \"//\" separators in metadata."
---

# No Hardcoded Content in Templates

**What:** All user-facing text must be CMS-editable. Section headings come from block labels or view titles — never from Twig. Exception: structural labels like "by" or "//" separators in metadata.

**Rationale:** Hardcoded text in templates can't be changed without a deploy. Editors lose autonomy, translation workflows break, and "small copy tweaks" become engineering tickets. Block labels, view titles, field labels, and configurable text fields all give editors control without touching code.

**When it applies:** Any template (`.html.twig`) that renders for end users. Structural separators (commas, ampersands, label glue like "by") are exempt because they're typographic plumbing, not content.

**Example:**

```twig
{# Wrong — copy lives in code #}
<h2>Latest News</h2>
{{ drupal_view('news', 'block_1') }}

{# Right — view title or block label provides the heading #}
{{ drupal_view('news', 'block_1') }}
{# View configured with title: "Latest News" → renders inside the view's wrapper #}

{# Or for a custom block #}
{# block label "Latest News" set in admin → label_display: visible #}

{# Acceptable exception — typographic glue #}
<span class="byline">by {{ author.label }}</span>
<span class="meta-separator">//</span>
```
