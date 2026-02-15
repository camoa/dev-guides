---
description: Practical OCP patterns — plugin systems, middleware, data-driven configuration, and when to apply or skip OCP.
---

# OCP in Practice

## When to Apply OCP

Apply OCP when:
- You anticipate new variations of a concept (payment methods, exporters, validators)
- You're building a plugin system or framework
- Changes to existing code have high risk (production-critical systems)
- Multiple teams extend the same codebase

**Don't apply OCP when**:
- You have 1-2 stable variations unlikely to change
- The abstraction cost outweighs the extension benefit
- The domain is exploratory and requirements are unclear

## Pattern: Plugin Systems as OCP

**Python Plugin Example**:
```python
# Core system (closed for modification)
class PluginManager:
    def __init__(self):
        self.plugins = []

    def register(self, plugin: Plugin):
        self.plugins.append(plugin)

    def execute(self, data):
        for plugin in self.plugins:
            data = plugin.process(data)
        return data

# Extension point (open for extension)
class Plugin(ABC):
    @abstractmethod
    def process(self, data): pass

# New plugins extend without modifying core
class LoggingPlugin(Plugin):
    def process(self, data):
        log(data)
        return data

class ValidationPlugin(Plugin):
    def process(self, data):
        if not self.is_valid(data):
            raise ValidationError()
        return data
```

## Pattern: Middleware as OCP

**JavaScript/Express Example**:
```javascript
// Core pipeline (closed)
class Pipeline {
  constructor() {
    this.middlewares = [];
  }

  use(middleware) {
    this.middlewares.push(middleware);
    return this;
  }

  async execute(request) {
    let response = request;
    for (const mw of this.middlewares) {
      response = await mw(response);
    }
    return response;
  }
}

// Extensions (open)
const authMiddleware = async (req) => {
  if (!req.headers.auth) throw new AuthError();
  return req;
};

const loggingMiddleware = async (req) => {
  console.log(req);
  return req;
};

// Usage: no modification to Pipeline
const pipeline = new Pipeline()
  .use(loggingMiddleware)
  .use(authMiddleware);
```

## Decision: OCP Patterns by Use Case

| Use Case | Pattern | Example |
|---|---|---|
| Varying algorithms | Strategy | Payment methods, sorting algorithms |
| Adding features to objects | Decorator | Middleware, stream wrappers |
| Sequential processing | Chain of Responsibility | Validation chains, event handlers |
| Creating object variants | Factory + Polymorphism | Document exporters, database drivers |
| Extending behavior at runtime | Observer | Event systems, pub/sub |

## Data-Driven OCP

Instead of code changes, use configuration:

**PHP Example**:
```php
// Violation: hardcoded rules
class PriceCalculator {
  public function calculate($price, $country) {
    if ($country === 'US') return $price * 1.07;
    if ($country === 'CA') return $price * 1.13;
    // Requires code change for new country
  }
}

// OCP via configuration
class PriceCalculator {
  public function __construct(private array $taxRates) {}

  public function calculate($price, $country) {
    $rate = $this->taxRates[$country] ?? 0;
    return $price * (1 + $rate);
  }
}

// New countries: update config, not code
$calculator = new PriceCalculator([
  'US' => 0.07,
  'CA' => 0.13,
  'UK' => 0.20,
]);
```

## Common Mistakes

- **Creating interfaces with one implementation** -- Premature. Wait for the second variation. Why: speculative abstraction (YAGNI)
- **Abstract base classes doing too much** -- Base classes should define contracts, not behavior. Why: forces coupling to implementation details
- **Forgetting to close core logic** -- If adding extensions requires changing the manager/processor, OCP isn't achieved. Why: defeats the purpose
- **Over-reliance on inheritance** -- Prefer composition. Why: inheritance is tight coupling; composition is flexible
- **Not versioning extension points** -- In libraries, breaking interface changes break clients. Why: interfaces are contracts; changes require versioning

## Performance Considerations

**OCP Trade-offs**:
- Polymorphic dispatch has negligible cost in modern runtimes
- Plugin systems may have registration overhead
- Excessive indirection hurts readability more than performance

**Optimize when**: Profiling shows extension mechanism is a bottleneck (rare). Document trade-off.
