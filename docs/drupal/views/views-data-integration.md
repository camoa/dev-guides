## 28. Views Data Integration (hook_views_data)

### When to Use
Exposing custom database tables, altering entity views integration, defining custom handlers for existing fields, adding computed/pseudo-fields.

### Pattern: Basic Table Integration
```php
/**
 * Implements hook_views_data().
 */
function mymodule_views_data() {
  $data = [];

  $data['custom_table']['table']['group'] = t('Custom Data');
  $data['custom_table']['table']['base'] = [
    'field' => 'id',
    'title' => t('Custom Table'),
    'help' => t('Custom data table'),
  ];

  // Field definitions
  $data['custom_table']['id'] = [
    'title' => t('ID'),
    'field' => ['id' => 'numeric'],
    'sort' => ['id' => 'standard'],
    'filter' => ['id' => 'numeric'],
    'argument' => ['id' => 'numeric'],
  ];

  return $data;
}
```

### Handler Definitions by Type

#### Field Handler
```php
$data['custom_table']['name'] = [
  'title' => t('Name'),
  'help' => t('The name field'),
  'field' => [
    'id' => 'standard',  // Or custom handler ID
    'click sortable' => TRUE,
  ],
];
```

#### Filter Handler
```php
$data['custom_table']['status'] = [
  'title' => t('Status'),
  'filter' => [
    'id' => 'boolean',
    'label' => t('Active'),
    'type' => 'yes-no',
    'use_equal' => TRUE,
  ],
];
```

#### Sort Handler
```php
$data['custom_table']['created'] = [
  'title' => t('Created date'),
  'sort' => [
    'id' => 'date',
  ],
];
```

#### Argument (Contextual Filter)
```php
$data['custom_table']['id'] = [
  'argument' => [
    'id' => 'numeric',
    'name field' => 'name',  // Field to use for title
    'numeric' => TRUE,
  ],
];
```

#### Relationship
```php
$data['custom_table']['node_id'] = [
  'title' => t('Content'),
  'relationship' => [
    'id' => 'standard',
    'base' => 'node_field_data',
    'base field' => 'nid',
    'label' => t('Related content'),
  ],
];
```

### Pattern: Join to Existing Table
```php
function mymodule_views_data() {
  $data = [];

  // Define join FROM node_field_data TO custom_table
  $data['custom_table']['table']['join']['node_field_data'] = [
    'left_field' => 'nid',
    'field' => 'node_id',
  ];

  return $data;
}
```

### Pattern: Altering Entity Integration
```php
/**
 * Implements hook_views_data_alter().
 */
function mymodule_views_data_alter(&$data) {
  // Replace default handler with custom
  $data['node_field_data']['title']['field']['id'] = 'my_custom_field';

  // Add pseudo-field (computed, not in DB)
  $data['node_field_data']['custom_calculated'] = [
    'title' => t('Custom Calculation'),
    'field' => [
      'id' => 'my_custom_field',
      'real field' => 'nid',  // Actual DB field to add to query
    ],
  ];
}
```

### Common Definition Keys
| Key | Purpose | Example Values |
|-----|---------|----------------|
| id | Plugin ID | 'standard', 'numeric', 'boolean', 'my_custom_handler' |
| title | Admin UI label | t('Node ID') |
| help | Admin UI description | t('The unique node identifier') |
| real field | Actual DB column | 'nid' (when key name differs) |
| click sortable | Field supports click-sort | TRUE, FALSE |
| use_equal | Use = instead of <> | TRUE (performance optimization) |
| allow empty | Support NULL operators | TRUE (adds IS NULL, IS NOT NULL) |

### Common Mistakes
- Missing 'table']['base' for base tables → Views won't list table as queryable base
- Wrong handler ID → Use standard handlers ('numeric', 'string', 'boolean') unless custom needed
- Forgetting 'real field' for computed fields → Views needs to know which DB field to actually query
- Not defining all handler types → Fields without sort/filter definitions can't be sorted/filtered
- Missing join definitions → Related tables need join paths defined

### See Also
- Section 19-27: Plugin types that hook_views_data() references
- Reference: `core/modules/views/src/EntityViewsData.php` — entity integration base class
- Reference: `core/modules/node/src/NodeViewsData.php` — entity-specific customization example

