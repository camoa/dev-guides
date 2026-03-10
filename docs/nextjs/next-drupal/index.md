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

| Task | Guide |
|------|-------|
| **Choose between decoupled approaches** | [Decoupled Architecture Decision](decoupled-architecture-decision.md) |
| **Decide on JSON:API vs GraphQL** | [JSON:API vs GraphQL Decision](jsonapi-vs-graphql.md) |
| **Set up Drupal for Next.js** | [Drupal Setup](drupal-setup.md) |
| **Initialize a Next.js project** | [Next.js Project Setup](nextjs-project-setup.md) |
| **Configure the NextDrupal client** | [NextDrupal Client Configuration](nextdrupal-client-configuration.md) |
| **Set up authentication** | [Authentication Patterns](authentication-patterns.md) |
| **Fetch content from Drupal** | [Fetching Content](fetching-content.md) |
| **Build static or server-rendered pages** | [Building Pages](building-pages.md) |
| **Enable preview/draft mode** | [Draft Mode](draft-mode.md) |
| **Configure on-demand revalidation** | [On-Demand Revalidation](on-demand-revalidation.md) |
| **Handle images and media** | [Media and Images](media-images.md) |
| **Support multiple languages** | [Multilingual Support](multilingual-support.md) |
| **Integrate search functionality** | [Search Integration](search-integration.md) |
| **Handle webform submissions** | [Webform Integration](webform-integration.md) |
| **Configure environment variables** | [Environment Variables](environment-variables.md) |
| **Secure my implementation** | [Security Best Practices](security-best-practices.md) |
| **Optimize performance** | [Performance Optimization](performance-optimization.md) |
| **Troubleshoot common issues** | [Troubleshooting](troubleshooting.md) |
| **Check sources and references** | [Sources & Maintenance](sources-maintenance.md) |
