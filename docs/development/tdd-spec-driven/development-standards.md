---
description: Dependency injection, single responsibility, coding standards, and testability checklist
---

# Development Standards

## When to Use
Every development project using TDD or testing. These standards ensure code quality, maintainability, and team consistency.

## Dependency Injection Over Static Calls

**Why**: Testability. Static calls and global state are hard to mock/stub in tests.

```php
// BAD: Static calls and global state
class UserService {
    public function createUser($email, $password) {
        $user = new User();
        $user->email = $email;
        $user->password = Hash::make($password);  // Static call - can't mock

        DB::table('users')->insert($user);  // Global DB - can't use test database

        return $user;
    }
}

// GOOD: Dependency injection
class UserService {
    private $hasher;
    private $userRepository;

    public function __construct(Hasher $hasher, UserRepository $userRepository) {
        $this->hasher = $hasher;
        $this->userRepository = $userRepository;
    }

    public function createUser($email, $password) {
        $user = new User();
        $user->email = $email;
        $user->password = $this->hasher->make($password);  // Injected - can mock

        $this->userRepository->save($user);  // Injected - can use test repo

        return $user;
    }
}

// Test with mocks
public function testCreateUser() {
    $hasher = $this->createMock(Hasher::class);
    $hasher->method('make')->willReturn('hashed_password');

    $userRepo = new InMemoryUserRepository();  // Fast test double

    $service = new UserService($hasher, $userRepo);
    $user = $service->createUser('alice@example.com', 'secret123');

    $this->assertEquals('hashed_password', $user->password);
    $this->assertEquals(1, $userRepo->count());
}
```

## Render Arrays Over Raw HTML

**Why**: Testability and security. Rendering HTML from strings leads to XSS vulnerabilities and is hard to test.

```php
// BAD: String concatenation (Drupal anti-pattern)
function render_user_profile($user) {
    $output = '<div class="user-profile">';
    $output .= '<h2>' . $user->name . '</h2>';  // XSS vulnerability
    $output .= '<p>' . $user->bio . '</p>';
    $output .= '</div>';
    return $output;
}

// GOOD: Render array (Drupal best practice)
function render_user_profile($user) {
    return [
        '#theme' => 'user_profile',
        '#user' => $user,
        '#cache' => [
            'tags' => ['user:' . $user->id()],
        ],
    ];
}

// Template file handles rendering (auto-escaped):
// user-profile.html.twig:
// <div class="user-profile">
//   <h2>{{ user.name }}</h2>
//   <p>{{ user.bio }}</p>
// </div>

// Test render array structure
public function testUserProfileRenderArray() {
    $user = User::create(['name' => 'Alice', 'bio' => 'Developer']);

    $render = render_user_profile($user);

    $this->assertEquals('user_profile', $render['#theme']);
    $this->assertEquals($user, $render['#user']);
    $this->assertContains('user:' . $user->id(), $render['#cache']['tags']);
}
```

## Proper API Usage

**Don't reinvent the wheel**: Use framework/language APIs correctly.

```python
# BAD: Reimplementing standard library functions
def my_sort(items):
    # 30 lines of bubble sort implementation
    pass

def test_my_sort():
    # Testing code that shouldn't exist
    pass

# GOOD: Use built-in
def process_items(items):
    return sorted(items)  # Built-in, tested, optimized

def test_process_items():
    # Test your logic, not Python's sort
    items = [3, 1, 2]
    assert process_items(items) == [1, 2, 3]
```

## Single Responsibility Principle

**Why**: Testability. Classes/functions with one responsibility are easier to test.

```typescript
// BAD: God class with multiple responsibilities
class UserManager {
  validateEmail(email: string): boolean { }
  hashPassword(password: string): string { }
  sendWelcomeEmail(email: string): void { }
  logRegistration(userId: number): void { }
  updateMetrics(event: string): void { }
  createUser(email: string, password: string): User {
    // Uses all of the above
  }
}

// Tests are complex because class does too much
// Mocking is difficult because all dependencies in one class

// GOOD: Separate concerns
class EmailValidator {
  validate(email: string): boolean { }
}

class PasswordHasher {
  hash(password: string): string { }
}

class UserRepository {
  save(user: User): User { }
}

class RegistrationService {
  constructor(
    private validator: EmailValidator,
    private hasher: PasswordHasher,
    private repository: UserRepository
  ) {}

  register(email: string, password: string): User {
    if (!this.validator.validate(email)) {
      throw new Error('Invalid email');
    }

    const user = new User(email, this.hasher.hash(password));
    return this.repository.save(user);
  }
}

// Tests are simple, focused, fast
test('EmailValidator validates email format', () => {
  const validator = new EmailValidator();
  expect(validator.validate('alice@example.com')).toBe(true);
  expect(validator.validate('invalid')).toBe(false);
});
```

## Coding Standards

**Consistency matters more than specific style**: Pick a standard, enforce it.

```javascript
// Use linters and formatters
// .eslintrc.json
{
  "extends": "airbnb",
  "rules": {
    "max-len": ["error", { "code": 100 }],
    "no-console": "error"
  }
}

// .prettierrc
{
  "singleQuote": true,
  "trailingComma": "es5"
}

// Run in CI
"scripts": {
  "lint": "eslint src/",
  "format": "prettier --check src/",
  "test": "jest"
}
```

## Testability Checklist

Code is testable when:
- [ ] Dependencies are injected, not created internally
- [ ] Functions are pure (same input = same output) when possible
- [ ] Side effects are isolated and explicit
- [ ] Classes have single responsibility
- [ ] No hidden global state
- [ ] No hard-coded file paths, URLs, dates, random values
- [ ] Public API is small and focused

Code is NOT testable when:
- [ ] Uses static methods/singletons extensively
- [ ] Accesses database/filesystem directly (not through abstraction)
- [ ] Has many dependencies created with `new` inside methods
- [ ] Uses current date/time without abstraction
- [ ] Has conditional logic based on environment (DEV vs PROD)
- [ ] Depends on execution order or global state

## Common Mistakes

- Writing code without thinking about tests - Results in untestable code; consider testability during design
- Refactoring to make tests pass instead of code testable - Hides design problems; untestable code is poorly designed code
- Using mocks to work around bad design - Mocks should be for external boundaries, not covering up coupling
- Not enforcing coding standards - Inconsistency wastes time in code review and makes code harder to maintain
- Skipping code review for "small changes" - Small changes can introduce big security/quality issues

## See Also
- Previous: [Performance Best Practices](performance-best-practices.md) | Next: [Code Reference Map](code-reference-map.md)
- Related: [Test Doubles](test-doubles.md) (proper use of mocks)
- Related: [Refactoring with Confidence](refactoring-confidence.md)
- Reference: [PHP-FIG Standards](https://www.php-fig.org/)
- Reference: [Google Style Guides](https://google.github.io/styleguide/)
