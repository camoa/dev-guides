---
description: "Scaffold a Tool API plugin and its tests with drush generate plugin:tool, then fix the generated access, outputs and catch block"
tldr: "Run drush generate plugin:tool to write the plugin plus unit and kernel tests. Gotcha: the generated checkAccess() throws LogicException until you define access, and the generated catch returns exception messages to callers."
drupal_version: "^10.5 || ^11"
---

# Scaffolding with drush generate

## When to Use

> Use this to start a new Tool API plugin. The generator writes the plugin and two tests, and its access check fails closed until you define one.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Steps

1. **Run the generator.** Name `plugin:tool`, alias `tool` (tool 1.0.0-beta11 `src/Drush/Generators/ToolGenerator.php`).

   ```bash
   drush generate plugin:tool
   ```

2. **Answer the prompts.** Module machine name, tool label, plugin ID, class (suffix `Tool`), description (required, no default), operation (default `Read`), and "Is the tool destructive (irreversible write/trigger)?" (default no).

3. **Review the three files it writes.**

   | File | Content |
   |---|---|
   | `src/Plugin/tool/Tool/{class}.php` | `#[Tool]` with one `example` string input and one `result` `MapOutputDefinition` |
   | `tests/src/Unit/Tool/{class}AccessTest.php` | Unit access test |
   | `tests/src/Kernel/Tool/{class}Test.php` | Kernel test |

4. **Define access.** The generated `checkAccess()` throws `\LogicException` ("Access control for %s has not been defined.") until you declare a `permission` and delete the override, or implement it. See [Access Control](access-control.md) for what that exception does to callers.

5. **Replace the example input and output.** The template comment says keys not in `output_definitions` "are dropped"; they are not typed outputs, but they still reach callers raw. See [Output Definitions](output-definitions.md).

6. **Fix the generated `catch (\Exception $e)`**, which returns `$e->getMessage()` to callers. See [doExecute and ExecutableResult](doexecute-and-executableresult.md).

7. **Rebuild and inspect.**

   ```bash
   drush cr
   drush tool:info my_module_my_tool --format=json
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Access | The rule depends only on the account | Add `permission:` and delete the `checkAccess()` override |
| Access | The rule depends on input values | Implement `checkAccess()` |
| Operation | The tool stores data | Pick `Write`, not the default `Read` |

## Common Mistakes

- Keeping the generic description → it is what agents read; the generator refuses a default for that reason
- Deleting the generated tests → they are the cheapest place to pin the access rule
- Leaving the default `Read` operation on a tool that writes → see [Operation and Destructive](operation-and-destructive.md)

## See Also

- [Defining a Tool](defining-a-tool.md) → the attribute in full
- [Access Control](access-control.md) → choosing `permission` vs `checkAccess()`
- Reference: `modules/contrib/tool/src/Drush/Generators/`
