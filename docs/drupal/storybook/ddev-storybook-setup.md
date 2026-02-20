---
description: DDEV port exposure, ddev-storybook addon, and BrowserSync vs Storybook workflow comparison
drupal_version: "11.x"
---

# DDEV + Storybook Setup

## When to Use

> Use this guide when running `drupal/storybook` or `storybook-addon-sdc` inside a DDEV project and needing the Storybook UI accessible in the browser from outside the container.

## Decision

| Approach | When to Use |
|---|---|
| Manual port exposure in `.ddev/config.yaml` | You want minimal setup with full control |
| `tyler36/ddev-storybook` addon | You want automated setup with `ddev storybook` commands |

### BrowserSync vs Storybook

| Tool | Purpose | Port | When to Use |
|---|---|---|---|
| BrowserSync | CSS hot reload, general theme dev | 3000 | Daily theme development — CSS changes, template tweaks |
| Storybook | Component isolation, story browsing, design-dev handoff | 6006 | Reviewing component states, writing stories, sharing with designers |

These can run simultaneously. BrowserSync does not replace Storybook for component isolation; Storybook does not replace BrowserSync for CSS dev.

## Pattern

### Manual Port Exposure

```yaml
# .ddev/config.yaml
web_extra_exposed_ports:
  - name: storybook
    container_port: 6006
    http_port: 6006
    https_port: 6007
```

After adding: `ddev restart`

Storybook accessible at:
- `http://{project}.ddev.site:6006`
- `https://{project}.ddev.site:6007`

### Automated Setup — ddev-storybook Addon

```bash
ddev add-on get tyler36/ddev-storybook
ddev restart
```

Provides:
- Port exposure (6006/6007) — automatic
- `ddev storybook` — starts the dev server inside the container
- `ddev storybook build` — production build of stories
- Node.js inside the container — no local Node.js required

### Running Storybook

With the addon:

```bash
ddev storybook        # starts dev server (watch mode)
ddev storybook build  # production static build
```

Without the addon (manual):

```bash
ddev exec -d /var/www/html/web/themes/custom/my_theme npm run storybook
```

Add to `package.json` — the `--host 0.0.0.0` flag is required so the server is accessible outside the container:

```json
{
  "scripts": {
    "storybook": "storybook dev --port 6006 --host 0.0.0.0"
  }
}
```

## Common Mistakes

- **Wrong**: Not exposing port 6006 in `.ddev/config.yaml` → **Right**: Storybook runs inside the container but is unreachable from the browser without explicit port exposure
- **Wrong**: Binding Storybook to `localhost` → **Right**: Use `--host 0.0.0.0` so traffic from outside the container is allowed
- **Wrong**: Running `drupal/storybook` module without CORS configured in Drupal → **Right**: The Storybook UI loads but all story fetches fail without CORS headers; configure `development.services.yml`
- **Wrong**: Accessing HTTPS port (6007) without trusting the DDEV certificate → **Right**: Trust the DDEV self-signed cert first (`mkcert -install` or `ddev trust`)

## See Also

- [drupal/storybook Module](drupal-storybook-module.md)
- [storybook-addon-sdc (Offline)](addon-sdc-offline.md)
- [Sub-Theme Stories](subtheme-stories.md)
- Reference: https://github.com/tyler36/ddev-storybook
- Reference: https://ddev.readthedocs.io/en/stable/users/extend/custom-ports/
