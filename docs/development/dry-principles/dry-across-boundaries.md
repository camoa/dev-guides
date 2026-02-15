---
description: Handling knowledge duplication across microservices, frontend/backend, multiple languages, and separate repositories
---

# DRY Across Boundaries

## When to Use

When dealing with knowledge duplication across system boundaries: microservices, frontend/backend, multiple programming languages, or separate repositories.

## Decision Framework

| Boundary Type | DRY Approach | Implementation |
|---------------|--------------|----------------|
| **Frontend <-> Backend** | Shared schema/types | GraphQL schema, tRPC, Protocol Buffers, OpenAPI codegen |
| **Multiple microservices** | Shared contracts | API specs, event schemas, shared libraries (carefully) |
| **Multiple languages** | Code generation | Protocol Buffers, OpenAPI Generator, GraphQL Codegen |
| **Multiple repos** | Shared packages | npm packages, PyPI, Maven Central (versioned) |
| **Database <-> Code** | Schema-driven | ORM models, migrations, codegen from schema |
| **Mobile <-> Backend** | API contracts | OpenAPI/Swagger, GraphQL, REST with typed clients |

## Pattern: Schema-Driven Development

```protobuf
// SINGLE SOURCE: Protocol Buffers schema
syntax = "proto3";

message User {
  int32 id = 1;
  string email = 2;
  string name = 3;
  UserType type = 4;
}

enum UserType {
  REGULAR = 0;
  VIP = 1;
  GOLD = 2;
}

service UserService {
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc GetUser(GetUserRequest) returns (User);
}

// GENERATED CODE (never hand-written):
// - user_pb2.py (Python)
// - user.pb.go (Go)
// - user_pb.ts (TypeScript)
// - User.java (Java)

// All languages now share exact same schema
// Type safety across boundaries
```

## Pattern: API Contract Sharing (OpenAPI)

```yaml
# openapi.yml — Single source of truth
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0

paths:
  /users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      required: [id, email, name]
      properties:
        id: { type: integer }
        email: { type: string, format: email }
        name: { type: string }
        type: { type: string, enum: [regular, vip, gold] }
```

```bash
# Generate client SDKs from OpenAPI spec
npx openapi-generator-cli generate \
  -i openapi.yml \
  -g typescript-fetch \
  -o ./frontend/src/api

npx openapi-generator-cli generate \
  -i openapi.yml \
  -g python \
  -o ./mobile-app/api

# Frontend and mobile now have type-safe clients
# Schema lives in ONE place
```

## Pattern: Shared Validation Logic

```typescript
// PROBLEM: Validation duplicated frontend/backend

// Frontend (JavaScript)
if (password.length < 8) {
  throw new Error('Password too short');
}

// Backend (Python)
if len(password) < 8:
    raise ValidationError('Password too short')

// SOLUTION: Shared schema
// schema.zod.ts (shared package)
import { z } from 'zod';

export const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(1),
});

export type CreateUserData = z.infer<typeof CreateUserSchema>;

// Frontend uses directly
import { CreateUserSchema } from '@company/shared-schemas';

const data = CreateUserSchema.parse(formData);

// Backend: Convert Zod schema to JSON Schema, use in Python
// (via build step that generates JSON Schema -> Python Pydantic models)
```

## Pattern: Monorepo with Shared Packages

```
# Repository structure
monorepo/
  packages/
    schemas/          # Shared schemas (Zod, JSON Schema, Protocol Buffers)
    types/            # Shared TypeScript types
    validation/       # Shared validation utilities
  apps/
    web-frontend/     # Imports from packages/
    mobile-app/       # Imports from packages/
    backend-api/      # Imports from packages/
  package.json

# All apps import shared packages
# Single source of truth for schemas and types
# No duplication across boundaries
```

## When Duplication Across Boundaries is OK

| Scenario | Why Duplication is Acceptable |
|----------|------------------------------|
| **Microservices with different domains** | Services should be independently deployable; shared libraries create coupling |
| **Different security contexts** | Backend validation is authoritative; frontend validation is UX convenience |
| **Performance-critical paths** | Optimized implementations may differ even with same contract |
| **Legacy integration** | Bridging old and new systems; duplication temporary during migration |

## Common Mistakes

- **Shared code libraries across microservices** — Creates coupling, breaks independent deployability
- **Frontend validation without backend validation** — Security vulnerability; frontend is advisory only
- **Manual synchronization of types** — Guaranteed drift; always use code generation
- **Tightly coupling services through shared database** — Violates service boundaries; use event schemas instead
- **No versioning on shared contracts** — Breaking changes propagate uncontrollably

## See Also

- [Knowledge Duplication](knowledge-duplication.md)
- [DRY in Configuration](dry-in-configuration.md)
- [Protocol Buffers](https://protobuf.dev/)
- [OpenAPI Generator](https://openapi-generator.tech/)
