---
description: Supply chain security including 7-day dependency cooldown, lock files, vulnerability scanning, dependency pruning, SRI, and private registries.
tldr: "Every project uses third-party dependencies — npm packages, PyPI libraries, Maven artifacts, gems, Go modules. **Supply chain attacks** are the fastest-growing threat in 2025."
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

**Attack evolution:**

- Traditional attacks: Typosquatting, dependency confusion
- 2025 trend: **Worm-like propagation** through build tools and package managers
- Attackers target developer tooling for high-leverage access downstream

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

## Package Source Verification

```bash
# npm - use only official registry
npm config set registry https://registry.npmjs.org/

# Verify package publisher
npm view package-name

# Check for typosquatting
# Installing "reqeusts" instead of "requests"
# Installing "python-dateutil" instead of "dateutil"

# Python - use only PyPI
pip install --index-url https://pypi.org/simple/ package-name

# Verify package authenticity
pip show package-name
```

## Signed Packages

```bash
# npm - verify package signatures (npm 7+)
npm config set audit-signatures true
npm audit signatures

# Python - verify package signatures with GPG
# (Most PyPI packages not signed - rely on HTTPS + lock files)

# Maven - verify signatures
mvn verify
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

<!-- Generate SRI hash -->
<!-- cat lib.js | openssl dgst -sha384 -binary | openssl base64 -A -->
```

## Dependency Policies

```json
// package.json - define acceptable licenses
{
  "license-checker": {
    "allowed": ["MIT", "Apache-2.0", "BSD-3-Clause"],
    "blocked": ["GPL", "AGPL"]  // Copyleft licenses
  }
}
```

```bash
# Check licenses
npx license-checker --production --onlyAllow 'MIT;Apache-2.0;BSD-3-Clause'
```

## Private Package Registries

```bash
# Use private registry for internal packages
npm config set @mycompany:registry https://npm.mycompany.com

# Prevent dependency confusion attacks
# Attacker publishes "mycompany-utils" to public npm
# Developer accidentally installs public malicious package instead of private

# Defense: Scope all internal packages
@mycompany/utils  # Private scoped package
```

## Common Mistakes

- **A06:2021 Vulnerable and Outdated Components is #6 OWASP Top 10** — Extremely common, enables remote code execution
- **Not using lock files** — Different developers get different versions. Malicious package can be injected between installs
- **Running `npm install` as root** — Packages can run arbitrary code during install. Use non-root user, sandbox
- **Not reviewing dependency updates** — Dependabot PRs auto-merged without review. Compromised package slips in
- **Installing dev dependencies in production** — `npm install --production` to skip devDependencies. Smaller attack surface
- **Ignoring indirect dependencies** — You depend on A, A depends on B (has vulnerability). Scan entire tree
- **Not monitoring for advisories** — Subscribe to security advisories for your ecosystem (GitHub Security Advisories, npm security alerts)
- **Typosquatting** — `npm install reqeusts` instead of `requests`. Attacker registers similar names. Double-check spelling
- **Dependency confusion** — Public package with same name as private package. Use scoped packages, configure registry priority
- **Not removing unused dependencies** — Dead code is still attack surface. Prune regularly

## See Also

- Previous: [File Upload Security](file-upload-security.md) | Next: [Logging and Monitoring](logging-monitoring.md)
- Reference: [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- Reference: [Sonatype 2026 State of the Software Supply Chain Report](https://www.sonatype.com/state-of-the-software-supply-chain/2026)
- Reference: [Snyk](https://snyk.io/)
