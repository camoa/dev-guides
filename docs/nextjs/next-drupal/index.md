---
description: "Comprehensive guide for integrating Next.js with Drupal using the next-drupal library. Covers architecture decisions, setup, content fetching, rendering strategies, and more."
drupal_version: "11.x"
topic: "drupal/next-drupal"
guide-meta:
  concepts:
    - next-drupal library
    - NextDrupal client
    - decoupled architecture
    - draft mode
    - on-demand revalidation
    - "JSON:API fetching"
    - Next.js Drupal auth
  not:
    - Drupal Canvas (see drupal/canvas)
    - Astro or Nuxt integration
  requires:
    - drupal/jsonapi
  complements:
    - drupal/jsonapi
    - nextjs/deepchat-nextjs
    - drupal/multilingual
  specializes: ""
  category: nextjs
---

# Next.js for Drupal

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| **Choose between decoupled approaches** | [Decoupled Architecture Decision](decoupled-architecture-decision.md) | Choose decoupled Drupal with Next.js when you need modern frontend performance, independent backend/frontend development teams, or flexibility to serve multiple frontends from one Drupal backend. As of May 2026, next-drupal is minimally maintained and does not support Next.js 16 — weigh this before starting a long-lived build. |
| **Decide on JSON:API vs GraphQL** | [JSON:API vs GraphQL Decision](jsonapi-vs-graphql.md) | Both JSON:API and GraphQL work with next-drupal. JSON:API is simpler and built into Drupal core. |
| **Set up Drupal for Next.js** | [Drupal Setup](drupal-setup.md) | Follow this workflow when setting up a new Drupal backend for Next.js or adding Next.js support to an existing Drupal site. |
| **Initialize a Next.js project** | [Next.js Project Setup](nextjs-project-setup.md) | Use when creating a new Next.js frontend for an existing Drupal backend. App Router (Next.js 13+) is recommended over Pages Router. |
| **Configure the NextDrupal client** | [NextDrupal Client Configuration](nextdrupal-client-configuration.md) | Configure the NextDrupal client to customize API prefix, authentication, caching, deserialization, and other client behaviors. |
| **Set up authentication** | [Authentication Patterns](authentication-patterns.md) | Authentication is required for draft mode, creating/updating content, and accessing unpublished resources. Choose the pattern based on your security requirements and Drupal configuration. |
| **Fetch content from Drupal** | [Fetching Content](fetching-content.md) | Fetch JSON:API resources from Drupal for rendering in Next.js pages. All methods support filtering, sorting, includes, and sparse fieldsets. |
| **Build static or server-rendered pages** | [Building Pages](building-pages.md) | Build statically generated (SSG), server-rendered (SSR), or incrementally static regenerated (ISR) pages from Drupal content. App Router uses native fetch with Next.js cache options. |
| **Enable preview/draft mode** | [Draft Mode](draft-mode.md) | Enable content editors to preview unpublished content and revisions in an iframe within Drupal before publishing. |
| **Configure on-demand revalidation** | [On-Demand Revalidation](on-demand-revalidation.md) | Automatically update Next.js cached pages when content is created, updated, or deleted in Drupal. Supports path-based and tag-based revalidation. |
| **Handle images and media** | [Media and Images](media-images.md) | Handle Drupal media entities, image fields, and inline images in body fields using Next.js Image component for optimization. |
| **Support multiple languages** | [Multilingual Support](multilingual-support.md) | Support multiple languages in your Next.js site backed by multilingual Drupal content. |
| **Integrate search functionality** | [Search Integration](search-integration.md) | Implement search functionality using Drupal Search API exposed via JSON:API. |
| **Handle webform submissions** | [Webform Integration](webform-integration.md) | Submit webforms from Next.js to Drupal using the Webform REST module. Supports client-side and server-side (API route) submission. |
| **Configure environment variables** | [Environment Variables](environment-variables.md) | Configure Next.js connection to Drupal, authentication credentials, and feature flags using environment variables. |
| **Secure my implementation** | [Security Best Practices](security-best-practices.md) | Follow these practices for all Next.js + Drupal implementations to prevent common security vulnerabilities. |
| **Optimize performance** | [Performance Optimization](performance-optimization.md) | Apply these optimizations to reduce build times, improve page load speed, and minimize API requests. |
| **Troubleshoot common issues** | [Troubleshooting](troubleshooting.md) | Diagnose and resolve common issues when integrating Next.js with Drupal. |
| **Check sources and references** | [Sources & Maintenance](sources-maintenance.md) |  |
