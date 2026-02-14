---
description: Preventing SQL injection using Database API placeholders, Entity Query, Query Builder, and safe identifier escaping.
---

# SQL Injection Prevention

## When to Use
Every database query -- SQL injection allows attackers to manipulate queries and access/modify unauthorized data.

## Steps
1. **Use Database API with placeholders (ALWAYS)**
   ```php
   // CORRECT: Parameterized query
   $database = \Drupal::database();
   $result = $database->query(
     'SELECT title FROM {node_field_data} WHERE nid = :nid',
     [':nid' => $nid]
   );

   // WRONG: String concatenation
   $result = $database->query(
     "SELECT title FROM {node_field_data} WHERE nid = " . $nid
   );  // SQL INJECTION VULNERABILITY
   ```

2. **Use Entity Query for entity data**
   ```php
   // Preferred: Entity Query (higher-level, safer)
   $nids = \Drupal::entityQuery('node')
     ->accessCheck(TRUE)
     ->condition('type', 'article')
     ->condition('title', $search, 'CONTAINS')  // Automatically safe
     ->execute();
   ```

3. **For table/column names, use escapeTable/escapeField**
   ```php
   // Placeholders DON'T work for identifiers
   $table = $database->escapeTable($table_name);
   $field = $database->escapeField($field_name);
   $query = $database->query("SELECT $field FROM {" . $table . "}");
   ```

4. **Array placeholders for IN clauses**
   ```php
   // Drupal expands arrays automatically
   $nids = [1, 2, 3, 4];
   $result = $database->query(
     'SELECT title FROM {node_field_data} WHERE nid IN (:nids[])',
     [':nids[]' => $nids]
   );
   // Expands to: WHERE nid IN (:nids_0, :nids_1, :nids_2, :nids_3)
   ```

5. **Use Query Builder for complex queries**
   ```php
   $query = $database->select('node_field_data', 'n');
   $query->fields('n', ['nid', 'title']);
   $query->condition('type', 'article');
   $query->condition('status', 1);
   $query->range(0, 10);
   $result = $query->execute();
   // All values automatically parameterized
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Querying | Entity data | Use Entity Query (highest level) |
| Querying | Custom table data | Use Database API with placeholders |
| Querying | Complex joins/subqueries | Use Query Builder (select/insert/update objects) |
| Values | User input in WHERE/SET | Use placeholders (`:name`, `:value`) |
| Identifiers | Table/column names from input | Use `escapeTable()` / `escapeField()` |
| Raw SQL needed | No alternative exists | Extreme scrutiny, code review, document why |

## Common Mistakes
- String concatenation in queries -- **CRITICAL VULNERABILITY**: `"WHERE id = " . $_GET['id']`
- Using placeholders for table names -- Won't work; use `escapeTable()`
- Trusting input because "it's validated" -- Always use placeholders regardless
- Direct PDO usage bypassing Database API -- Loses Drupal's automatic protection
- Using `db_query()` in D7 without placeholders -- D7 EOL Jan 2025, but legacy code exists
- Not using `->accessCheck(TRUE)` on Entity Query -- Different vulnerability (access bypass)

## See Also
- Reference: `/core/lib/Drupal/Core/Database/Connection.php`
- Reference: https://www.drupal.org/docs/develop/drupal-apis/database-api/static-queries
