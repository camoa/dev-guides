---
description: You're setting up build tools for a new Radix sub-theme
drupal_version: "11.x"
---

## 3.7 Build Tools and Compilation

### When to Use This Section
- You're setting up build tools for a new Radix sub-theme
- You need to configure Laravel Mix for SCSS/JS compilation
- You want to optimize production builds with PurgeCSS
- You're setting up live reload with BrowserSync

### Laravel Mix Configuration

#### Decision: Standard Laravel Mix Setup

**WHEN TO USE:**
- Radix sub-themes use Laravel Mix by default for SCSS/JS compilation
- You need build process for development and production
- You want automatic compilation on file changes

**File: `webpack.mix.js` (located in sub-theme root)**

```javascript
const mix = require('laravel-mix');

// Set public path for output
mix.setPublicPath('.');

// SCSS compilation
mix.sass('src/scss/main.style.scss', 'dist/css')
  .options({
    processCssUrls: false,
    postCss: [
      require('autoprefixer')({
        grid: true,
      }),
    ],
  });

// JavaScript compilation
mix.js('src/js/main.script.js', 'dist/js')
  .extract(); // Extract vendor libraries

// Source maps for development
if (!mix.inProduction()) {
  mix.sourceMaps();
}

// Production optimizations
if (mix.inProduction()) {
  mix.version(); // Cache busting
}
```

#### Decision: PurgeCSS Integration

**WHEN TO USE:**
- Production builds where CSS file size matters
- You want to remove unused Bootstrap classes
- You're concerned about page load performance

**WHY:** Bootstrap includes many utility classes you may not use. PurgeCSS removes unused CSS, reducing file size by 50-80%.

**Configuration:**

```javascript
const mix = require('laravel-mix');
require('laravel-mix-purgecss');

mix.setPublicPath('.');

mix.sass('src/scss/main.style.scss', 'dist/css')
  .options({
    processCssUrls: false,
    postCss: [
      require('autoprefixer')({
        grid: true,
      }),
    ],
  });

// PurgeCSS configuration
if (mix.inProduction()) {
  mix.purgeCss({
    // Scan these files for used classes
    content: [
      './templates/**/*.twig',
      './components/**/*.twig',
      './src/js/**/*.js',
      './THEME_NAME.theme', // Preprocess file
      './THEME_NAME.libraries.yml',
    ],
    // Preserve dynamic classes
    safelist: [
      /^col-/,           // Bootstrap grid
      /^btn-/,           // Bootstrap buttons
      /^alert-/,         // Bootstrap alerts
      /^dropdown-/,      // Bootstrap dropdowns
      /^modal-/,         // Bootstrap modals
      /^carousel-/,      // Bootstrap carousels
      /^accordion-/,     // Bootstrap accordions
      /^nav-/,           // Bootstrap navigation
      /^navbar-/,        // Bootstrap navbar
      /^card-/,          // Bootstrap cards
      /^fade/,           // Bootstrap transitions
      /^show/,           // Bootstrap show states
      /^active/,         // Bootstrap active states
      /^disabled/,       // Bootstrap disabled states
      /^js-/,            // JavaScript-added classes
      /^ajax-/,          // Drupal AJAX classes
      /^drupal-/,        // Drupal system classes
    ],
    // Preserve classes matching patterns
    safelist: {
      standard: [/^is-/, /^has-/],
      deep: [/^bs-/, /^carousel/, /^modal/],
      greedy: [/tooltip$/, /popover$/],
    },
  });
}
```

**CRITICAL SAFELISTS:**
- **Bootstrap JavaScript Components:** Classes added dynamically (fade, show, active)
- **Drupal System Classes:** ajax-processed, contextual-links, etc.
- **State Classes:** is-active, has-error, etc.

**WHY SAFELIST NEEDED:** PurgeCSS only scans static files. JavaScript-added classes get removed unless safelisted, breaking functionality.

#### Decision: BrowserSync Configuration

**WHEN TO USE:**
- You want live reload during development
- You're testing responsive designs across devices
- You want synchronized scrolling/clicks across browsers

**WHY:** Eliminates manual browser refresh, speeds up development, enables multi-device testing.

**Configuration:**

```javascript
const mix = require('laravel-mix');

mix.setPublicPath('.');

mix.sass('src/scss/main.style.scss', 'dist/css')
  .options({
    processCssUrls: false,
  });

// BrowserSync configuration
mix.browserSync({
  // Local development URL
  proxy: 'https://SITENAME.ddev.local',

  // Watch these files for changes
  files: [
    'dist/css/**/*.css',
    'dist/js/**/*.js',
    'templates/**/*.twig',
    'components/**/*.twig',
    '*.theme',
  ],

  // BrowserSync options
  open: false,              // Don't auto-open browser
  notify: false,            // Disable notification overlay
  reloadDelay: 0,           // Immediate reload
  injectChanges: true,      // Inject CSS without reload

  // HTTPS configuration (for DDEV)
  https: {
    key: '/path/to/.ddev/traefik/certs/SITENAME.ddev.local-key.pem',
    cert: '/path/to/.ddev/traefik/certs/SITENAME.ddev.local.pem',
  },
});
```

**DDEV SETUP:**

For DDEV projects, use this simplified configuration:

```javascript
mix.browserSync({
  proxy: 'https://SITENAME.ddev.local',
  files: [
    'dist/css/**/*.css',
    'templates/**/*.twig',
    'components/**/*.twig',
  ],
  open: 'external',
  host: 'SITENAME.ddev.local',
  notify: false,
});
```

**WHY PROXY:** BrowserSync proxies your local site, injecting live reload scripts without modifying your Drupal installation.

### Build Commands

#### Decision Table: Which Command to Use

| Task | Command | Use When |
|------|---------|----------|
| Active development | `npm run watch` | Making frequent SCSS/JS changes |
| Single build (dev) | `npm run dev` | One-time development build |
| Production build | `npm run production` | Before commit/deploy |
| Initial setup | `npm install` | First time or after package.json changes |

#### Pattern: Development Workflow

```bash
# 1. Install dependencies (first time only)
cd themes/custom/THEME_NAME
npm install

# 2. Start watch mode with BrowserSync
npm run watch

# 3. Make changes to SCSS/JS/Twig files
# (BrowserSync auto-reloads on save)

# 4. Before committing, build production
npm run production
git add dist/
git commit -m "Theme updates"
```

#### Pattern: Production Build Workflow

```bash
# Clean previous builds
rm -rf dist/css/* dist/js/*

# Build optimized production assets
npm run production

# Verify output
ls -lh dist/css/
ls -lh dist/js/

# Commit production assets
git add dist/
git commit -m "Production build: [description]"
```

### Common Mistakes

**1. Not installing npm packages in sub-theme**

```bash
# BAD: No package.json or node_modules in sub-theme
themes/custom/THEME_NAME/
└── webpack.mix.js  # Exists but npm install never run
```

**WHY:** Laravel Mix and dependencies must be installed locally in sub-theme.

**CORRECT:**

```bash
cd themes/custom/THEME_NAME
npm install  # Creates node_modules/ and installs dependencies
```

---

**2. Committing node_modules/ to git**

```bash
# BAD: Committing massive node_modules directory
git add node_modules/
git commit
```

**WHY:** Bloats repository with thousands of files (100+ MB). Dependencies should be installed via `npm install`, not committed.

**CORRECT:**

Add to `.gitignore`:
```
node_modules/
npm-debug.log
```

Commit only `package.json` and `package-lock.json`:
```bash
git add package.json package-lock.json
```

---

**3. Using watch mode in production**

```bash
# BAD: Running watch on production server
npm run watch &
```

**WHY:** Watch mode includes source maps, unminified code, and file watchers that consume resources. Never run watch in production.

**CORRECT:**

Production servers run compiled assets only:
```bash
npm run production  # Build locally before deploy
git add dist/       # Commit production build
# Deploy to production
```

---

**4. Not clearing Drupal cache after CSS changes**

```bash
# Change SCSS → compile → refresh browser → styles don't update
```

**WHY:** Drupal aggregates CSS files. Changes may not appear until cache cleared.

**CORRECT:**

```bash
npm run watch              # Compile CSS
drush cr                   # Clear Drupal cache
# OR disable CSS aggregation during development
drush config-set system.performance css.preprocess 0
```

---

**5. Wrong PurgeCSS safelist (breaks JavaScript components)**

```javascript
// BAD: No safelist for dynamic classes
mix.purgeCss({
  content: ['./templates/**/*.twig'],
  safelist: [], // Missing Bootstrap JS classes
});
```

**WHY:** Bootstrap JavaScript adds classes like `.show`, `.active`, `.fade`. PurgeCSS removes them, breaking modals, dropdowns, carousels.

**CORRECT:**

```javascript
mix.purgeCss({
  safelist: [
    /^show/, /^active/, /^fade/, /^collapse/,
    /^modal-/, /^dropdown-/, /^carousel-/,
  ],
});
```

### See Also
- [1.1 Sub-Theme Directory Structure](#11-sub-theme-directory-structure)
- [3.6 SCSS Compilation Modes](#36-radix-sub-theme-best-practices)
- [6.5 Performance Best Practices](#65-performance-best-practices)