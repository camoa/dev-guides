---
description: How to structure specifications with behavior, acceptance criteria, edge cases, and constraints
---

# Writing Effective Specifications

## When to Use
Before implementing any feature using AI code generation or when you want specifications to serve as living documentation and development contract.

## Specification Structure

A good specification includes:

**1. Overview** - What this feature/component does (2-3 sentences)

**2. Behavior** - How it should behave in normal operation (Given/When/Then style)

**3. Acceptance Criteria** - Checklist of requirements that define "done"

**4. Edge Cases** - Non-obvious scenarios and how to handle them

**5. Constraints** - Technical/business rules that must be followed

**6. Integration Points** - What this interacts with and how

## Pattern: Effective Specification

```markdown
# User Authentication Service

## Overview
Authenticates users via email/password, issues JWT tokens for session management,
and enforces rate limiting to prevent brute force attacks.

## Behavior

### Successful Login
Given a user with email "alice@example.com" and password "secret123"
When the user submits valid credentials
Then the service returns a JWT token valid for 24 hours
And the token includes user ID and role claims

### Failed Login - Invalid Credentials
Given a user with email "alice@example.com"
When the user submits an incorrect password
Then the service returns 401 Unauthorized
And the service logs the failed attempt
And the service does NOT reveal whether email exists

### Failed Login - Rate Limiting
Given a user has made 5 failed login attempts in 15 minutes
When the user attempts another login
Then the service returns 429 Too Many Requests
And the service blocks further attempts for 15 minutes

## Acceptance Criteria
- [ ] Password comparison uses timing-safe comparison to prevent timing attacks
- [ ] Passwords are never logged or returned in responses
- [ ] JWT tokens are signed with RS256 algorithm
- [ ] Rate limiting is per IP address, not per email
- [ ] Failed login attempts are logged with timestamp, IP, and email (but not password)
- [ ] Service responds within 200ms for valid credentials
- [ ] Service responds within 200-500ms for invalid credentials (constant-time response)

## Edge Cases
- Empty email or password: 400 Bad Request with validation errors
- Email with uppercase/mixed case: Normalize to lowercase before lookup
- Email not found in database: Return same error as invalid password (don't leak user existence)
- User account is locked/disabled: 403 Forbidden with "account disabled" message
- Token expiration time in past: Treat as invalid token
- Missing JWT secret in configuration: Fail startup, don't allow insecure operation

## Constraints
- Must NOT store passwords in plain text
- Must use bcrypt with cost factor >= 12 for password hashing
- Must NOT use MD5, SHA1, or SHA256 for password hashing
- JWT secret must be at least 256 bits
- Rate limiting must survive service restarts (use Redis or database, not in-memory)

## Integration Points
- **User Database**: Queries user table by email, retrieves hashed password and user metadata
- **Redis**: Stores rate limiting counters with TTL
- **Logging Service**: Sends structured logs for failed attempts and successful authentications
- **Metrics Service**: Reports login success/failure rates for monitoring
```

## Good Specification Characteristics

**Uses Domain Language**: Describes behavior in business terms, not technical implementation
- Good: "When cart total exceeds $100, apply free shipping"
- Bad: "When `cart.total > 100`, set `shipping_cost = 0` in the database"

**Focuses on Behavior**: What the code should do, not how to do it
- Good: "Retry failed API calls up to 3 times with exponential backoff"
- Bad: "Create a for loop that runs 3 times, multiply delay by 2 each time"

**Covers Critical Path and Edge Cases**: Not exhaustive, but hits important scenarios
- Include: Happy path, common errors, security boundaries
- Skip: Every possible permutation (that's what tests verify)

**Measurable Acceptance Criteria**: Clear pass/fail conditions
- Good: "Responds within 200ms for 95% of requests"
- Bad: "Runs fast"

**Concise but Complete**: Enough detail for unambiguous implementation
- Sweet spot: 1-2 pages for most features
- Too short: "Build a user login" (vague)
- Too long: 20 pages of detailed implementation (defeats AI generation purpose)

## Specification Anti-Patterns

**Implementation Details in Spec**
```markdown
# BAD: Overly prescriptive
- Create a UserAuthenticator class that extends BaseAuthenticator
- Use a HashMap to store user credentials in memory
- Implement a singleton pattern for the authentication service

# GOOD: Behavior-focused
- Authenticate users with email and password
- Support concurrent authentication requests without race conditions
- Persist authentication state across service restarts
```

**Vague Requirements**
```markdown
# BAD: Unclear
- Handle errors properly
- Make it fast
- Should be secure

# GOOD: Specific
- Return 400 Bad Request with validation errors for invalid input
- Respond within 200ms for 95% of requests under normal load
- Use bcrypt with cost factor 12 for password hashing
```

**Missing Edge Cases**
```markdown
# BAD: Only happy path
Given valid credentials, user is authenticated

# GOOD: Covers edge cases
- Valid credentials: Success with JWT token
- Invalid password: 401 Unauthorized
- Account disabled: 403 Forbidden
- Rate limit exceeded: 429 Too Many Requests
- Malformed email: 400 Bad Request
```

## Tools and Templates

**GitHub Spec Kit**: Formalizes SDD with CLI and templates
```bash
spec-kit init               # Initialize spec structure
spec-kit spec create        # Create new spec from template
spec-kit plan              # Generate implementation plan
spec-kit task              # Break down into tasks
```

**Amazon Kiro**: Uses spec -> design -> tasks workflow

**Claude Code / Cursor**: Read spec files and generate code (no formal template required)

## Common Mistakes

- Mixing specification and implementation - Keep separate; spec says what, code says how
- Writing specs like traditional requirements docs - Specs are for AI/developers, not stakeholders; use technical precision, not business jargon
- Not reviewing specs before coding - Bad spec = bad generated code; review and refine specs first
- Specifications without acceptance criteria - Can't verify code matches spec without measurable criteria
- Over-specifying every detail - Specs aren't exhaustive; cover critical path and edge cases, let implementation handle routine cases

## See Also
- Previous: [Spec-Driven Development Overview](spec-driven-overview.md) | Next: [From Spec to Implementation](spec-to-implementation.md)
- Related: [Testing Patterns](testing-patterns.md) (Given-When-Then structure)
- Reference: [GitHub Spec Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit)
- Reference: [How Spec-Driven Development Improves AI Coding Quality](https://developers.redhat.com/articles/2025/10/22/how-spec-driven-development-improves-ai-coding-quality)
