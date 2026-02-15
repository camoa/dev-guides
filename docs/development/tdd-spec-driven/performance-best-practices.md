---
description: Test suite speed targets, making tests fast, performance testing strategy, and identifying bottlenecks
---

# Performance Best Practices

## When to Use
Writing performance-critical code, optimizing slow tests, or ensuring your test suite runs fast enough to be run frequently.

## Test Suite Performance

**The 10-Second Rule**: Unit test suite should run in under 10 seconds for rapid feedback.

**Why Speed Matters**:
- Developers won't run slow tests frequently
- Slow tests break TDD flow (red-green-refactor cycle measured in minutes)
- CI/CD pipelines bottleneck on slow tests

**Speed Targets**:
- Unit test: < 10ms each
- Integration test: < 100ms each
- E2E test: < 5s each
- Full suite: < 2 minutes (for CI)

## Making Tests Fast

**Mock External Dependencies**
```python
# SLOW: Real HTTP call (200-1000ms)
def test_fetch_user_data():
    api = UserAPI()
    user = api.get_user(123)  # Real HTTP request
    assert user.name == 'Alice'

# FAST: Mocked HTTP (< 1ms)
def test_fetch_user_data():
    api = UserAPI()
    api.http_client = Mock()
    api.http_client.get.return_value = {'id': 123, 'name': 'Alice'}

    user = api.get_user(123)
    assert user.name == 'Alice'
```

**Use In-Memory Databases**
```javascript
// SLOW: Real PostgreSQL (50-200ms setup per test)
beforeEach(async () => {
  db = new PostgreSQL('localhost:5432');
  await db.connect();
  await db.migrate();
});

// FAST: In-memory SQLite (5-10ms setup per test)
beforeEach(() => {
  db = new SQLite(':memory:');
  db.migrate();
});
```

**Avoid Unnecessary I/O**
```java
// SLOW: Writing to disk
@Test
public void testFileProcessing() {
    File tempFile = new File("/tmp/test.txt");
    writeToFile(tempFile, "test data");

    String result = processor.process(tempFile);

    assertEquals("expected", result);
    tempFile.delete();
}

// FAST: In-memory
@Test
public void testFileProcessing() {
    InputStream input = new ByteArrayInputStream("test data".getBytes());

    String result = processor.process(input);

    assertEquals("expected", result);
}
```

**Parallelize Tests**
```bash
# Python: pytest with xdist
pytest -n auto  # Auto-detect CPU cores

# JavaScript: Jest runs parallel by default
jest --maxWorkers=4

# Go: Tests parallel by default
go test -parallel 4

# Ruby: RSpec with parallel_tests gem
parallel_rspec spec/
```

## Performance Testing Strategy

**Don't Performance Test in Unit Tests**: Unit tests verify correctness, not speed.

**Use Dedicated Performance Tests**:
```python
# Separate performance test suite
import pytest
from time import perf_counter

@pytest.mark.performance
def test_search_performance():
    database = create_database_with_million_records()

    start = perf_counter()
    results = database.search(query='Alice')
    duration = perf_counter() - start

    assert len(results) > 0  # Correctness
    assert duration < 0.1  # Performance threshold: < 100ms
```

**Load Testing**: Separate from unit tests
```python
# Use locust, k6, or JMeter for load testing
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def search_products(self):
        self.client.get("/api/products?q=laptop")

    @task(3)  # 3x more frequent
    def view_product(self):
        self.client.get("/api/products/123")

# Run: locust -f locustfile.py --users 100 --spawn-rate 10
```

## Identifying Performance Bottlenecks

**Profile Test Suite**
```bash
# Python: pytest with profiling
pytest --profile

# JavaScript: Jest with --logHeapUsage
jest --logHeapUsage

# Identify slowest tests
pytest --durations=10  # Show 10 slowest tests
```

**Common Bottlenecks**:
- Database queries (N+1 problem)
- File I/O
- Network calls
- Complex setup/teardown
- Inefficient algorithms

## Pattern: Performance-Critical Code Testing

```go
// Use benchmarks (separate from tests) for performance-critical code
func BenchmarkSearch(b *testing.B) {
    db := setupTestDatabase()

    b.ResetTimer()  // Don't include setup time
    for i := 0; i < b.N; i++ {
        db.Search("query")
    }
}

// Run: go test -bench=. -benchmem
// Output: BenchmarkSearch-8  100000  11234 ns/op  2048 B/op  15 allocs/op

// Test correctness separately
func TestSearch(t *testing.T) {
    db := setupTestDatabase()
    results := db.Search("query")

    assert.NotEmpty(t, results)
    assert.Equal(t, "expected", results[0].Name)
}
```

## When to Optimize

**Optimize test suite when:**
- Developers skip running tests because they're slow
- CI pipeline is bottlenecked on tests
- Individual test takes > 100ms (for unit tests)

**Don't optimize prematurely:**
- Test suite under 30 seconds - Good enough for most projects
- Optimization adds complexity - Only optimize if speed is actually a problem

## Common Mistakes

- Optimizing application code without tests - Optimization often breaks behavior; test first, then optimize
- Sharing state between tests for speed - Causes flaky tests; better to parallelize independent tests
- Skipping slow tests instead of fixing them - They'll never run, defeating the purpose
- Testing performance in unit tests - Unreliable (CPU load, other processes); use dedicated benchmarks
- Not profiling before optimizing - Profile to find actual bottlenecks, don't guess
- Caching test data between runs - Tests become non-repeatable; each test should set up own data

## See Also
- Previous: [Security Best Practices](security-best-practices.md) | Next: [Development Standards](development-standards.md)
- Related: [Unit Testing Fundamentals](unit-testing-fundamentals.md) (FIRST principles - Fast)
- Related: [Integration Testing Strategy](integration-testing.md)
