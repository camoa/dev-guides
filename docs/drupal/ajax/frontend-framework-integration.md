---
description: Integrate React, Vue, or other frontend frameworks with Drupal AJAX endpoints using JSON responses and Drupal.behaviors
drupal_version: "11.x"
---

# Frontend Framework Integration

## When to Use

> Use JSON endpoints with React/Vue for fully decoupled sites. Use Drupal AJAX for simple enhancements. Choose one approach per feature — don't mix Drupal AJAX and framework AJAX for the same interaction.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Full decoupling | JSON:API + custom AJAX endpoints | React/Vue handle all rendering, Drupal is API only |
| Progressive decoupling | Drupal AJAX + framework components | Server renders initial page, JavaScript enhances |
| Simple enhancements | Drupal AJAX only | No framework overhead, faster initial load |

## Pattern

**PHP JSON endpoint:**

```php
class ApiController extends ControllerBase {
  public function getData(Request $request) {
    $items = $this->loadItems();
    $data = array_map(fn($item) => [
      'id' => $item->id(),
      'title' => $item->label(),
      'body' => $item->get('body')->value,
    ], $items);

    return new JsonResponse(['data' => $data]);
  }
}
```

**React component consuming endpoint:**

```javascript
// js/components/ItemList.jsx
function ItemList() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    fetch('/my-module/api/items')
      .then(r => r.json())
      .then(data => setItems(data.data));
  }, []);
  return <ul>{items.map(i => <li key={i.id}>{i.title}</li>)}</ul>;
}

// Attach React component via Drupal.behaviors
(function (Drupal, React, ReactDOM) {
  Drupal.behaviors.reactItemList = {
    attach(context) {
      const el = document.getElementById('react-item-list');
      if (el && !el.hasAttribute('data-react-initialized')) {
        ReactDOM.render(<ItemList />, el);
        el.setAttribute('data-react-initialized', 'true');
      }
    }
  };
})(Drupal, React, ReactDOM);
```

Reference: `core/modules/jsonapi/` (JSON:API module)

## Common Mistakes

- **Wrong**: Not protecting API endpoints → **Right**: Add authentication and CSRF protection for all data-changing endpoints
- **Wrong**: Returning too much data → **Right**: Serialize only needed fields; avoid loading entire entity graphs
- **Wrong**: Not handling CORS → **Right**: Configure CORS headers for cross-origin requests in services.yml
- **Wrong**: Using both Drupal AJAX and framework AJAX for the same feature → **Right**: Choose one approach per interaction
- **Wrong**: Rebuilding JSON:API for standard entities → **Right**: Use JSON:API module; don't reinvent a standards-compliant API

## See Also

- [Testing AJAX](testing-ajax.md)
- [Best Practices: Security](best-practices-security.md)
- Reference: [Decoupled Drupal documentation](https://www.drupal.org/docs/develop/decoupled-drupal)
