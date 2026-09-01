---
description: Mailgun transactional email for Drupal — module selection, DNS setup, configuration, programmatic sending, webhooks, bounce handling, and operations.
guide-meta:
  concepts:
    - mailgun
    - transactional email
    - drupal mail
    - MailManager
    - hook_mail
    - DKIM
    - SPF
    - DMARC
    - bounce handling
    - webhook
    - queue
    - mailsystem
    - symfony mailer
    - api key storage
    - mail routing
    - sandbox domain
    - dedicated IP
    - email deliverability
  not:
    - marketing automation
    - newsletter platforms
    - bulk email campaigns
    - CRM email sequences
  requires: []
  complements:
    - drupal/forms
    - drupal/services
  category: drupal
tracks:
  - project: mailgun
    channel: stable
    declared: 2.1.x
    verified: 2026-04-26
---

# Mailgun

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Choose between drupal/mailgun, Mailer Plus, or Symfony Mailer Lite | [Module Decision](module-decision.md) | Use drupal/mailgun 2.1.x as the default for 2026 Drupal sites; choose Mailer Plus only when you need Twig-templated emails, multi-language policies, or signing. Mixing both on the same site causes conflicts. |
| Set up SPF, DKIM, and DMARC DNS records | [DNS Setup](dns-setup.md) | Set up a subdomain (e.g., mg.example.com) with SPF TXT record, two DKIM CNAMEs via Automatic Sender Security, and a DMARC TXT at the organizational root; start DMARC at p=none and escalate only after monitoring. |
| Pick the right Mailgun region (US vs EU) | [Region Selection](region-selection.md) | Default to the US region unless GDPR or contractual requirements mandate EU data residency; the region choice is permanent per domain and a US API key will return 401 Unauthorized if used against the EU endpoint. |
| Install and enable the Mailgun module | [Module Installation](module-installation.md) | Require drupal/mailgun:^2.1 and drupal/mailsystem via Composer then enable both; use ^2.1 specifically to get the July 2025 release, and add Key module support via the open patch at issue |
| Configure settings.php for safe API key handling | [Settings Configuration](settings-configuration.md) | Always add mailgun to config_exclude_modules before saving the API key, then inject the key via getenv() in settings.php; skipping config_exclude_modules commits the API key to git on the next drush cex. |
| Route module emails through Mailgun via system.mail.yml | [Mail Routing](mail-routing.md) | Set system.mail.yml interface.default to mailgun_mail to route all Drupal mail through Mailgun, or use the Mailsystem module to route specific modules while keeping others on php_mail; never edit system.mail.yml without running drush cim or cex. |
| Configure the module via the admin UI | [UI Configuration](ui-configuration.md) | Navigate to /admin/config/services/mailgun and configure the Private/Sending API key, working domain, and API endpoint per environment; use settings.php env-var overrides rather than hardcoding values that differ between dev, stage, and prod. |
| Store the API key securely | [API Key Storage](api-key-storage.md) | Inject the Mailgun API key via getenv() in settings.php as the default method; never commit mailgun.settings.yml to git — add mailgun to config_exclude_modules first and rotate immediately if a key is accidentally committed. |
| Send transactional emails programmatically | [Programmatic Sending](programmatic-sending.md) | Implement hook_mail() to set subject/body/headers on $message, then call MailManager::mail() from a service injected with mail.manager; never call the Mailgun PHP SDK directly — it bypasses routing, test mode, and the queue. |
| Use Mailgun-specific features (tags, tracking, attachments) | [Mailgun-Specific Params](mailgun-specific-params.md) | Pass tags, tracking toggles, deliverytime, bcc, and custom headers via $params in MailManager::mail() and copy them to $message['params'] in hook_mail(); Mailgun limits 3 tags per message and rejects deliverytime set in the past. |
| Decide between direct send and queue worker | [Queue vs Direct Send](queue-vs-direct-send.md) | Use direct send for time-sensitive mail (password resets, OTPs, payment confirmations) and the queue plugin for high-volume or webhook-triggered mail; beware open issues |
| Receive Mailgun webhooks for delivery events | [Webhook Handling](webhook-handling.md) | Build a custom controller at a no-cache, no-CSRF route to receive Mailgun webhook POST requests; always verify the HMAC signature and reject events older than 5 minutes to prevent replay attacks — the drupal/mailgun module does not ship a webhook receiver as of 2.1.0. |
| Handle bounces, complaints, and unsubscribes | [Bounce & Complaint Handling](bounce-complaint-handling.md) | Immediately suppress hard bounces and complaints via hook_mail_alter() checking a field_mail_status field on User; reconcile nightly with Mailgun's /v3/<domain>/bounces API because webhooks can be missed. |
| Test and verify the setup end-to-end | [Verification & Testing](verification-testing.md) | Always run a direct curl test first to isolate Mailgun credential and DNS issues from Drupal, then confirm with drush eval through the full mail stack; API success ("Queued. Thank you.") does not mean delivered — check Mailgun Logs for actual delivery status. |
| Diagnose common errors (401, 421, 404, region mismatch) | [Common Errors](common-errors.md) | Most failures fall into four categories — region mismatch (401), DNS not propagated (421), wrong working_domain (404), and sandbox recipient restriction; start with a direct curl test to isolate the layer before debugging Drupal. |
| Compare Mailgun against SendGrid, Postmark, Brevo, raw SMTP | [Alternatives Comparison](alternatives-comparison.md) | Mailgun is the default developer-first choice for Drupal transactional email with EU region support and DKIM auto-rotation; choose Postmark for maximum deliverability on pure transactional, Brevo for budget/marketing-heavy sites or no-CC-required free tier, and SES only if already in the AWS ecosystem at scale. |
| Estimate cost and pick a plan tier | [Pricing & Tier Selection](pricing-tier-selection.md) | Go live on Free only with a CC on file (removes authorized-recipients restriction); upgrade to Basic ($15/10k) for volume or support needs, Foundation ($35/50k) when monthly sends exceed ~18k; skip dedicated IP until 100k+/month. |
