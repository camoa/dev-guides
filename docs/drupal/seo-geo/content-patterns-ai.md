---
description: Content writing patterns that increase AI citation frequency — answer-first design, statistics, source citations, entity salience, and recency signals
drupal_version: "11.x"
---

# Content Patterns for AI

## When to Use

> You are writing or editing content and want it cited by AI systems (ChatGPT, Google AI Overviews, Perplexity). These patterns are grounded in the Princeton/Georgia Tech GEO research (KDD 2024) and apply to any content type on your Drupal site. Apply these at the content creation stage, not as a post-processing step.

## Decision

| Content goal | Pattern | Priority |
|--------------|---------|----------|
| AI systems aren't citing your pages | Answer-first design + statistics | Start here |
| Competing pages outrank you in AI answers | Add credible source citations | High impact: +40% |
| Content feels qualitative and vague | Replace assertions with numbers | +30% visibility |
| Need authority signals | Add expert quotations | +20% visibility |
| Content is complete but rarely extracted | Self-contained sections | Structural fix |
| Pages cited for old information | Recency signals + freshness updates | 89.7% of citations go to recently updated pages |

## The Three Proven Strategies

These three strategies from the Princeton GEO paper (arxiv.org/abs/2311.09735) consistently produced the largest visibility gains across generative search platforms:

### 1. Cite Authoritative Sources (+40% avg. visibility)

AI systems use citation quality as a credibility proxy. Pages that reference authoritative external sources are more likely to be included in AI-generated answers.

**Pattern:**
- Cite primary sources (research papers, official documentation, government data, standards bodies)
- Use inline citations with links: "According to [OWASP](https://owasp.org/), ..."
- Prefer recent sources (within 2 years) — AI systems treat dated sources as weaker signals
- Name the source explicitly: "A 2024 Google Search Central study found..." is stronger than "Studies show..."

**Wrong:** "Research shows that structured data improves AI citation rates."
**Right:** "A 2024 Data World study found that GPT-4 accuracy improved from 16% to 54% when pages included Schema.org structured data."

### 2. Statistics Addition (+30% avg. visibility)

Quantitative, specific data anchors AI-generated summaries. AI models prefer content where claims are backed by numbers rather than qualitative language.

**Pattern:**
- Replace qualitative descriptions with quantitative measurements
- Include percentages, counts, durations, and dates
- Attribute statistics to their source
- Use precise numbers over rounded figures when accuracy allows

**Wrong:** "AI Overviews appear frequently in search results."
**Right:** "AI Overviews appear in approximately 16% of Google search queries as of Q1 2026."

**Wrong:** "Many AI citations come from lower-ranked pages."
**Right:** "83.3% of AI Overview citations come from pages ranked beyond position 10 in organic search results."

### 3. Quotation Addition (+20% avg. visibility)

Direct expert quotes signal that content has been produced through expert consultation, not synthesized from other web content. AI models treat quotations as authenticity markers.

**Pattern:**
- Include direct quotes from named experts, researchers, or practitioners
- Attribute quotes fully: name, title, organization
- Use quotes to add perspective, not to restate obvious facts
- One substantive quote per major section is enough

**Wrong:** "Experts agree that GEO is becoming important."
**Right:** "As Drupal Association Director Tim Lehnen noted in his 2025 DrupalCon keynote: 'Structured data is no longer optional — it is the minimum viable signal for AI discoverability.'"

## Entity Salience

AI models parse pages for **entities** — named people, organizations, places, concepts, products — and measure how central each entity is to the overall document. This is called entity salience.

| Concept | Traditional SEO equivalent | GEO approach |
|---------|--------------------------|--------------|
| Keyword density | Repeat keywords X times | Entity salience: entity appears in title, headings, body, and structured data |
| Topic authority | Domain authority + backlinks | Semantic centrality: entity discussed in depth with related entities |
| Measurement tool | Keyword rank trackers | Google Cloud Natural Language API entity salience scores |

**Salience threshold:** Aim for 0.10+ salience score for your primary entities using the Google Cloud Natural Language API. Below 0.05, an entity is unlikely to be recognized as the document's focus.

**Practical pattern:**
1. Identify 2-3 primary entities for each page
2. Ensure each entity appears in: the page title, at least one H2, the first 200 words, and your Schema.org structured data
3. Connect entities with semantic context — "Drupal" and "CMS" and "PHP" as co-occurring entities strengthen all three

## Answer-First Design

AI systems extract content snippets, often from the first 200 words of a section. If the answer is buried after preamble, it may be missed.

**Structure every page and section as:**

```
[Direct answer to the implied question — 1-2 sentences]

[Supporting context and detail]

[Evidence: statistics, citations, examples]
```

**Wrong structure:**
```
Drupal has evolved significantly over the years. Originally released in 2001,
it has grown into a mature CMS platform used by millions of sites. Many
organizations choose Drupal for content management. When considering SEO,
Drupal offers several useful modules.
→ Answer appears in paragraph 4
```

**Right structure:**
```
Drupal's SEO module stack (Metatag 2.2.0 + Schema Metatag 3.0.4 + Simple Sitemap 4.2.3)
covers all standard SEO requirements out of the box when installed via the
drupal_cms_seo_tools recipe.
→ Direct answer in sentence 1
```

**First 200 words checklist:**
- States the primary entity and topic
- Answers the most likely user question directly
- Contains at least one quantitative data point
- No preamble, throat-clearing, or history of the topic

## Self-Contained Sections

AI systems extract individual sections, not entire pages. Each `##` section must be understandable without reading the rest of the page.

**Pattern:**
- Begin each section with a 1-2 sentence context statement
- Define any acronyms on first use within the section
- Include the key fact or answer before linking elsewhere
- Do not use "as mentioned above" or forward references

**Wrong:**
```
## Statistics Addition
As noted in the previous section, the Princeton study is the primary reference here.
Use numbers to strengthen the patterns described above.
```

**Right:**
```
## Statistics Addition
Replacing qualitative claims with specific numbers increases AI citation rates by
approximately 30%, per the Princeton GEO study (arXiv:2311.09735). AI models anchor
summaries to specific data points.
```

## Recency Signals

89.7% of ChatGPT citations in a 2024 Seer Interactive analysis went to pages updated within the past 12 months. AI systems treat page freshness as a credibility signal.

| Signal | Implementation | Drupal mechanic |
|--------|---------------|----------------|
| Content update date | Update `dateModified` in Schema.org Article markup | Schema Metatag token: `[node:changed]` |
| Last reviewed date | Add explicit "Last reviewed: YYYY-MM-DD" line | Drupal field + token |
| Freshness in content | Reference current-year data points within text | Editorial practice |
| Sitemap changefreq | Set appropriate changefreq per content type | Simple Sitemap config |

**Minimum freshness practice:** Review and re-save high-value content at least every 6 months, even if the substantive content has not changed. Update the year on any statistics. AI systems can read the `dateModified` Schema.org property and the HTTP `Last-Modified` header.

## Common Mistakes

- **Wrong**: Writing for keyword density → **Right**: Write for entity salience and factual completeness; keyword stuffing actively harms AI citation quality
- **Wrong**: Burying the answer after an introduction → **Right**: Lead with the direct answer; context follows
- **Wrong**: Using "some studies show" → **Right**: Name the study, year, and finding with a link
- **Wrong**: One large monolithic page → **Right**: Self-contained sections that each answer a specific question independently
- **Wrong**: Updating only when content is wrong → **Right**: Refresh high-value pages every 6 months to maintain recency signals
- **Wrong**: Optimizing for a single AI platform → **Right**: These patterns improve citation across all AI platforms because they target the underlying LLM selection criteria

## See Also

- [GEO Overview](geo-overview.md) — research foundation and metrics
- [Schema.org for AI Discovery](schema-ai-discovery.md) — structured data reinforces entity salience
- [llms.txt Implementation](llms-txt-implementation.md) — point AI assistants at your best content
- Reference: [GEO Paper (arXiv:2311.09735)](https://arxiv.org/abs/2311.09735)
