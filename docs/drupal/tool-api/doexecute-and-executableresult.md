---
description: "Write doExecute(), return an ExecutableResult success or failure, and pick the FailureCategory that tells callers whether to retry"
tldr: "doExecute() receives validated values and returns ExecutableResult::success() or failure() with a FailureCategory. Gotcha: failure() defaults to Input, which tells a model to retry; never return exception messages to callers."
drupal_version: "^10.5 || ^11"
---

# doExecute and ExecutableResult

## When to Use

> Use this when writing the body of a tool. `doExecute()` is the only abstract method on `ToolBase`; it receives resolved, validated values and returns an `ExecutableResult`.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Pattern

```php
use Drupal\tool\ExecutableResult;
use Drupal\tool\FailureCategory;

// tool 1.0.0-beta11 src/Tool/ToolBase.php
abstract protected function doExecute(array $values): ExecutableResult;

// tool 1.0.0-beta11 src/ExecutableResult.php
public static function success(TranslatableMarkup $message, ?array $context_values = []): static
public static function failure(TranslatableMarkup $message, ?array $context_values = [], FailureCategory $category = FailureCategory::Input): static
```

`$context_values` is keyed by output name. `ExecutableResult` is `final readonly`. Results are not cached by design: `ToolInterface` is "Deliberately not cacheable" ([#3582965](https://git.drupalcode.org/project/tool/-/work_items/3582965)). Cache inside `doExecute()` with Drupal's cache API when a `Read` tool is expensive, and give list tools paging inputs with `Range` constraints, as Tool Belt's `entity_list` does with `amount` and `offset`.

## Failure Categories

`FailureCategory` tells a caller whether retrying with different arguments can help (tool 1.0.0-beta11 `src/FailureCategory.php`).

| Case | Meaning | `isCorrectable()` |
|---|---|---|
| `Input` | Input values were invalid, missing or unsuitable | TRUE |
| `Access` | The user may not run the operation | FALSE |
| `Runtime` | Failed for a reason unrelated to the input | FALSE |

**`failure()` defaults to `Input`.** The AI connector attaches the input schema to correctable failures so the model retries (tool 1.0.0-beta11 `modules/tool_ai_connector/src/Plugin/AiFunctionCall/ToolPluginBase.php`).

## What Reaches the Caller When doExecute Throws

`execute()` catches every exception from `doExecute()` and value resolution (tool 1.0.0-beta11 `src/Tool/ToolBase.php`):

| `doExecute()` throws... | Caller sees | Category |
|---|---|---|
| `\InvalidArgumentException` or `InputException` | "Tool execution failed due to invalid input: " plus the exception message | `Input` |
| Anything else | "Tool execution failed: <class>. The full error has been logged." The detail goes to the `tool` log channel | `Runtime` |

The same `\InvalidArgumentException` path also catches input validation failures, because `getExecutableValues()` throws one with the violation list.

## Decision

| If... | Do... |
|---|---|
| The caller can fix it by changing arguments | `ExecutableResult::failure($msg)` (category `Input`) |
| The account lacks rights discovered late | `ExecutableResult::failure($msg, [], FailureCategory::Access)` |
| A service, network or bug failed | `ExecutableResult::failure($msg, [], FailureCategory::Runtime)` |
| You hit an unexpected exception | Let it propagate; `ToolBase` logs it and hides the detail |

## Common Mistakes

- Catching `\Exception` and returning `failure()` with `$e->getMessage()` → this sends internals (paths, SQL, service names) to an LLM or MCP client. The generated template (`src/Drush/Generators/tool.twig`) and several Tool Belt tools do this; curate the message
- Returning `failure()` for a runtime fault without a category → the default `Input` tells a model to retry with other arguments, wasting calls
- Reading `getResult()` before `execute()` → `\BadMethodCallException`; use `hasResult()` and `hasExecuted()`
- Putting internals in `context_values` on a failure → they never become typed outputs, but `getFormattedResult()` still carries them: Drush prints them and the AI connector returns them in `outputs` with `success: false`. Only the MCP bridge drops them (mcp_server_tool_bridge 1.0.0-beta3 `src/Plugin/mcp_server/Tool/ToolApi.php`)

## See Also

- [Output Definitions](output-definitions.md) → how values become outputs
- [Security Checklist](security-best-practices.md)
- Reference: `modules/contrib/tool/src/ExecutableResult.php`, `modules/contrib/tool/src/FailureCategory.php`, `modules/contrib/tool/src/Tool/ToolBase.php`
