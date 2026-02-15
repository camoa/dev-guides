---
description: Applying SOLID principles to microservices, component-based frontends, API design, and event-driven architecture.
---

# SOLID in Modern Architecture

## When to Apply SOLID Architecturally

SOLID principles extend beyond class design to:
- Microservices architecture
- Component-based frontend frameworks
- API design
- Module/package boundaries

## Pattern: SOLID in Microservices

**SRP in Services**:
- Each microservice has one business capability
- User Service handles users, Order Service handles orders
- Violation: "UserOrderPaymentService" doing three things

**OCP in Service Extension**:
- Add new services without modifying existing services
- Event-driven architecture: new services subscribe to events
- Violation: Modifying checkout service for every new payment method

**LSP in Service Contracts**:
- Services implementing same contract are substitutable
- Multiple payment services behind `IPaymentService` contract
- Violation: StripeService throws exceptions that PayPalService doesn't

**ISP in API Design**:
- BFF (Backend for Frontend) pattern: tailored APIs per client
- Mobile API vs Web API vs Admin API
- Violation: Single monolithic API forcing mobile to fetch unused data

**DIP in Service Dependencies**:
- Services depend on abstractions (message queues, service registries)
- Not coupled to specific infrastructure (RabbitMQ vs Kafka)
- Violation: Service hardcoded to RabbitMQ client

## Pattern: SOLID in Component Architecture

**React/Vue Example** (TypeScript):
```typescript
// SRP: One component, one responsibility
const UserProfile = ({ user }: { user: User }) => {
  return <div>{user.name}</div>;
};

const UserAvatar = ({ user }: { user: User }) => {
  return <img src={user.avatar} />;
};

// Not: UserProfileAndAvatarAndSettings component

// OCP: Extend via composition
const Button = ({ children, onClick }: ButtonProps) => {
  return <button onClick={onClick}>{children}</button>;
};

const IconButton = ({ icon, ...props }: IconButtonProps) => {
  return <Button {...props}><Icon name={icon} /></Button>;
};

// ISP: Specific prop interfaces
interface ClickableProps {
  onClick: () => void;
}

interface DisableableProps {
  disabled?: boolean;
}

// Components use only what they need
const SubmitButton = ({ onClick, disabled }: ClickableProps & DisableableProps) => {
  // ...
};

// DIP: Depend on abstractions (hooks, contexts)
const useAuth = (): IAuthService => {
  return useContext(AuthContext); // Abstract interface
};

const LoginForm = () => {
  const auth = useAuth(); // Depends on IAuthService, not concrete implementation
  // ...
};
```

## Pattern: SOLID in API Design

**RESTful API with SOLID**:

**SRP**: One resource per endpoint
```
GET  /users      -> UserController::index()
POST /orders     -> OrderController::create()
```

**ISP**: Resource-specific responses
```json
// Mobile client (minimal payload)
GET /users/123?fields=id,name

// Web client (full data)
GET /users/123?fields=id,name,email,address,preferences
```

**DIP**: Controllers depend on services, not repositories directly
```php
class UserController {
    public function __construct(private IUserService $userService) {}

    public function show($id) {
        return $this->userService->getUserById($id);
    }
}
```

## Decision: SOLID Across Architectural Layers

| Layer | SOLID Application | Example |
|---|---|---|
| **Presentation** | SRP: One view per use case | LoginView, DashboardView (not LoginAndDashboardView) |
| **Application** | OCP: Use cases extensible via composition | AddPaymentMethodUseCase extends CheckoutUseCase |
| **Domain** | LSP: Entities substitutable | PremiumUser substitutes User |
| **Infrastructure** | DIP: Implementations depend on domain interfaces | MySQLUserRepository implements IUserRepository (domain interface) |

## Pattern: Event-Driven Architecture as OCP

**Node.js/TypeScript Example**:
```typescript
// Core system closed for modification
class EventBus {
  private handlers = new Map<string, Array<(event: any) => void>>();

  subscribe(eventType: string, handler: (event: any) => void) {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, []);
    }
    this.handlers.get(eventType)!.push(handler);
  }

  publish(eventType: string, event: any) {
    this.handlers.get(eventType)?.forEach(handler => handler(event));
  }
}

// Open for extension: add handlers without modifying EventBus
const bus = new EventBus();

bus.subscribe('user.registered', (event) => {
  sendWelcomeEmail(event.user);
});

bus.subscribe('user.registered', (event) => {
  logAnalytics(event.user);
});

bus.subscribe('user.registered', (event) => {
  updateCRM(event.user);
});

// Adding new handler doesn't change existing code
bus.subscribe('user.registered', (event) => {
  sendSlackNotification(event.user);
});
```

## Common Mistakes

- **Microservices per database table** -- Violates SRP (too granular). Why: creates distributed monolith
- **Shared database between services** -- Violates DIP. Why: tight coupling through schema
- **God services** -- "CoreBusinessService" doing everything. Why: violates SRP
- **Breaking contracts between services** -- LSP violation. Why: upstream consumers break
- **Monolithic APIs** -- Forcing mobile to fetch desktop-level data. Why: violates ISP
- **Framework coupling in domain** -- Domain entities importing ORM annotations. Why: violates DIP
