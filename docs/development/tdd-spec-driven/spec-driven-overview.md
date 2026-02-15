---
description: What Spec-Driven Development is, how it works, and how it complements TDD for AI-assisted coding
---

# Spec-Driven Development Overview

## When to Use
You're using AI coding assistants and want to maintain control over architecture while leveraging AI for implementation. Essential for production-quality code generation with tools like Claude Code, GitHub Copilot, Cursor, or Amazon Kiro.

## What is Spec-Driven Development (SDD)?

Spec-Driven Development is a development paradigm that **treats specifications as the source of truth and code as a generated or verified secondary artifact**. Instead of writing code first and documenting later, you write detailed specifications first, then use those specs to drive implementation - either manually or with AI assistance.

**Traditional workflow:**
```
Requirements -> Code -> Tests -> Documentation
```

**Spec-Driven workflow:**
```
Requirements -> Specification -> Code (AI-generated) -> Verification against Spec
                     |
              Living Documentation
```

## Why SDD Emerged in 2024-2025

The rise of AI coding assistants created a new problem: "vibe coding" where developers could build applications quickly but they were **buggy, unmaintainable, and not production-ready**. The code worked for demos but couldn't scale.

In mid-2025, AWS introduced Amazon Kiro, promoting SDD as the solution. The key insight: **AI needs structured prompts (specifications) to generate quality code**, not free-form descriptions.

By late 2025, 15+ major platforms adopted SDD principles:
- **AI-native IDEs**: Cursor, Windsurf, Zed
- **CLI tools**: Amazon Kiro, Claude Code
- **Extensions**: GitHub Copilot with Spec Kit

## How SDD Works

1. **Specification Phase** (Human-led)
   - Write detailed specs describing behavior, constraints, acceptance criteria
   - Define edge cases, error handling, integration points
   - Review and refine specs before coding
   - Specs use domain language, not implementation details

2. **Implementation Phase** (AI-assisted or manual)
   - AI coding agent reads spec and generates code
   - Code is treated as disposable - if wrong, regenerate from spec
   - Spec remains authoritative; code changes require spec updates

3. **Verification Phase** (Human-led)
   - Verify generated code matches specification
   - Test against acceptance criteria in spec
   - Refine spec if requirements were unclear

## SDD vs TDD

| Aspect | TDD | SDD |
|--------|-----|-----|
| Source of truth | Tests | Specification documents |
| Primary artifact | Code + tests | Specification + code |
| Workflow | Test -> Code -> Refactor | Spec -> Generate -> Verify |
| AI integration | Not designed for AI | Designed for AI code generation |
| Documentation | Tests as documentation | Specs as documentation |
| When code changes | Update tests and code together | Update spec, regenerate code |

**They're complementary**: SDD defines what to build, TDD ensures it works correctly. Best practice: Write specs, generate/write code with TDD approach.

## Benefits of SDD

**Better AI code quality**: Internal Azure team reported 5x speedup (2 weeks to 2 days) using AI with detailed specs. Industry reports show 2-10x improvements are common.

**Specs as living documentation**: Unlike outdated docs, specs must be current or code generation fails.

**Easier code review**: Review spec first (quick), then verify code matches spec (mechanical).

**Prevents scope creep**: Spec changes are explicit and reviewed before implementation.

**Onboarding**: New developers read specs to understand system, not reverse-engineer from code.

## Common Mistakes

- Writing implementation-focused specs - Specs should describe behavior, not implementation (no "use a HashMap" or "make it a singleton")
- Vague specifications - AI generates code matching vague specs, but it won't be what you actually need
- Skipping spec review - Bad specs generate bad code; review specs before coding
- Not updating specs when requirements change - Specs become stale documentation, defeating the purpose
- Treating specs as heavyweight docs - Specs should be concise, focused on critical path and edge cases

## See Also
- Next: [Writing Effective Specifications](writing-specs.md)
- Related: [TDD Overview](tdd-overview.md) - complementary practice
- Reference: [Spec-Driven Development - Thoughtworks](https://thoughtworks.medium.com/spec-driven-development-d85995a81387)
- Reference: [Spec-Driven Development Guide 2025](https://www.softwareseni.com/spec-driven-development-in-2025-the-complete-guide-to-using-ai-to-write-production-code/)
