---
description: Integrate React, Vue, or other frontend frameworks with Drupal AJAX endpoints using JSON responses and Drupal.behaviors
tldr: "Use JSON endpoints with React/Vue for fully decoupled sites. Use Drupal AJAX for simple enhancements."
drupal_version: "11.x"
---

# Frontend Framework Integration

## When to Use

You're building a decoupled or progressively decoupled Drupal site with React, Vue, or other JavaScript frameworks consuming AJAX endpoints.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Full decoupling | JSON:API + custom AJAX endpoints | React/Vue handle all rendering, Drupal is API only |
| Progressive decoupling | Drupal AJAX + framework components | Server renders initial page, JavaScript enhances |
| Simple enhancements | Drupal AJAX only | No framework overhead, faster initial load |

## Pattern

```php
// JSON endpoint for frontend frameworks
namespace Drupal\my_module\Controller;

use Drupal\Core\Controller\ControllerBase;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;

class ApiController extends ControllerBase {
  public function getData(Request $request) {
    $items = $this->loadItems();

    $data = array_map(function($item) {
      return [
        'id' => $item->id(),
        'title' => $item->label(),
        'body' => $item->get('body')->value,
        'created' => $item->getCreatedTime(),
      ];
    }, $items);

    return new JsonResponse(['data' => $data]);
  }
}
```

```javascript
// React component consuming endpoint
// js/components/ItemList.jsx
import React, { useState, useEffect } from 'react';

function ItemList() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/my-module/api/items')
      .then(response => response.json())
      .then(data => {
        setItems(data.data);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.title}</li>
      ))}
    </ul>
  );
}

export default ItemList;

// Attach React component to Drupal page
// js/init-react.js
(function (Drupal, React, ReactDOM) {
  Drupal.behaviors.reactItemList = {
    attach: function (context, settings) {
      const container = document.getElementById('react-item-list');
      if (container && !container.hasAttribute('data-react-initialized')) {
        ReactDOM.render(<ItemList />, container);
        container.setAttribute('data-react-initialized', 'true');
      }
    }
  };
})(Drupal, React, ReactDOM);
```

Reference: `core/modules/jsonapi/` (JSON:API module)

## Common Mistakes

- Not protecting API endpoints → Add authentication/CSRF for all data-changing endpoints
- Returning too much data → Serialize only needed fields; avoid loading entire entity graphs
- Not handling CORS → Configure CORS headers for cross-origin requests in services.yml
- Duplicating Drupal AJAX → Choose Drupal AJAX OR framework AJAX, not both for same feature
- Not using JSON:API for standard entities → JSON:API provides optimized, standards-compliant API; don't reinvent

## See Also

- ← Previous: [Testing AJAX](testing-ajax.md) | Next: [Best Practices: Security](best-practices-security.md)
- Reference: [Decoupled Drupal documentation](https://www.drupal.org/docs/develop/decoupled-drupal)
