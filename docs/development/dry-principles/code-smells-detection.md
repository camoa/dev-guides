---
description: Detecting duplication through code review, automated tools, and metrics - plus identifying wrong abstractions
---

# Code Smells and Detection

## When to Use

When reviewing code, performing maintenance, or evaluating technical debt related to duplication.

## Duplication Code Smells

| Code Smell | What to Look For | Severity |
|------------|------------------|----------|
| **Exact duplication** | Copy-pasted code blocks | High -- refactor immediately |
| **Semantic duplication** | Same business logic, different implementations | High -- consolidate |
| **Structural duplication** | Similar patterns serving different purposes | Low -- may be acceptable |
| **Magic numbers repeated** | Same constants hardcoded in multiple places | Medium -- extract to config |
| **Parallel inheritance hierarchies** | Adding subclass requires adding another elsewhere | High -- redesign abstraction |
| **Shotgun surgery** | Single change requires editing many files | High -- indicates missing abstraction |

## Detection Techniques

### 1. Manual Code Review

```python
# Checklist during code review:
# - Are there repeated code blocks? (exact duplication)
# - Are business rules expressed in multiple places? (knowledge duplication)
# - Are constants hardcoded repeatedly? (magic numbers)
# - Do multiple functions have similar structure? (structural duplication)
# - Would a change require editing multiple files? (shotgun surgery)
```

### 2. Automated Tools

| Tool | Language Support | Strengths | Use Case |
|------|-----------------|-----------|----------|
| **jscpd** | 150+ languages | Fast, supports many formats | Multi-language projects |
| **PMD CPD** | 31+ languages (Java, C++, Python, Go) | Comprehensive, XML/HTML reports | Java-focused shops |
| **SonarQube** | 30+ languages | Integrates with CI/CD, tracks over time | Enterprise codebases |
| **Simian** | Java, C#, C++, Ruby, etc. | Cross-language detection | Polyglot codebases |
| **Clone Digger** | Python | Deep semantic analysis | Python projects |

```bash
# Example: jscpd for detecting duplication
npx jscpd src/ --min-lines 5 --min-tokens 50 --format json

# Example: PMD CPD for Java
pmd cpd --minimum-tokens 50 --files src/ --language java --format text

# Example: SonarQube scanner
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=src \
  -Dsonar.host.url=http://localhost:9000
```

### 3. Metrics to Track

| Metric | What It Measures | Healthy Range |
|--------|------------------|---------------|
| **Duplication %** | Percentage of duplicated code | < 5% |
| **Duplication blocks** | Number of duplicated code blocks | Trend down over time |
| **Shotgun surgery instances** | Files changed per feature | < 5 files per change |
| **Cyclomatic complexity** | Branching/conditionals in functions | < 10 per function |

## Identifying Wrong Abstractions

```typescript
// RED FLAGS for wrong abstractions:

// 1. Lots of boolean parameters (configuration smell)
function sendNotification(
  user: User,
  message: string,
  isEmail: boolean,
  isSms: boolean,
  isPush: boolean,
  isUrgent: boolean
) {
  // Too many conditionals based on booleans
  if (isEmail) { /* ... */ }
  if (isSms) { /* ... */ }
  // This should be separate functions or strategy pattern
}

// 2. Null/undefined passed frequently (abstraction doesn't fit all callers)
processOrder(order, null, undefined, false);  // What do these mean?

// 3. Constantly modifying abstraction for new cases
class Exporter {
  export(data, format) {
    if (format === 'csv') { /* ... */ }
    else if (format === 'json') { /* ... */ }
    else if (format === 'xml') { /* ... */ }
    else if (format === 'pdf') { /* ... */ }  // Keep adding...
    // This should be strategy pattern or separate classes
  }
}

// 4. Abstraction name is vague
class DataManager { /* What does this even do? */ }
class Helper { /* Helper for what? */ }
class Utility { /* Too generic */ }
```

## Code Review Checklist

**When reviewing for duplication:**

- [ ] Is there exact code duplication (copy-paste)?
- [ ] Is the same business logic expressed in multiple places?
- [ ] Are there magic numbers or strings that should be constants?
- [ ] If I change a business rule, how many files do I need to edit?
- [ ] Are there similar functions that could be parameterized or generalized?
- [ ] Is this abstraction helping or hiding complexity?
- [ ] Could a developer understand this code in 6 months?

**When creating abstractions:**

- [ ] Have I seen this pattern at least 3 times?
- [ ] Do all instances represent the same knowledge?
- [ ] Is the abstraction simpler than the duplication?
- [ ] Are requirements stable enough to abstract?
- [ ] Can I give the abstraction a clear, specific name?
- [ ] Does the abstraction have fewer than 5 parameters?
- [ ] Will this abstraction make future changes easier?

## Refactoring Strategy

```
1. Identify duplication (tools + manual review)
   |
2. Classify type:
   - Exact -> Extract function/class immediately
   - Knowledge -> Consolidate to single source
   - Incidental -> Leave separate
   - Imposed -> Code generation or accept
   |
3. Apply Rule of Three:
   - 1-2 instances -> Wait
   - 3+ instances -> Consider refactoring
   |
4. Choose abstraction strategy:
   - Simple logic -> Extract function
   - State + behavior -> Extract class
   - Cross-cutting -> Decorator/middleware
   - Variation -> Strategy pattern
   |
5. Validate:
   - Tests pass
   - Code is simpler
   - Future changes are easier
   - No hidden coupling introduced
```

## Common Mistakes

- **Relying only on tools** — Tools catch syntactic duplication, miss semantic/knowledge duplication
- **Ignoring structural duplication** — Sometimes similar code serves different purposes (OK to keep)
- **Not tracking duplication over time** — Need baseline and trend analysis
- **Refactoring without tests** — Risky; write tests first, then refactor
- **Treating all duplication as urgent** — Prioritize knowledge duplication and security-critical code

## See Also

- [Code Duplication](code-duplication.md)
- [Rule of Three](rule-of-three.md)
- [jscpd - Copy/Paste Detector](https://github.com/kucherenko/jscpd)
- [PMD CPD Documentation](https://pmd.github.io/pmd/pmd_userdocs_cpd.html)
