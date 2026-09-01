---
description: Security logging and monitoring including structured JSON logging, event types, data redaction, log rotation, real-time alerting, SIEM integration, and audit trails.
tldr: "Security logging and monitoring are MANDATORY for every application. **A09:2021 Security Logging and Monitoring Failures** — insufficient logging allows breaches to go undetected for months."
---

# Logging and Monitoring

## When to Use

Security logging and monitoring are MANDATORY for every application. **A09:2021 Security Logging and Monitoring Failures** — insufficient logging allows breaches to go undetected for months. IBM 2025 report: average breach detection time is **204 days**.

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Log security events | Structured logging (JSON) | Machine-parseable, queryable |
| Monitor for attacks | SIEM (Security Information and Event Management) | Correlate events, detect patterns |
| Alert on incidents | Real-time alerting (PagerDuty, Slack) | Rapid response |
| Audit trail | Immutable append-only logs | Forensics, compliance |
| Log sensitive data | **DON'T** | Logs often have weak access control |

## What to Log

| Event Type | What to Log | Why |
|---|---|---|
| **Authentication** | Login success/failure, logout, session creation | Detect brute force, credential stuffing |
| **Authorization** | Access denials, permission changes | Detect privilege escalation |
| **Input validation** | Validation failures, rejected input | Detect injection attacks |
| **Data access** | PII/sensitive data reads | Audit trail, insider threats |
| **Admin actions** | User creation/deletion, permission changes, config changes | Accountability |
| **Application errors** | Exceptions, stack traces (sanitized) | Detect exploitation attempts |
| **Rate limiting** | Rate limit triggers | Detect abuse |
| **File uploads** | File uploads, MIME mismatches | Detect malicious files |

## Structured Logging

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
        }
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'event_type'):
            log_data['event_type'] = record.event_type
        return json.dumps(log_data)

logger = logging.getLogger('security')
handler = logging.FileHandler('/var/log/app/security.log')
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
```

## Security Event Logging

```python
# Authentication events
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    ip_address = request.remote_addr

    user = authenticate(username, password)

    if user:
        logger.info('Successful login', extra={
            'event_type': 'auth_success',
            'user_id': user.id,
            'username': username,
            'ip_address': ip_address,
            'user_agent': request.headers.get('User-Agent')
        })
        return redirect('/dashboard')
    else:
        logger.warning('Failed login attempt', extra={
            'event_type': 'auth_failure',
            'username': username,
            'ip_address': ip_address,
            'user_agent': request.headers.get('User-Agent')
        })
        return 'Invalid credentials', 401

# Authorization failures
@app.route('/admin/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not current_user.is_admin:
        logger.warning('Unauthorized access attempt', extra={
            'event_type': 'authz_failure',
            'user_id': current_user.id,
            'requested_resource': f'/admin/delete-user/{user_id}',
            'ip_address': request.remote_addr
        })
        return 'Forbidden', 403

    # Proceed with deletion
    logger.info('User deleted', extra={
        'event_type': 'admin_action',
        'actor_user_id': current_user.id,
        'target_user_id': user_id,
        'action': 'delete_user'
    })

# Input validation failures
@app.route('/api/articles', methods=['POST'])
def create_article():
    try:
        validate_json(request.json, article_schema)
    except ValidationError as e:
        logger.warning('Input validation failure', extra={
            'event_type': 'validation_failure',
            'user_id': current_user.id,
            'endpoint': '/api/articles',
            'error': str(e),
            'ip_address': request.remote_addr
        })
        return {'error': 'Invalid input'}, 400
```

## What NOT to Log

```python
# Bad: Logging passwords
logger.info(f'Login attempt: {username} with password {password}')  # NEVER!

# Bad: Logging credit cards, session tokens, PII
logger.info(f'Payment processed: card {credit_card_number}')  # NEVER!

# Good: Log user ID, not PII
logger.info(f'User data accessed', extra={'user_id': user.id})

# Good: Redact sensitive fields
def sanitize_data(data):
    sensitive_fields = ['password', 'credit_card', 'ssn', 'token']
    sanitized = data.copy()
    for field in sensitive_fields:
        if field in sanitized:
            sanitized[field] = '[REDACTED]'
    return sanitized
```

## Log Rotation and Retention

```python
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# Rotate by size (10MB max, keep 5 backups)
handler = RotatingFileHandler('/var/log/app/security.log',
    maxBytes=10*1024*1024, backupCount=5)

# Rotate by time (daily, keep 90 days)
handler = TimedRotatingFileHandler('/var/log/app/security.log',
    when='midnight', interval=1, backupCount=90)
```

**Retention policies:**

- **Security logs:** 90+ days (compliance requirements)
- **Audit logs:** 1-7 years (depending on industry)
- **Application logs:** 30 days
- **Debug logs:** 7 days

## Real-Time Monitoring

```python
def check_brute_force(username, ip_address):
    key = f'{username}:{ip_address}'
    failed_logins[key] = failed_logins.get(key, 0) + 1
    if failed_logins[key] >= 5:
        alert_security_team(
            f'Brute force detected: {username} from {ip_address}',
            severity='high')

def detect_privilege_escalation(user_id):
    recent_failures = db.execute("""
        SELECT COUNT(*) FROM security_logs
        WHERE user_id = ? AND event_type = 'authz_failure'
        AND timestamp > datetime('now', '-1 hour')
    """, [user_id]).fetchone()[0]
    if recent_failures >= 10:
        alert_security_team(
            f'Possible privilege escalation: user {user_id}',
            severity='critical')
```

## Audit Trails

```python
def create_audit_record(action, actor_id, resource_type, resource_id, changes):
    db.execute("""
        INSERT INTO audit_logs (action, actor_id, resource_type, resource_id,
            changes, timestamp, signature)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [action, actor_id, resource_type, resource_id,
        json.dumps(changes), datetime.utcnow(),
        generate_signature(action, actor_id, resource_id)])
```

## Log Analysis

```bash
# Query JSON logs with jq
cat security.log | jq 'select(.event_type == "auth_failure")'

# Count failed logins by IP
cat security.log | jq -r 'select(.event_type == "auth_failure") | .ip_address' | sort | uniq -c | sort -rn

# Find users with multiple access denials
cat security.log | jq -r 'select(.event_type == "authz_failure") | .user_id' | sort | uniq -c | sort -rn
```

## Common Mistakes

- **Not logging authentication events** — Can't detect brute force attacks
- **Logging passwords or tokens** — Logs have weak access control. Attacker gets logs = full compromise
- **Only logging errors** — Need success events too for baseline and anomaly detection
- **No log monitoring** — Logs are useless if no one reads them. Set up alerts
- **Logging to application database** — Database breach exposes logs. Use separate log storage
- **No log integrity protection** — Attacker modifies logs to hide tracks. Use HMAC signatures
- **Generic log messages** — "Error occurred" is useless. Include context: user ID, IP, resource
- **Not correlating events** — Login from New York, 5 minutes later from Russia. Correlate by user ID
- **Verbose logging in production** — DEBUG-level logs with PII. Use INFO/WARNING/ERROR in production

## See Also

- Previous: [Dependency Security](dependency-security.md) | Next: [Cryptography Basics](cryptography-basics.md)
- Reference: [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- Reference: [OWASP A09:2021 Security Logging and Monitoring Failures](https://owasp.org/Top10/2021/A09_2021-Security_Logging_and_Monitoring_Failures/)
