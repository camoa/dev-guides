---
description: GitHub Actions for Drupal — automated CI/CD workflows for testing, building, and deploying
tracks: []
guide-meta:
  concepts:
    - GitHub Actions
    - Drupal CI/CD
    - matrix testing
    - PHPUnit CI
    - theme asset compilation
    - deployment artifacts
    - secret management
  not:
    - GitLab CI
    - Bitbucket Pipelines
    - local testing
  requires: []
  complements:
    - drupal/testing
    - drupal/tdd
  specializes: ""
  category: drupal
---

# GitHub Actions

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand GitHub Actions basics | [Workflow Fundamentals](workflow-fundamentals.md) | Use GitHub Actions workflows to automate testing, builds, and deployments. Choose triggers based on when automation should run. |
| Set up a Drupal workflow | [Drupal Stack Setup](drupal-stack-setup.md) | Use when configuring the runtime environment for Drupal testing and builds in GitHub Actions. |
| Test multiple versions | [Matrix Testing](matrix-testing.md) | Use matrix testing when you need to verify compatibility across multiple Drupal versions, PHP versions, or database types. |
| Run code quality checks | [Code Quality Checks](code-quality-checks.md) | Use before running tests to validate code standards, security, and static analysis. |
| Test with PHPUnit | [PHPUnit Testing](phpunit-testing.md) | Use for automated unit, kernel, functional, and JavaScript tests for Drupal modules. |
| Compile theme assets | [Theme Asset Compilation](theme-asset-compilation.md) | Use when building Sass, JavaScript, and optimizing assets for Drupal themes in automated workflows. |
| Create deployment artifacts | [Deployment Artifacts](deployment-artifacts.md) | Use when packaging builds for deployment to staging or production environments. |
| Deploy to environments | [Multi-Environment Deployment](multi-environment-deployment.md) | Use when deploying to staging, production, or multiple hosting environments with different requirements. |
| Cache dependencies | [Caching Strategies](caching-strategies.md) | Use to speed up workflow execution by reusing dependencies and build outputs between runs. |
| Run jobs in parallel | [Parallel Execution](parallel-execution.md) | Use when running independent jobs concurrently to reduce total workflow time. |
| Manage secrets | [Secret Management](secret-management.md) | Use for storing sensitive credentials for deployments, API access, and third-party services. |
| Protect environments | [Environment Protection](environment-protection.md) | Use when adding approval gates and validation for production deployments to prevent accidental releases. |
| Troubleshoot failures | [Troubleshooting](troubleshooting.md) | Use when debugging common GitHub Actions failures in Drupal workflows. |
