---
description: Testing frameworks, mocking libraries, BDD tools, and resources organized by programming language
---

# Code Reference Map

## When to Use
You need testing frameworks, tools, or resources for your specific language/framework. This is a curated map of authoritative resources.

## Essential Books (Language-Agnostic)

**Test-Driven Development: By Example** - Kent Beck (2002)
- The foundational TDD book
- Language: Java and Python examples
- Covers: Red-Green-Refactor, test patterns, TDD rhythm
- Still relevant in 2025

**Clean Code** - Robert C. Martin (2008)
- Chapters on TDD and testing principles
- Language: Java
- Covers: Test quality, FIRST principles, clean tests

**Growing Object-Oriented Software, Guided by Tests** - Steve Freeman & Nat Pryce (2009)
- Advanced TDD techniques
- Language: Java
- Covers: Outside-in TDD, mock objects, test-driven design

**Refactoring: Improving the Design of Existing Code** - Martin Fowler (2018, 2nd ed)
- Essential for the Refactor step in TDD
- Language: JavaScript (1st ed was Java)
- Covers: Code smells, refactoring catalog, refactoring under tests

**Effective Behavior-Driven Development** - Gaspar Nagy & Seb Rose (2025)
- Modern BDD practices
- Language: Gherkin/Cucumber
- Covers: Discovery, formulation, automation with BDD

## Testing Frameworks by Language

**Python**
- **pytest** - https://pytest.org - Industry standard, powerful fixtures, plugins
- **unittest** - https://docs.python.org/3/library/unittest.html - Built-in, xUnit style
- **doctest** - Built-in, tests in docstrings
- **Hypothesis** - Property-based testing
- Coverage: `coverage.py`, `pytest-cov`

**JavaScript/TypeScript**
- **Jest** - https://jestjs.io - React ecosystem, batteries included
- **Vitest** - https://vitest.dev - Modern, Vite-based, fast
- **Mocha** - Classic, flexible
- **Jasmine** - BDD style
- E2E: **Playwright**, **Cypress**
- Coverage: Istanbul (nyc), built into Jest/Vitest

**PHP**
- **PHPUnit** - https://phpunit.de - Industry standard
- **Pest** - Modern, elegant syntax, built on PHPUnit
- **Codeception** - Full-stack testing (unit, integration, E2E)
- **Behat** - BDD with Gherkin
- Coverage: Xdebug with PHPUnit

**Java**
- **JUnit 5** - https://junit.org/junit5 - Industry standard
- **TestNG** - Alternative with advanced features
- **Mockito** - Mocking framework
- **AssertJ** - Fluent assertions
- **Cucumber-JVM** - BDD
- Coverage: JaCoCo, Cobertura

**C#/.NET**
- **xUnit** - https://xunit.net - Modern, recommended by Microsoft
- **NUnit** - Classic, widely used
- **MSTest** - Microsoft's built-in
- **Moq** - Mocking
- **SpecFlow** - BDD
- Coverage: Coverlet, dotCover

**Ruby**
- **RSpec** - https://rspec.info - BDD style, most popular
- **Minitest** - Built-in, fast, simple
- **Cucumber** - BDD with Gherkin
- Coverage: SimpleCov

**Go**
- **testing** - https://pkg.go.dev/testing - Built-in, standard
- **testify** - Assertions and mocks
- **Ginkgo** - BDD style
- **gomock** - Mocking
- Coverage: `go test -cover` (built-in)

**Rust**
- **cargo test** - Built-in test framework
- **proptest** - Property-based testing
- **mockall** - Mocking
- Coverage: `cargo-tarpaulin`

## BDD Tools

**Gherkin/Cucumber Family**
- **Cucumber** (Ruby, Java, JavaScript) - https://cucumber.io
- **Behat** (PHP) - https://behat.org
- **SpecFlow** (.NET) - https://specflow.org
- **behave** (Python) - https://behave.readthedocs.io

## Mocking Libraries

See [Test Doubles](test-doubles.md) for when to use each type.

```
Python:      unittest.mock (built-in), pytest-mock
JavaScript:  Sinon.js, Jest (built-in), Vitest (built-in)
PHP:         Mockery, Prophecy, PHPUnit mocks
Java:        Mockito, EasyMock, PowerMock
C#:          Moq, NSubstitute, FakeItEasy
Ruby:        RSpec mocks (built-in), Mocha
Go:          gomock, testify/mock
```

## Web Resources

**Martin Fowler's Blog** - https://martinfowler.com
- Authoritative articles on testing, refactoring, TDD
- Test Double, Test Pyramid, Mocks Aren't Stubs

**Kent C. Dodds** - https://kentcdodds.com
- Testing Trophy, JavaScript testing practices
- "Write tests. Not too many. Mostly integration."

**Thoughtworks Technology Radar** - https://www.thoughtworks.com/radar
- Emerging testing tools and practices
- Spec-Driven Development coverage (2025)

**OWASP** - https://owasp.org
- Security testing best practices
- Top 10 vulnerabilities to test for

## Community Resources

**Drupal at Your Fingertips** - https://www.drupalatyourfingertips.com/
- Selwyn Polit's comprehensive Drupal development resource
- PHP/Drupal testing patterns and examples

**Test-Driven Development MOOC** - https://tdd.mooc.fi
- Free online course on TDD fundamentals
- Interactive exercises

## Spec-Driven Development Tools (2025+)

**GitHub Spec Kit** - https://github.com/github/spec-kit
- Open-source SDD framework
- CLI, templates, prompts for spec to plan to tasks to code

**Amazon Kiro** - https://aws.amazon.com/kiro
- AWS's SDD tool
- Spec to design to tasks workflow

**Claude Code** - https://claude.com/claude-code
- AI coding assistant with spec support
- Read specs from files, generate implementation

**Cursor** - https://cursor.sh
- AI-powered IDE
- Spec-aware code generation

## See Also
- Previous: [Development Standards](development-standards.md)
