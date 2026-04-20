---
description: "Comprehensive guide for working with Drupal's JSON:API module (core) and JSON:API Extras (contrib). Covers spec-compliant REST API with filtering, includes, pagination, and customization."
drupal_version: "11.x"
topic: "drupal/jsonapi"
guide-meta:
  concepts:
    - "JSON:API"
    - "JSON:API Extras"
    - resource types
    - filtering
    - includes
    - sparse fieldsets
    - pagination
    - "JSON:API CRUD"
  not:
    - REST module
    - GraphQL
    - Next.js client setup (see nextjs/next-drupal)
  requires:
    - drupal/entities
  complements:
    - nextjs/next-drupal
    - drupal/security
    - drupal/caching
  specializes: ""
  category: drupal
---

# Drupal JSON:API

Comprehensive guide for working with Drupal's JSON:API module (core) and JSON:API Extras (contrib). Covers spec-compliant REST API with filtering, includes, pagination, and customization.

## I need to...

### Get Started

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what JSON:API is and when to use it | [What is JSON:API](what-is-jsonapi.md) | Understanding JSON:API's purpose helps determine if it fits your project requirements. JSON:API is a spec-compliant implementation built into Drupal core since 8.7. |
| Decide between JSON:API vs REST vs GraphQL | [JSON:API vs REST vs GraphQL](jsonapi-vs-rest-vs-graphql.md) | Choose the right API approach based on your project's requirements and constraints. |
| Understand the core architecture and components | [Core Architecture](core-architecture.md) | Understanding the architecture is essential when customizing JSON:API behavior, debugging issues, or extending functionality. |

### Work with Resources

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand URL structure and resource types | [URL Structure & Resource Types](url-structure-resource-types.md) | Understanding URL patterns and resource type naming is fundamental for all API operations. |
| Fetch data with GET requests | [Fetching Resources (GET)](fetching-resources.md) | Retrieving entity data from Drupal. Applies to collections (multiple entities) and individual entities. |
| Filter results by field values, operators, or groups | [Filtering](filtering.md) | Narrow down collection results based on field values. Essential for search, listing published content, filtering by author, date ranges, and complex queries. |
| Include related resources and limit response fields | [Includes & Sparse Fieldsets](includes-sparse-fieldsets.md) | **Includes:** Fetch related entities in a single request (compound documents). Reduces HTTP round trips. |
| Sort results and paginate collections | [Sorting & Pagination](sorting-pagination.md) | **Sorting:** Control result order. Essential for chronological listings, alphabetical lists, and custom ordering. |

### Modify Data

| I need to... | Guide |
|--------------|-------|
| Create resources with POST requests | [Creating Resources (POST)](creating-resources.md) |
| Update resources with PATCH requests | [Updating Resources (PATCH)](updating-resources.md) |
| Delete resources | [Deleting Resources (DELETE)](deleting-resources.md) |
| Upload files (images, documents) | [File Uploads](file-uploads.md) |

### Secure and Customize

| I need to... | Guide |
|--------------|-------|
| Set up authentication (Basic, Cookie, OAuth2, JWT) | [Authentication Patterns](authentication-patterns.md) |
| Apply security best practices for production | [Security Best Practices](security-best-practices.md) |
| Customize resource names, URLs, and field visibility | [JSON:API Extras Customization](jsonapi-extras-customization.md) |
| Transform field values with enhancers | [Field Enhancers](field-enhancers.md) |

### Optimize and Extend

| I need to... | Guide |
|--------------|-------|
| Improve API performance (caching, CDN, sparse fields) | [Performance Optimization](performance-optimization.md) |
| Work with revisions and translations | [Revisions & Translations](revisions-translations.md) |
| Find key source code files for debugging | [Code Reference Map](code-reference-map.md) |
| Test and debug JSON:API implementations | [Testing & Debugging](testing-debugging.md) |

### Reference

| I need to... | Guide |
|--------------|-------|
| Check guide sources and maintenance info | [Sources & Maintenance](sources-maintenance.md) |
