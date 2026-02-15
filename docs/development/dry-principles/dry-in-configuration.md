---
description: Managing application configuration, environment variables, and settings without duplication across environments
---

# DRY in Configuration

## When to Use

When managing application configuration, environment variables, feature flags, and settings across environments.

## Decision Framework

| Configuration Type | Single Source | Distribution Method |
|-------------------|---------------|---------------------|
| **Environment-specific** (DB host, API keys) | `.env` files, secrets manager | Environment variables, config service |
| **Application settings** (timeouts, limits) | Config files (YAML, JSON) | Typed config classes, validation at startup |
| **Feature flags** | Feature flag service | Runtime config API |
| **Business rules as config** | Database, admin UI | Config API, cache aggressively |
| **Infrastructure as code** | Terraform, CloudFormation | Code generation, state management |
| **Schema definitions** | JSON Schema, Protocol Buffers | Code generation for multiple languages |

## The Problem: Configuration Duplication

```yaml
# ANTI-PATTERN: Configuration duplicated across files

# config/development.yml
database:
  pool_size: 10
  timeout: 5000
  retry_attempts: 3
email:
  from: "dev@example.com"
  smtp_host: "localhost"

# config/staging.yml
database:
  pool_size: 10        # Duplicated
  timeout: 5000        # Duplicated
  retry_attempts: 3    # Duplicated
email:
  from: "staging@example.com"
  smtp_host: "smtp.staging.example.com"

# config/production.yml
database:
  pool_size: 10        # Duplicated
  timeout: 5000        # Duplicated
  retry_attempts: 3    # Duplicated
email:
  from: "noreply@example.com"
  smtp_host: "smtp.example.com"

# What happens when default pool_size changes? Update 3 files!
```

## Pattern: DRY Configuration

```yaml
# config/defaults.yml (single source of truth)
database:
  pool_size: 10
  timeout: 5000
  retry_attempts: 3

email:
  from: "noreply@example.com"
  smtp_host: "smtp.example.com"

# config/development.yml (only overrides)
email:
  from: "dev@example.com"
  smtp_host: "localhost"

# config/staging.yml (only overrides)
email:
  smtp_host: "smtp.staging.example.com"

# config/production.yml (only overrides, if any)
# Inherits all defaults
```

```python
# Load with merge strategy (Python example)
import yaml
from pathlib import Path

def load_config(env='development'):
    defaults = yaml.safe_load(Path('config/defaults.yml').read_text())
    env_config = yaml.safe_load(Path(f'config/{env}.yml').read_text())

    # Deep merge env_config into defaults
    return deep_merge(defaults, env_config)

config = load_config(os.getenv('APP_ENV', 'development'))
```

## Schema-Driven Configuration

```typescript
// DRY: Single schema generates types, validation, docs
import { z } from 'zod';

const ConfigSchema = z.object({
  database: z.object({
    poolSize: z.number().int().min(1).max(100).default(10),
    timeout: z.number().int().positive().default(5000),
    retryAttempts: z.number().int().min(0).max(10).default(3),
  }),
  email: z.object({
    from: z.string().email(),
    smtpHost: z.string(),
    smtpPort: z.number().int().default(587),
  }),
});

type Config = z.infer<typeof ConfigSchema>;

// Validation at startup
const config = ConfigSchema.parse({
  database: { poolSize: 10, timeout: 5000, retryAttempts: 3 },
  email: { from: 'dev@example.com', smtpHost: 'localhost' },
});

// Auto-generate documentation from schema
// Auto-generate JSON Schema for config files
```

## Infrastructure as Code (Single Source)

```hcl
# terraform/variables.tf (single source of truth)
variable "app_config" {
  type = object({
    pool_size       = number
    timeout         = number
    retry_attempts  = number
  })
  default = {
    pool_size      = 10
    timeout        = 5000
    retry_attempts = 3
  }
}

# Generate application config file from Terraform
resource "local_file" "app_config" {
  content = jsonencode({
    database = var.app_config
  })
  filename = "${path.module}/generated/config.json"
}

# No manual duplication — config exists in one place
```

## Common Mistakes

- **Copying entire config files per environment** — Massive duplication, hard to see what actually differs
- **Hardcoding values in code** — Configuration scattered across codebase, impossible to manage
- **No validation** — Invalid config only discovered at runtime, often in production
- **Manual synchronization** — Expecting developers to keep multiple config files in sync
- **Ignoring config as code** — No version control, no review process, no audit trail
- **Secrets in code** — API keys, passwords in source control (use secrets manager)

## See Also

- [Knowledge Duplication](knowledge-duplication.md)
- [DRY Across Boundaries](dry-across-boundaries.md)
- [Formae and PKL: Infrastructure Automation](https://dzone.com/articles/formae-pkl-infrastructure-automation)
- [Single Source of Truth - Wikipedia](https://en.wikipedia.org/wiki/Single_source_of_truth)
