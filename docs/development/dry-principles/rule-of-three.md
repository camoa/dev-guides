---
description: Deciding when to refactor duplicated code into an abstraction using the three strikes rule
---

# Rule of Three

## When to Use

When deciding whether it's time to refactor duplicated code into an abstraction.

## The Principle

**"Three strikes and you refactor"** — attributed to Don Roberts, popularized by Martin Fowler in "Refactoring."

| Instance | Action | Reasoning |
|----------|--------|-----------|
| **First** | Write the code | No pattern yet, no evidence of reuse |
| **Second** | Note the duplication | Pattern might be emerging, but still unclear |
| **Third** | Refactor to abstraction | Now you understand the variance and commonalities |

## Decision Framework

| If... | Then... | Why |
|-------|---------|-----|
| This is the first time you've needed this logic | Write it inline | No evidence it will be reused |
| This is the second time | Duplicate it (WET approach) | Wait to see if a third instance clarifies the pattern |
| This is the third time | Abstract it (DRY approach) | You now have enough context to abstract correctly |
| Requirements are still changing rapidly | Wait even longer | Abstraction may ossify before requirements stabilize |
| All instances always change together | Abstract sooner | Strong signal they represent same knowledge |
| Instances sometimes diverge | Keep separate longer | May be incidental duplication |

## Why Wait for Three?

**After one instance**: You have no idea if the pattern will recur.

**After two instances**: You don't yet understand the variance. Are these truly the same knowledge, or coincidentally similar? What parts are stable, what parts vary?

**After three instances**: You can see the pattern clearly. You understand what's common, what's variable, and what the abstraction should look like.

## Pattern

```python
# ITERATION 1: First instance — write it
def export_users_csv(users):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Email', 'Name'])
    for user in users:
        writer.writerow([user.id, user.email, user.name])
    return output.getvalue()

# ITERATION 2: Second instance — duplicate it (WET)
def export_products_csv(products):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'SKU', 'Name', 'Price'])
    for product in products:
        writer.writerow([product.id, product.sku, product.name, product.price])
    return output.getvalue()

# NOTE: Don't abstract yet! Wait to see if third instance clarifies pattern

# ITERATION 3: Third instance — NOW abstract
def export_orders_csv(orders):
    # Pattern is now clear: headers + row transformation
    pass  # Don't implement — refactor instead!

# REFACTORED: Abstract with confidence
def export_to_csv(items, headers, row_mapper):
    """
    Generic CSV exporter.

    Args:
        items: Iterable of objects to export
        headers: List of column headers
        row_mapper: Function that transforms item to list of values
    """
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    for item in items:
        writer.writerow(row_mapper(item))
    return output.getvalue()

# Usage — clean and DRY
users_csv = export_to_csv(
    users,
    ['ID', 'Email', 'Name'],
    lambda u: [u.id, u.email, u.name]
)

products_csv = export_to_csv(
    products,
    ['ID', 'SKU', 'Name', 'Price'],
    lambda p: [p.id, p.sku, p.name, p.price]
)

orders_csv = export_to_csv(
    orders,
    ['ID', 'Customer', 'Total'],
    lambda o: [o.id, o.customer_id, o.total]
)
```

## Exceptions to the Rule

**Abstract earlier when:**

- All instances are guaranteed to change together (true knowledge duplication)
- It's a well-known, stable pattern (e.g., retry logic, logging)
- Code is in hot path and performance demands consolidation
- Legal/compliance requires single source (e.g., tax calculation)

**Wait longer when:**

- Requirements are highly volatile
- Instances serve different business domains
- Cost of wrong abstraction is high (public API, shared library)
- Team is still learning the domain

## Common Mistakes

- **Abstracting at instance #1 or #2** — High chance of wrong abstraction, will need to undo later
- **Rigidly applying "three" as law** — Context matters; use judgment
- **Never refactoring even after many instances** — Technical debt accumulates, maintenance nightmare
- **Treating "three" as maximum** — If 5-6 instances exist with no abstraction, you're late to refactor
- **Ignoring the "pain signal"** — If duplication causes real pain (bugs, hard to change), abstract regardless of count

## See Also

- [DRY vs WET vs AHA](dry-vs-wet-vs-aha.md)
- [Rule of Three - Wikipedia](https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming))
- [Clarifying the Rule of Three in Refactoring](https://blog.thecodewhisperer.com/permalink/clarifying-the-rule-of-three-in-refactoring)
