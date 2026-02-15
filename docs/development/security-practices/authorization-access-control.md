---
description: Authorization patterns including RBAC, ABAC, ACLs, least privilege, IDOR prevention, and resource ownership checks.
---

# Authorization and Access Control

## When to Use

Every operation that accesses resources must check authorization — reading data, modifying data, deleting data, accessing admin features. Authentication answers "who are you?", authorization answers "what can you do?"

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Role-based permissions | **RBAC (Role-Based Access Control)** | Simple, manageable - users have roles (admin, editor, viewer) |
| Fine-grained permissions | ABAC (Attribute-Based Access Control) | Complex rules - based on attributes (department, location, time) |
| Resource ownership | Ownership checks + RBAC | Users can only modify their own resources |
| Hierarchical permissions | Permission inheritance | Organizations -> teams -> users |
| API access control | Scopes + claims (OAuth/JWT) | Granular API permissions |

## RBAC Pattern

```python
ROLES = {
    'admin': ['create', 'read', 'update', 'delete', 'admin_panel'],
    'editor': ['create', 'read', 'update'],
    'viewer': ['read']
}

def require_permission(permission):
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = get_current_user()
            user_permissions = ROLES.get(user['role'], [])
            if permission not in user_permissions:
                return {"error": "Forbidden"}, 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/api/articles', methods=['POST'])
@require_permission('create')
def create_article():
    article = request.json
    db.execute("INSERT INTO articles (...) VALUES (...)", article)
    return {"id": article_id}, 201
```

**Resource ownership checks:**

```python
@app.route('/api/articles/<int:article_id>', methods=['PUT'])
@require_authentication
def update_article(article_id):
    user = get_current_user()
    article = db.execute("SELECT * FROM articles WHERE id = ?", [article_id]).fetchone()
    if not article:
        return {"error": "Not found"}, 404
    if article['author_id'] != user['id'] and user['role'] != 'admin':
        return {"error": "Forbidden - not your article"}, 403
    # Proceed with update
```

## ABAC Pattern

```python
def check_access(user, resource, action):
    rules = [
        {
            'condition': lambda u, r: u['role'] == 'dept_head' and u['department'] == r['department'],
            'allows': ['approve', 'read']
        },
        {
            'condition': lambda u, r: u['role'] == 'manager' and r['team_id'] in u['managed_teams'],
            'allows': ['read', 'update']
        },
        {
            'condition': lambda u, r: 9 <= datetime.now().hour < 17,
            'allows': ['create', 'update', 'delete']
        }
    ]
    for rule in rules:
        if rule['condition'](user, resource) and action in rule['allows']:
            return True
    return False
```

## Access Control Lists (ACLs)

```sql
CREATE TABLE permissions (
    id INTEGER PRIMARY KEY,
    resource_type VARCHAR(50),
    resource_id INTEGER,
    user_id INTEGER,
    permission VARCHAR(20),
    UNIQUE(resource_type, resource_id, user_id, permission)
);
```

```python
def has_permission(user_id, resource_type, resource_id, permission):
    result = db.execute("""
        SELECT COUNT(*) as count FROM permissions
        WHERE resource_type = ? AND resource_id = ? AND user_id = ? AND permission = ?
    """, [resource_type, resource_id, user_id, permission]).fetchone()
    return result['count'] > 0
```

## Principle of Least Privilege

```python
# Bad: Default allow
def can_access_admin_panel(user):
    if user['role'] == 'banned':
        return False
    return True  # Everyone else can access - WRONG

# Good: Default deny
def can_access_admin_panel(user):
    allowed_roles = ['admin', 'superadmin']
    return user['role'] in allowed_roles
```

## Insecure Direct Object References (IDOR)

```python
# Vulnerable - no ownership check
@app.route('/api/orders/<int:order_id>')
def get_order(order_id):
    order = db.execute("SELECT * FROM orders WHERE id = ?", [order_id]).fetchone()
    return jsonify(order)
# Attack: Change order_id in URL to access other users' orders

# Fixed - verify ownership
@app.route('/api/orders/<int:order_id>')
def get_order_secure(order_id):
    user = get_current_user()
    order = db.execute("""
        SELECT * FROM orders WHERE id = ? AND user_id = ?
    """, [order_id, user['id']]).fetchone()
    if not order:
        return {"error": "Not found"}, 404  # Don't leak existence
    return jsonify(order)
```

**Use UUIDs instead of sequential IDs:**

```python
import uuid
invoice_id = str(uuid.uuid4())  # '550e8400-e29b-41d4-a716-446655440000'
# Unpredictable, can't enumerate
```

## Common Mistakes

- **A01:2021 Broken Access Control is #1 OWASP Top 10** — Most common vulnerability, found in 3.81% of applications tested
- **Client-side access control** — Hiding UI elements is NOT security. Always enforce server-side
- **No re-authorization for sensitive actions** — Password change, email change should require re-entering password
- **Trusting user-supplied IDs** — Never use `request.json['user_id']` for access control. Get user from session/token
- **Horizontal privilege escalation** — User A modifying User B's data (IDOR). Always check resource ownership
- **Vertical privilege escalation** — Regular user accessing admin functions. Check role/permissions on EVERY request
- **Missing function-level access control** — API endpoint `/api/admin/delete-user` not checking if user is admin
- **Not checking access on file downloads** — `/uploads/invoices/123.pdf` accessible without authentication
- **Caching access control decisions** — User permissions change. Don't cache for > 5 minutes

## See Also

- Previous: [Authentication Best Practices](authentication-best-practices.md) | Next: [Sensitive Data Protection](sensitive-data-protection.md)
- Reference: [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- Reference: [OWASP A01:2021 Broken Access Control](https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/)
