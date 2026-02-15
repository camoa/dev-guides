---
description: SQL injection prevention using parameterized queries, ORM safe patterns, dynamic identifier handling, and stored procedures.
---

# SQL Injection Prevention

## When to Use

EVERY database query that includes any untrusted data — user input, URL parameters, cookies, HTTP headers, data from external APIs, even data read from your own database (defense in depth).

## Why SQL Injection Is Critical

**Real-world impact:**

- **2025 BusinessOn breach:** SQL injection exposed 179,386 user accounts, 200M won fine
- **SQL injection is still rampant in 2025** despite being a solved problem since the 1990s
- Consequences: Data theft, data destruction, authentication bypass, remote code execution

**Attack example:**

```sql
-- Vulnerable query
SELECT * FROM users WHERE username = 'USER_INPUT' AND password = 'USER_INPUT'

-- Attacker input: username = admin' OR '1'='1 , password = anything
SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = 'anything'
-- Returns all users, authentication bypassed
```

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Execute SQL with user data | **Parameterized queries** (prepared statements) | Only safe option - separates SQL code from data |
| Use ORM (Django, Eloquent, Hibernate) | ORM query builder methods | Safe when used correctly (avoid raw SQL) |
| Dynamic table/column names | Allowlist validation + manual escaping | Parameterized queries don't work for identifiers |
| Reporting/analytics with complex SQL | Stored procedures + parameterized inputs | Encapsulates SQL logic, uses parameters |

## Pattern

**Parameterized queries (the ONLY safe approach for values):**

```python
# Python (sqlite3, psycopg2, MySQLdb)
# Good: Parameterized query
def get_user(username):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

# Bad: String concatenation
def get_user_bad(username):
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")  # SQL injection!
```

```php
// PHP (PDO)
// Good: Prepared statement
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = :username");
$stmt->execute(['username' => $username]);
$user = $stmt->fetch();

// Bad: String concatenation
$query = "SELECT * FROM users WHERE username = '$username'";  // SQL injection!
```

```javascript
// Node.js (MySQL2, pg)
// Good: Parameterized query
const [rows] = await connection.execute(
    'SELECT * FROM users WHERE username = ?',
    [username]
);

// Bad: Template literal
const query = `SELECT * FROM users WHERE username = '${username}'`;  // SQL injection!
```

**ORM usage (safe when done correctly):**

```python
# Django ORM - Good
user = User.objects.get(username=username)  # Parameterized automatically

# Django ORM - Bad: raw SQL
user = User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{username}'")  # SQL injection!

# Django ORM - Good: raw SQL with parameters
user = User.objects.raw("SELECT * FROM auth_user WHERE username = %s", [username])
```

```php
// Laravel Eloquent - Good
$user = User::where('username', $username)->first();  // Parameterized

// Laravel - Bad: raw query
$user = DB::select("SELECT * FROM users WHERE username = '$username'");  // SQL injection!

// Laravel - Good: raw with bindings
$user = DB::select("SELECT * FROM users WHERE username = ?", [$username]);
```

**Dynamic identifiers (table/column names) - CANNOT use parameterized queries:**

```python
ALLOWED_TABLES = ['users', 'products', 'orders']

def get_records(table_name):
    if table_name not in ALLOWED_TABLES:
        raise ValueError("Invalid table name")
    query = f"SELECT * FROM {table_name} WHERE active = ?"
    cursor.execute(query, (True,))
    return cursor.fetchall()
```

**Stored procedures (defense in depth):**

```sql
CREATE PROCEDURE GetUserByUsername(@username NVARCHAR(50))
AS
BEGIN
    SELECT * FROM users WHERE username = @username;
END
```

## Why Parameterized Queries Work

```python
# Parameterized query sends TWO separate messages to database:
# 1. SQL structure: "SELECT * FROM users WHERE id = ?"
# 2. Parameter value: "1 OR 1=1"

# Database treats "1 OR 1=1" as a LITERAL STRING VALUE, not SQL code
# Query looks for user with id = "1 OR 1=1" (doesn't exist, returns empty)
```

## Common Mistakes

- **Using parameterized queries sometimes** — 100% of queries with untrusted data MUST use parameters. One vulnerable query = compromised database
- **Concatenating LIKE patterns** — `WHERE name LIKE '%{user_input}%'` is injectable. Use: `WHERE name LIKE ?` with parameter `f'%{user_input}%'`
- **Second-order SQL injection** — Attacker stores malicious SQL in database via safe query. Later, vulnerable query reads and executes it
- **Trusting ORM completely** — ORMs are safe for standard queries but allow raw SQL. Django `extra()`, Laravel `DB::raw()` can be vulnerable if misused
- **Manual escaping functions** — `mysql_real_escape_string()`, `pg_escape_string()` are error-prone and bypassable. Use parameterized queries instead
- **Storing SQL queries in user-editable files** — Configuration files with SQL templates accessible to users can be exploited

## See Also

- Previous: [XSS Prevention Patterns](xss-prevention-patterns.md) | Next: [CSRF Prevention](csrf-prevention.md)
- Reference: [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- Reference: [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
