---
description: Practical ISP patterns — adapter pattern for third-party interfaces, interface inheritance, granularity decisions, and refactoring fat interfaces.
---

# ISP in Practice

## When to Split Interfaces

Split interfaces when:
- Clients implement methods with `throw new Error("Not supported")`
- Clients implement methods as no-ops or stubs
- Changes to interface affect clients that don't use the changed methods
- Interface has method groups used by different clients

**Don't split when**:
- All clients use all methods (cohesive interface)
- You have only one client (YAGNI)
- Methods are tightly related (single responsibility)

## Pattern: Adapter Pattern for ISP

When you can't change the fat interface (third-party library):

**Python Example**:
```python
# Third-party fat interface (can't modify)
class DatabaseConnection:
    def connect(self): pass
    def disconnect(self): pass
    def query(self, sql): pass
    def transaction_begin(self): pass
    def transaction_commit(self): pass
    def transaction_rollback(self): pass

# Your client only needs querying
class ReportGenerator:
    def __init__(self, db: DatabaseConnection):
        self.db = db  # Depends on entire fat interface

    def generate(self):
        return self.db.query("SELECT * FROM reports")

# ISP-Compliant: adapter with thin interface
class QueryInterface(ABC):
    @abstractmethod
    def query(self, sql): pass

class DatabaseQueryAdapter(QueryInterface):
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def query(self, sql):
        return self.connection.query(sql)

class ReportGenerator:
    def __init__(self, db: QueryInterface):  # Depends only on what it needs
        self.db = db

    def generate(self):
        return self.db.query("SELECT * FROM reports")
```

## Pattern: Interface Inheritance for Composition

**TypeScript Example**:
```typescript
// Base interface: minimal contract
interface Readable {
  read(): string;
}

// Extended interface: builds on base
interface Writable extends Readable {
  write(data: string): void;
}

// Further extended
interface Seekable extends Readable {
  seek(position: number): void;
}

// Clients choose the interface level they need
class FileReader implements Readable {
  read(): string { /* ... */ }
}

class FileEditor implements Writable {
  read(): string { /* ... */ }
  write(data: string): void { /* ... */ }
}

class RandomAccessFile implements Writable, Seekable {
  read(): string { /* ... */ }
  write(data: string): void { /* ... */ }
  seek(position: number): void { /* ... */ }
}
```

## Decision: Interface Granularity

| Interface Size | When to Use | Trade-off |
|---|---|---|
| Fine-grained (1-2 methods) | Highly varied client needs | More interfaces, more composition |
| Medium-grained (3-5 methods) | Common client patterns | Balance of cohesion and flexibility |
| Coarse-grained (6+ methods) | All clients need most methods | Fewer interfaces, less flexibility |

## Pattern: Refactoring Fat Interfaces

**Step 1: Identify Client Groups**
Group clients by which methods they use.

**Step 2: Extract Role Interfaces**
Create interfaces for each usage pattern.

**Step 3: Compose Interfaces**
Large interfaces can extend multiple role interfaces.

**Step 4: Update Clients**
Clients depend on role interfaces, not fat interface.

**JavaScript Example**:
```javascript
// Before: fat interface
class DataService {
  // CRUD operations
  create(data) { /* ... */ }
  read(id) { /* ... */ }
  update(id, data) { /* ... */ }
  delete(id) { /* ... */ }

  // Reporting
  generateReport() { /* ... */ }
  exportCSV() { /* ... */ }

  // Caching
  clearCache() { /* ... */ }
  warmCache() { /* ... */ }
}

// After: role interfaces
class ReadableDataService {
  read(id) { /* ... */ }
}

class WritableDataService extends ReadableDataService {
  create(data) { /* ... */ }
  update(id, data) { /* ... */ }
  delete(id) { /* ... */ }
}

class ReportingService {
  constructor(dataService) {
    this.dataService = dataService; // ReadableDataService
  }
  generateReport() { /* uses dataService.read() */ }
  exportCSV() { /* uses dataService.read() */ }
}

class CacheManager {
  clearCache() { /* ... */ }
  warmCache() { /* ... */ }
}
```

## Common Mistakes

- **Splitting every interface prematurely** -- Wait for actual varied client needs. Why: YAGNI, speculative design
- **Creating interfaces with one method** -- Sometimes valid, but often over-granular. Why: destroys cohesion
- **Not using interface inheritance** -- Duplicating method signatures across related interfaces. Why: maintenance nightmare
- **Forgetting the "client" in client-focused** -- Splitting by implementation convenience. Why: doesn't solve coupling problem
- **Breaking existing clients** -- Refactoring without adapters. Why: interface changes are breaking changes
- **Ignoring versioning** -- In libraries, interface changes break consumers. Why: interfaces are contracts

## ISP in Modern Architectures

**Microservices**: Each service exposes minimal API surface for its clients (API segregation).
**GraphQL**: Clients query exactly the fields they need (field-level segregation).
**REST**: Resource-specific endpoints rather than one endpoint doing everything (endpoint segregation).
