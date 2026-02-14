---
description: Protecting state-changing operations from Cross-Site Request Forgery using Form API tokens, route-level CSRF, and AJAX token headers.
---

# CSRF Protection

## When to Use
Protecting state-changing operations (create, update, delete) from Cross-Site Request Forgery attacks where malicious sites trick users into performing unwanted actions.

## Steps
1. **Form API (automatic protection)**
   ```php
   // Forms automatically include CSRF token
   public function buildForm(array $form, FormStateInterface $form_state) {
     $form['title'] = ['#type' => 'textfield', '#title' => 'Title'];
     $form['submit'] = ['#type' => 'submit', '#value' => 'Save'];
     return $form;
     // Form API adds hidden 'form_token' field automatically
   }
   ```

2. **Route-level CSRF for non-form operations**
   ```yaml
   # mymodule.routing.yml
   mymodule.delete_item:
     path: '/item/{id}/delete'
     defaults:
       _controller: '\Drupal\mymodule\Controller\ItemController::delete'
     requirements:
       _csrf_token: 'TRUE'  # Requires valid token in query string
   ```

3. **Generate CSRF-protected URLs**
   ```php
   use Drupal\Core\Url;

   $url = Url::fromRoute('mymodule.delete_item', ['id' => $item_id]);
   // Token automatically added to URL when route has _csrf_token requirement

   // In Twig
   {{ link('Delete', 'mymodule.delete_item', {'id': item.id}) }}
   // Renders: /item/123/delete?token=abc123...
   ```

4. **Manual token validation (rare)**
   ```php
   $csrf_token = \Drupal::service('csrf_token');

   // Generate token
   $token = $csrf_token->get('action_name');

   // Validate token
   if (!$csrf_token->validate($token, 'action_name')) {
     throw new AccessDeniedHttpException();
   }
   ```

5. **AJAX with CSRF protection**
   ```javascript
   // Get session token for AJAX
   fetch('/session/token')
     .then(response => response.text())
     .then(token => {
       fetch('/api/endpoint', {
         headers: {
           'X-CSRF-Token': token
         }
       });
     });
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Implementation | Using Form API | CSRF automatic, do nothing |
| Implementation | Non-form route changing state | Add `_csrf_token: 'TRUE'` to requirements |
| Implementation | REST/JSON API endpoint | Use `CsrfRequestHeaderAccessCheck` |
| Link generation | CSRF-protected route | Use `Url::fromRoute()`, token added automatically |
| Anonymous users | Need CSRF on public forms | See contrib module `anonymous_token` |

## Common Mistakes
- GET requests changing state -- Use POST/DELETE; GET should be idempotent
- No CSRF on destructive routes -- **CRITICAL**: Users can be tricked into deleting data
- Disabling form token validation -- Never use `#token => FALSE` unless purely informational form
- Not validating token value -- If manually generating, must manually validate
- Forgetting anonymous users have no session -- CSRF checks fail for anonymous by default

## See Also
- Reference: `/core/lib/Drupal/Core/Access/CsrfTokenGenerator.php`
- Reference: `/core/lib/Drupal/Core/Access/CsrfAccessCheck.php`
- Reference: https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes/csrf-access-checking
