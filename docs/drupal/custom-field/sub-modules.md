---
description: Nine sub-modules for GraphQL, JSON:API, Entity Browser, Linkit, Media Library, Search API, Viewfield, SDC rendering, and AI integration.
tldr: "You need extended functionality like GraphQL, JSON:API normalization, Entity Browser, Linkit, Media Library, Search API, Single Directory Component rendering, or AI integration. Nine sub-modules ship with 5.x."
---

# Sub-Modules

## When to Use

You need extended functionality like GraphQL, JSON:API normalization, Entity Browser, Linkit, Media Library, Search API, Single Directory Component rendering, or AI integration. Nine sub-modules ship with 5.x.

All sub-modules declare `core_version_requirement: ^11.4 || ^12` in 5.x.

## custom_field_graphql

GraphQL Compose integration with 11 schema type plugins.

- **Dependencies:** `graphql_compose` -- unversioned in `.info.yml`; upstream tests against `2.4.x-dev`
- **Schema types:** CustomFieldType, CustomFieldImage, CustomFieldFile, CustomFieldEntityReference, CustomFieldLinkType, CustomFieldUriType, CustomFieldLinkAttributesType, CustomFieldDateRange, CustomFieldTimeRange, CustomFieldViewfield, CustomFieldViewfieldSchemaExtension
- Exposes custom fields to GraphQL API automatically

## custom_field_jsonapi

JSON:API normalizers for custom field types.

- **Dependencies:** jsonapi (core)
- **Normalizers:** 6 classes -- DateRange, DateTime, EntityReference, StringLong, TimeRange, Uri
- Automatically normalizes custom field data in JSON:API responses

## custom_field_entity_browser

Entity Browser widget for entity reference columns.

- **Dependencies:** entity_browser
- **Plugin:** EntityReferenceBrowserWidget
- Visual entity browser instead of autocomplete for entity reference columns

## custom_field_linkit

Linkit autocomplete widgets for link and uri columns.

- **Dependencies:** `linkit:linkit`, unversioned in `.info.yml`; `composer.json` require-dev pins `^7` only -- 6.x support was dropped
- **Plugins:** LinkitWidget, LinkitUrlWidget, plus the LinkitFormatter and LinkitUrlFormatter sub-field formatters
- Linkit autocomplete for internal link selection in link columns, and matching output formatters

## custom_field_media

Media library widget for image columns.

- **Dependencies:** `drupal:media_library` (core) -- the media_library module, not `media` alone
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

- **Dependencies:** `ai:ai (>= 1.3)` in `.info.yml`; require-dev `^1.3`
- AI-powered field processing

## custom_field_sdc

Renders a custom field through a Single Directory Component.

- **Dependencies:** none beyond core SDC
- **Plugin:** the `custom_field_sdc` field-level formatter (`SingleDirectoryComponentFormatter`), which fills component slots and props from sub-fields of any type via `#[PropWidget]` plugins
- An alternative to the `sdc_display` contrib module for component-driven output of compound fields

## Common Mistakes

- **Enabling unnecessary sub-modules** -- Only enable modules for integrations you actually use
- **Not configuring Linkit profiles** -- LinkitWidget requires configured Linkit profile to work
- **Expecting auto-indexing** -- Search API sub-module provides types; you must configure index fields

## See Also

- Reference: `/modules/contrib/custom_field/modules/`
- GraphQL Compose: https://www.drupal.org/project/graphql_compose
