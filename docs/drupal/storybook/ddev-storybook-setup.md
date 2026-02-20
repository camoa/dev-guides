---
description: DDEV port exposure, ddev-storybook addon, and BrowserSync vs Storybook workflow comparison
drupal_version: "11.x"
---

# DDEV + Storybook Setup

## When to Use

> Use this guide when running `drupal/storybook` or `storybook-addon-sdc` inside a DDEV project and needing the Storybook UI accessible in the browser from outside the container.

## Decision

| Tool | Purpose | Port | When to Use |
|---|---|---|---|
| BrowserSync | CSS hot reload, general theme dev | 3000 | Daily theme development — CSS changes, template tweaks |
| Storybook | Component isolation, story browsing, design-dev handoff | 6006 | When reviewing component states, writing stories, sharing with designers |

These can run simultaneously. BrowserSync does not replace Storybook for component isolation; Storybook does not replace BrowserSync for CSS dev.

| Setup approach | When to use |
|---|---|
| Manual port exposure in `.ddev/config.yaml` | You want full control, no addon |
| `tyler36/ddev-storybook` addon | Automated setup, no local Node.js required |

## Pattern

### Option 1 — Manual Port Exposure

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

Add `--host 0.0.0.0` to your `package.json` start script — required so the server binds to all interfaces:

```json
{
  "scripts": {
    "storybook": "storybook dev --port 6006 --host 0.0.0.0"
  }
}
```

Run manually inside DDEV:

```bash
ddev exec -d /var/www/html/web/themes/custom/my_theme npm run storybook
```

### Option 2 — ddev-storybook Addon (Automated)

```bash
ddev add-on get tyler36/ddev-storybook
ddev restart
```

Provides:
- Port exposure (6006/6007) — automatic
- `ddev storybook` — starts the Storybook dev server inside the container
- `ddev storybook build` — production build of stories
- Node.js inside the container — no local Node.js required

```bash
ddev storybook         # starts dev server (watch mode)
ddev storybook build   # production static build
```

## Common Mistakes

- **Wrong**: Not exposing port 6006 in `.ddev/config.yaml` → **Right**: Storybook runs inside the container but is unreachable from the browser without explicit port exposure.
- **Wrong**: Binding Storybook to `localhost` instead of `0.0.0.0` → **Right**: Traffic from outside the container is blocked unless the server binds to all interfaces.
- **Wrong**: Running `drupal/storybook` module without CORS configured in Drupal → **Right**: The Storybook UI loads but all story fetches fail; configure `cors.config` in `development.services.yml`.
- **Wrong**: Accessing HTTPS port (6007) without trusting the DDEV certificate → **Right**: Browser shows "connection refused" — DDEV's self-signed cert must be trusted first.

## See Also

- [storybook-addon-sdc (Offline)](addon-sdc-offline.md)
- [Sub-Theme Stories](subtheme-stories.md)
- Reference: `https://github.com/tyler36/ddev-storybook`
- Reference: `https://ddev.readthedocs.io/en/stable/users/extend/custom-ports/`
