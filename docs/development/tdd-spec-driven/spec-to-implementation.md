---
description: Workflow for generating code from specs using AI tools, with verification and iterative refinement
---

# From Spec to Implementation

## When to Use
You have a detailed specification and are ready to generate or write code using AI assistance, or you're manually implementing code that must match a specification.

## Workflow: Spec to Code

**1. Spec Review and Validation**
```markdown
Before coding:
- [ ] Spec has clear behavior descriptions (Given/When/Then)
- [ ] Acceptance criteria are measurable
- [ ] Edge cases are documented
- [ ] Constraints are specific (not "be secure" but "use bcrypt cost 12")
- [ ] Integration points are identified
- [ ] Team/stakeholders have reviewed and approved

If any checklist item fails, refine spec before proceeding.
```

**2. AI Code Generation**
```
# Prompt pattern for AI code generation
Given this specification: [paste or reference spec file]

Generate production-quality code that:
1. Implements all behaviors described in the spec
2. Handles all edge cases listed
3. Meets all acceptance criteria
4. Respects all constraints
5. Includes comprehensive error handling
6. Follows [language] best practices and idioms

Include unit tests that verify each behavior against the spec.
```

**3. Verification Against Spec**
- Does code implement all specified behaviors? - Check each Given/When/Then
- Does code handle all edge cases? - Test or code review each scenario
- Do tests verify acceptance criteria? - Each criterion should have test coverage
- Are constraints respected? - Code review for technical requirements
- Are integration points correct? - Check interfaces match spec

**4. Iterative Refinement**
```
If verification fails:
  - Identify gap between spec and implementation
  - Determine if spec was unclear or code is wrong
  - If spec unclear: Update spec, regenerate code
  - If code wrong: Fix code or regenerate with clarified prompt
  - Re-verify
```

## Pattern: Manual Implementation with Spec

```python
# Spec excerpt:
# When user submits valid credentials
# Then service returns JWT token valid for 24 hours
# And token includes user ID and role claims

# Implementation following spec
def authenticate(email: str, password: str) -> AuthResult:
    """
    Authenticates user with email/password.

    Spec reference: User Authentication Service - Successful Login
    """
    # Normalize email (spec edge case)
    email = email.lower().strip()

    # Lookup user (spec integration point: User Database)
    user = user_repository.find_by_email(email)
    if not user:
        # Spec requirement: same error for invalid password and non-existent user
        raise InvalidCredentialsError("Invalid email or password")

    # Verify password (spec constraint: timing-safe comparison)
    if not bcrypt.verify_timing_safe(password, user.password_hash):
        # Spec behavior: log failed attempt
        audit_log.record_failed_login(email, request.ip_address)
        raise InvalidCredentialsError("Invalid email or password")

    # Generate JWT (spec behavior: 24 hour expiry, includes user ID and role)
    token = jwt.encode(
        payload={
            'user_id': user.id,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        algorithm='RS256'  # Spec constraint
    )

    return AuthResult(token=token, user=user)
```

## AI Tools and Workflows

**Claude Code / Cursor**
1. Save spec as `spec.md` in project
2. Reference spec in prompt: "Read spec.md and implement UserAuthService"
3. AI generates code matching spec
4. Review, test, refine

**GitHub Copilot with Spec Kit**
1. Use spec-kit to create formal spec structure
2. Run `spec-kit plan` to generate implementation plan
3. Run `spec-kit task` to break into tasks
4. Copilot generates code for each task

**Amazon Kiro**
1. Write requirement in natural language
2. Kiro generates spec (review and refine)
3. Kiro generates design document (review and refine)
4. Kiro generates implementation tasks
5. Kiro generates code for each task

## Spec as Living Documentation

**When Requirements Change:**
```
Traditional: Update code, hope docs get updated later (they don't)

Spec-Driven:
1. Update spec to reflect new requirements
2. Review spec changes (like code review)
3. Regenerate affected code from updated spec
4. Verify new code against updated spec

Result: Spec is always current because code generation depends on it
```

**When Code Needs Optimization:**
```
If optimization doesn't change behavior:
  - Refactor code without changing spec
  - Tests verify behavior unchanged

If optimization changes behavior (e.g., different error messages):
  - Update spec to reflect new behavior
  - Update code to match spec
  - Review both changes together
```

## Decision Points

| Situation | Action |
|-----------|--------|
| AI generates code that doesn't match spec | Regenerate with more specific prompt or clarify spec |
| Spec is ambiguous during implementation | Stop coding, clarify spec, then implement |
| Edge case discovered during implementation | Add to spec, ensure it's tested, continue implementation |
| Performance requirement in spec not met | Profile code; if optimization needed, update spec if behavior changes |
| AI generates insecure code despite security spec | Spec wasn't specific enough; add technical constraints (e.g., "use bcrypt cost 12"), regenerate |

## Common Mistakes

- Generating code without reviewing spec first - Bad spec = bad code; review spec before generation
- Accepting AI-generated code without verification - Always verify against spec; AI makes mistakes
- Updating code without updating spec - Spec becomes stale; changes should update spec first
- Writing implementation details in spec to control AI - Spec should describe behavior, not implementation; let AI choose implementation
- Not testing generated code - AI code looks good but may have subtle bugs; comprehensive testing required

## See Also
- Previous: [Writing Effective Specifications](writing-specs.md) | Next: [Integration Testing Strategy](integration-testing.md)
- Related: [Red-Green-Refactor Workflow](red-green-refactor.md) (complementary practice)
- Related: [Security Best Practices](security-best-practices.md)
- Reference: [Spec-Driven Development ArXiv Paper](https://arxiv.org/html/2602.00180v1)
- Reference: [My LLM Coding Workflow - Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/)
