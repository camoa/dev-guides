---
description: Declaring trusted callbacks for render arrays using TrustedCallbackInterface and the TrustedCallback attribute to prevent arbitrary code execution.
---

# Trusted Callbacks

## When to Use
When using callbacks in render arrays (`#pre_render`, `#post_render`, `#lazy_builder`) -- Drupal requires explicit trust declaration to prevent arbitrary code execution.

## Steps
1. **Implement TrustedCallbackInterface**
   ```php
   namespace Drupal\mymodule;

   use Drupal\Core\Security\TrustedCallbackInterface;

   class MyRenderer implements TrustedCallbackInterface {

     public static function trustedCallbacks() {
       // List methods that can be used as callbacks
       return ['preRender', 'lazyBuild'];
     }

     public static function preRender(array $element) {
       // Safe to use as #pre_render
       $element['#markup'] = '<div>Rendered</div>';
       return $element;
     }

     public static function lazyBuild($arg1, $arg2) {
       // Safe to use as #lazy_builder
       return [
         '#markup' => "Built with $arg1, $arg2",
       ];
     }
   }
   ```

2. **Use in render arrays**
   ```php
   $build = [
     '#type' => 'container',
     '#pre_render' => [
       [MyRenderer::class, 'preRender'],
     ],
   ];

   // Or lazy builder
   $build = [
     '#lazy_builder' => [MyRenderer::class . '::lazyBuild', ['arg1', 'arg2']],
     '#create_placeholder' => TRUE,
   ];
   ```

3. **Use TrustedCallback attribute (alternative)**
   ```php
   use Drupal\Core\Security\Attribute\TrustedCallback;

   class MyRenderer {

     #[TrustedCallback]
     public static function preRender(array $element) {
       // Marked as trusted via attribute
       return $element;
     }
   }
   ```

4. **For service callbacks**
   ```php
   // If callback is a service method, implement interface on service
   class MyService implements TrustedCallbackInterface {
     public static function trustedCallbacks() {
       return ['buildContent'];
     }

     public function buildContent() {
       return ['#markup' => 'Content'];
     }
   }
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Callback type | Static method | Implement `TrustedCallbackInterface` on class |
| Callback type | Service method | Implement interface on service class |
| Callback type | Anonymous function | Automatically trusted (use sparingly) |
| Drupal version | D10+ | Prefer `#[TrustedCallback]` attribute |
| Drupal version | D9 | Use `trustedCallbacks()` method |

## Common Mistakes
- Not declaring callbacks as trusted -- Exception thrown: "Untrusted callback"
- Listing ALL methods in trustedCallbacks() -- Only list actual callbacks
- Using arbitrary user input in callbacks -- Still must validate, trust does not equal safety
- Forgetting to update trustedCallbacks() when adding methods -- New callbacks break
- Using `#markup` with callback instead of returning render array -- Callback should return array

## See Also
- Reference: `/core/lib/Drupal/Core/Security/TrustedCallbackInterface.php`
- Reference: `/core/lib/Drupal/Core/Security/DoTrustedCallbackTrait.php`
- Reference: https://www.drupal.org/node/2966725 (Trusted callback change record)
