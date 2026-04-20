---
description: AI Content - AI-powered content creation, optimization, and management using Drupal AI module
guide-meta:
  concepts:
    - Drupal AI module
    - AI providers
    - AI automators
    - AI content workflow
    - CKEditor AI
    - vector databases
    - RAG
    - AI content generation
  not:
    - Figma MCP server
    - AI agent tooling
    - DeepChat web component
  requires: []
  complements:
    - drupal/seo-geo
    - drupal/caching
  specializes: ""
  category: drupal
---

# AI Content

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the AI module architecture and plugin system | [AI Module Architecture](architecture.md) | Use AI module architecture knowledge before implementing any AI functionality. Understanding the provider layer, model types, and plugin system is essential for choosing the right approach for your use case. |
| Choose and configure an AI provider (OpenAI, Anthropic, etc.) | [AI Provider Configuration](provider-configuration.md) | Configure AI providers before using any AI features. Use provider configuration when you need to establish authentication, model access, rate limits, and operational settings for AI services. |
| Implement structured content workflows | [AI Content Workflow](content-workflow.md) | Use the 8-stage AI content workflow when creating, managing, or optimizing content at scale. Use when you need consistent quality, SEO optimization, and strategic alignment. |
| Apply content frameworks (AIDA, PAS, BAB) | [Content Framework Patterns](framework-patterns.md) | Use content frameworks to structure AI content generation. Choose frameworks based on content goals: persuasion, information delivery, storytelling, or education. |
| Set up AI automators for content fields | [AI Automator System](automators.md) | Use AI Automators when you need consistent, automated content generation for specific fields without custom code. Use for field-level automation triggered on entity create or update. |
| Generate optimized metatags and descriptions | [SEO with AI](seo.md) | Use AI-powered SEO automation to generate optimized meta tags, descriptions, structured data, and content that ranks well in both traditional search engines and AI-powered discovery tools (ChatGPT, Perplexity, Google SGE). |
| Use AI in CKEditor for in-editor assistance | [CKEditor AI Integration](ckeditor.md) | Use CKEditor AI integration for in-editor AI assistance. Use when content creators need real-time content generation, rewriting, and enhancement without leaving the editing interface. |
| Ensure content quality and consistency | [Content Quality & Review](quality-review.md) | Use AI-powered quality review to ensure consistency, readability, and effectiveness across all content. Use the 4 C's framework (Clear, Concise, Compelling, Credible) for structured quality assessment. |
| Set up vector databases for semantic search | [Vector Databases & RAG](vector-rag.md) | Use vector databases for semantic search, content similarity analysis, and RAG (Retrieval-Augmented Generation) workflows. Use when you need to find conceptually similar content, power AI chatbots with site context, or analyze content… |
| Implement RAG for content intelligence | [Vector Databases & RAG](vector-rag.md) | Use vector databases for semantic search, content similarity analysis, and RAG (Retrieval-Augmented Generation) workflows. Use when you need to find conceptually similar content, power AI chatbots with site context, or analyze content… |
| Secure AI integrations and API keys | [Security & Privacy](security-privacy.md) | Security and privacy considerations are MANDATORY for all AI integrations. Every prompt, API call, and data flow must be evaluated for potential vulnerabilities and data exposure. |
| Optimize performance and manage rate limits | [Performance Optimization](performance.md) | Performance optimization is critical for AI features because API calls are slow (1-30+ seconds) and expensive. Optimize from day one to prevent poor user experience and cost overruns. |
| Avoid common mistakes | [Common Anti-Patterns](anti-patterns.md) | Learn from common mistakes to avoid technical debt, security vulnerabilities, poor user experience, and cost overruns. Every anti-pattern includes WHY it's problematic. |
