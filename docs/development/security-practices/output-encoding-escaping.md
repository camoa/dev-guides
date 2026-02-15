---
description: Context-specific output escaping for HTML, JavaScript, URL, and CSS contexts, plus template engine auto-escaping behavior.
---

# Output Encoding and Escaping

## When to Use

Escape ALL output that includes untrusted data before rendering in HTML, JavaScript, CSS, URLs, SQL queries, OS commands, or any interpreter context. Different contexts require different escaping rules.

## Why Context Matters

**The same input needs different escaping based on WHERE it appears:**

```html
<!-- User input: <script>alert('XSS')</script> -->

<!-- HTML Context -->
<div>{{user_input}}</div>
<!-- Needs: &lt;script&gt;alert('XSS')&lt;/script&gt; -->

<!-- HTML Attribute Context -->
<div class="{{user_input}}">
<!-- Needs: different escaping - single quotes, double quotes, spaces matter -->

<!-- JavaScript Context -->
<script>var name = '{{user_input}}';</script>
<!-- Needs: JavaScript string escaping - different from HTML escaping -->

<!-- URL Context -->
<a href="/search?q={{user_input}}">
<!-- Needs: URL encoding - %3Cscript%3E... -->

<!-- CSS Context -->
<style>.{{user_input}} { color: red; }</style>
<!-- Needs: CSS escaping - different rules again -->
```

## Decision

| Output Context | Escaping Method | Characters to Escape |
|---|---|---|
| HTML body | HTML entity encoding | `< > & " '` |
| HTML attribute | HTML attribute encoding | `" ' < > &` + quote matching delimiter |
| JavaScript string | JavaScript escaping | `\ " ' \n \r` + control characters |
| JavaScript data | JSON.stringify() | Automatic safe encoding |
| URL parameter | URL encoding (percent encoding) | Non-alphanumeric characters |
| CSS value | CSS escaping | Hex escape sequences |
| SQL query | **Never escape manually** | Use parameterized queries |

## Pattern

**HTML context escaping:**

```python
import html

# Good: Escape for HTML context
def render_user_profile(username):
    safe_username = html.escape(username)
    return f"<h1>Welcome {safe_username}</h1>"

# Input: <script>alert('XSS')</script>
# Output: <h1>Welcome &lt;script&gt;alert('XSS')&lt;/script&gt;</h1>
```

**JavaScript context escaping:**

```javascript
// Good: Use JSON.stringify for data in JavaScript
function renderUser(user) {
    return `<script>
        const userData = ${JSON.stringify(user)};
        console.log(userData.name);
    </script>`;
}

// Bad: String concatenation
function renderUser_bad(user) {
    return `<script>
        const userName = '${user.name}';  // XSS if name contains '
    </script>`;
}
```

**URL context escaping:**

```php
// Good: URL encode query parameters
function buildSearchUrl(string $query): string {
    return '/search?q=' . urlencode($query);
}
```

**Multi-context escaping (dangerous):**

```html
<!-- VERY DANGEROUS: User input in JavaScript inside HTML attribute -->
<div onclick="handleClick('{{user_input}}')">Click me</div>

<!-- Better: Avoid multi-context entirely. Use data attributes + event listeners: -->
<div data-user-id="{{html_escaped_id}}" class="clickable">Click me</div>
<script>
    document.querySelectorAll('.clickable').forEach(el => {
        el.addEventListener('click', () => {
            handleClick(el.dataset.userId);  // Safe
        });
    });
</script>
```

## Template Engine Auto-Escaping

**Modern template engines escape by default:**

```python
# Jinja2 (Python) - auto-escapes HTML context
{{ user_input }}  # Automatically escaped
{{ user_input | safe }}  # Explicitly mark as safe (dangerous)

# Django template
{{ user_input }}  # Auto-escaped
{{ user_input | safe }}  # Bypass escaping (dangerous)
```

```javascript
// React JSX - auto-escapes
<div>{userInput}</div>  {/* Automatically escaped */}
<div dangerouslySetInnerHTML={{__html: userInput}} />  {/* Bypass - dangerous */}

// Vue.js
<div>{{ userInput }}</div>  <!-- Auto-escaped -->
<div v-html="userInput"></div>  <!-- Bypass - dangerous -->
```

**But template engines DON'T protect JavaScript/URL contexts:**

```jsx
// React - STILL VULNERABLE
<script>
    var userName = "{userInput}";  {/* Not escaped - XSS! */}
</script>

// Need manual escaping or JSON.stringify
<script>
    var userData = {JSON.stringify(userInput)};  {/* Safe */}
</script>
```

## Common Mistakes

- **Using same escaping for all contexts** — HTML escaping doesn't prevent XSS in JavaScript context. Each context needs specific escaping
- **Double encoding** — Escaping already-escaped data causes display bugs. Escape once at output time, not at input time
- **Encoding too early** — Encode at output, not input. Storing pre-encoded data in database causes issues when outputting to different contexts
- **Manual escaping when framework provides it** — Use your framework's built-in escaping. Don't reinvent the wheel with regex replacements
- **Trusting "safe" bypass mechanisms** — React's `dangerouslySetInnerHTML`, Django's `| safe`, Vue's `v-html` — these disable protection. Only use when HTML is from TRUSTED source
- **Not escaping in JSON API responses** — JSON APIs still need output escaping. Use `JSON.stringify()`, don't concatenate strings

## See Also

- Previous: [Input Validation](input-validation.md) | Next: [Cross-Site Scripting (XSS)](cross-site-scripting-xss.md)
- Reference: [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
