---
description: Supply chain security including 7-day dependency cooldown, lock files, vulnerability scanning, dependency pruning, SRI, and private registries.
---

# Dependency Security

## When to Use

Every project uses third-party dependencies — npm packages, PyPI libraries, Maven artifacts, gems, Go modules. **Supply chain attacks** are the fastest-growing threat in 2025. Dependencies are the largest attack surface in modern applications.

## The 2025 Supply Chain Threat Landscape

**Major 2025 attacks:**

- **Shai-Hulud (Sept 2025):** First self-replicating npm malware, spread autonomously across developer environments
- **Shai-Hulud 2.0:** Affected 25,000+ GitHub repositories, ~350 unique users
- **s1ngularity campaign (Aug-Nov 2025):** Compromised Nx packages, harvested 2,349 credentials from 1,079 developer systems
- **8 out of 10 major 2025 supply chain attacks** could have been prevented with 7-day dependency cooldown

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Track dependencies | **Software Bill of Materials (SBOM)** | Inventory for vulnerability tracking |
| Scan for vulnerabilities | Dependabot, Snyk, OWASP Dependency-Check | Automated vulnerability detection |
| Prevent supply chain attacks | **7-day cooldown** + lock files + signature verification | Time to detect malicious packages |
| Verify package integrity | Hash verification (package-lock.json, Pipfile.lock) | Detect tampering |
| Minimize attack surface | Dependency pruning + audit | Fewer dependencies = smaller attack surface |

## 7-Day Dependency Cooldown

**The single most effective supply chain defense in 2025:**

```json
// .npmrc or npm config
{
  "min-publish-age": 604800000
}
```

**Why it works:**

- 8 of 10 major 2025 supply chain attacks would have been prevented
- Malicious packages typically detected and removed within 24-48 hours
- Creates detection buffer for security vendors

```python
# Python - check package publish date before installing
import requests
from datetime import datetime, timedelta

def check_package_age(package_name, min_days=7):
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
    data = response.json()
    latest_version = data['info']['version']
    upload_time = data['releases'][latest_version][0]['upload_time']
    published_date = datetime.strptime(upload_time, '%Y-%m-%dT%H:%M:%S')
    age_days = (datetime.now() - published_date).days
    if age_days < min_days:
        raise ValueError(f'Package published {age_days} days ago, minimum {min_days} required')
    return True
```

## Lock Files and Integrity Verification

**Always commit lock files:**

```bash
# npm
npm install  # Generates package-lock.json
git add package-lock.json

# Python
pipenv lock  # Generates Pipfile.lock with hashes
pip-compile --generate-hashes requirements.in  # Better: with hashes
```

**Verify package integrity:**

```bash
npm ci  # Clean install using exact versions from lock file
pip install --require-hashes -r requirements.txt
go mod verify
```

## Vulnerability Scanning

```yaml
# GitHub Dependabot config (.github/dependabot.yml)
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

```bash
# Manual scanning
npm audit
npm audit fix
pip install safety && safety check
dependency-check --project MyProject --scan ./src
snyk test
```

## Dependency Pruning

```bash
# Find unused dependencies
npx depcheck
npm uninstall unused-package
pip install pipdeptree && pipdeptree
pip list --not-required
```

```javascript
// Bad: Import entire library for one function
import _ from 'lodash';  // 71KB
const result = _.debounce(func, 1000);

// Good: Import specific function
import debounce from 'lodash/debounce';  // 2KB

// Better: Use native JavaScript
function debounce(func, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), delay);
  };
}
```

## Subresource Integrity (SRI) for CDN

```html
<!-- Bad: Load from CDN without integrity check -->
<script src="https://cdn.example.com/lib.js"></script>

<!-- Good: SRI ensures CDN hasn't been compromised -->
<script
    src="https://cdn.example.com/lib.js"
    integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/uxy9rx7HNQlGYl1kPzQho1wx4JwY8wC"
    crossorigin="anonymous">
</script>
```

## Private Package Registries

```bash
# Use private registry for internal packages
npm config set @mycompany:registry https://npm.mycompany.com

# Prevent dependency confusion attacks
# Scope all internal packages: @mycompany/utils
```

## Common Mistakes

- **A06:2021 Vulnerable and Outdated Components is #6 OWASP Top 10** — Enables remote code execution
- **Not using lock files** — Different developers get different versions. Malicious package can be injected
- **Running `npm install` as root** — Packages can run arbitrary code during install
- **Not reviewing dependency updates** — Dependabot PRs auto-merged without review
- **Installing dev dependencies in production** — `npm install --production` to skip devDependencies
- **Ignoring indirect dependencies** — Scan entire dependency tree
- **Not monitoring for advisories** — Subscribe to security advisories for your ecosystem
- **Typosquatting** — `npm install reqeusts` instead of `requests`. Double-check spelling
- **Dependency confusion** — Public package with same name as private. Use scoped packages
- **Not removing unused dependencies** — Dead code is still attack surface

## See Also

- Previous: [File Upload Security](file-upload-security.md) | Next: [Logging and Monitoring](logging-monitoring.md)
- Reference: [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- Reference: [Snyk](https://snyk.io/)
