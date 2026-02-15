---
description: Eight sub-modules for GraphQL, JSON API, Entity Browser, Linkit, Media Library, Search API, Viewfield, and AI integration.
---

# Sub-Modules

## When to Use

You need extended functionality like GraphQL, JSON:API normalization, Entity Browser, Linkit, Media Library, Search API, or AI integration.

## custom_field_graphql

GraphQL Compose integration with 11 schema type plugins.

- **Dependencies:** graphql_compose ^2.2
- **Schema types:** CustomFieldType, CustomFieldImage, CustomFieldFile, CustomFieldEntityReference, CustomFieldLinkType, CustomFieldUriType, CustomFieldLinkAttributesType, CustomFieldDateRange, CustomFieldTimeRange, CustomFieldViewfield, CustomFieldViewfieldSchemaExtension
- Exposes custom fields to GraphQL API automatically

## custom_field_jsonapi

JSON:API normalizers for custom field types.

- **Dependencies:** jsonapi (core)
- **Normalizers:** 5 classes for proper JSON:API serialization
- Automatically normalizes custom field data in JSON:API responses

## custom_field_entity_browser

Entity Browser widget for entity reference columns.

- **Dependencies:** entity_browser
- **Plugin:** EntityReferenceBrowserWidget
- Visual entity browser instead of autocomplete for entity reference columns

## custom_field_linkit

Linkit autocomplete widgets for link and uri columns.

- **Dependencies:** linkit ^6.1 || ^7
- **Plugins:** LinkitWidget, LinkitUrlWidget
- Linkit autocomplete for internal link selection in link columns

## custom_field_media

Media library widget for image columns.

- **Dependencies:** media (core)
- Select existing media entities instead of direct file upload

## custom_field_search_api

Search API integration.

- **Dependencies:** search_api
- Index and search custom field columns

## custom_field_viewfield

Viewfield type for embedding views in custom fields.

- **Dependencies:** None
- **Type:** viewfield (embed view displays)
- **Extended properties:** `field__display`, `field__arguments`, `field__items`

## custom_field_ai

AI module integration.

- **Dependencies:** ai ^1.2
- AI-powered field processing

## Common Mistakes

- **Enabling unnecessary sub-modules** -- Only enable modules for integrations you actually use
- **Not configuring Linkit profiles** -- LinkitWidget requires configured Linkit profile to work
- **Expecting auto-indexing** -- Search API sub-module provides types; you must configure index fields

## See Also

- Reference: `/modules/contrib/custom_field/modules/`
- GraphQL Compose: https://www.drupal.org/project/graphql_compose
