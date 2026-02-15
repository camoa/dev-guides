---
description: Choosing between DRY, WET (Write Everything Twice), and AHA (Avoid Hasty Abstractions) approaches
---

# DRY vs WET vs AHA

## When to Use

When deciding whether to abstract duplicated code or let it remain duplicated, especially early in a feature's lifecycle.

## Decision Framework

| If you... | Use | Why |
|-----------|-----|-----|
| Know the abstraction is correct (third+ instance, stable requirements) | **DRY** | Eliminates knowledge duplication, single source of truth |
| Have only 1-2 instances, requirements still evolving | **WET** (Write Everything Twice) | Preserves flexibility, prevents premature abstraction |
| See similar code but unsure if it represents same knowledge | **AHA** (Avoid Hasty Abstractions) | Wait for clarity, let patterns emerge naturally |
| Existing abstraction is wrong and causing pain | **WET -> DRY** | Inline duplication, understand variance, re-abstract correctly |
| Duplication is incidental (similar syntax, different intent) | **WET** | Forced unification would couple unrelated concepts |

## Philosophy Comparison

**DRY (Don't Repeat Yourself)**

- **Goal**: Every piece of knowledge has single representation
- **Strength**: Eliminates knowledge duplication, easier maintenance when correct
- **Weakness**: Premature or incorrect abstractions couple unrelated code
- **Best for**: Stable requirements, well-understood domains

**WET (Write Everything Twice)**

- **Goal**: Duplicate code 1-2 times before abstracting
- **Strength**: Keeps code flexible while requirements evolve
- **Weakness**: Can lead to actual knowledge duplication if never refactored
- **Best for**: New features, exploratory development, rapid prototyping

**AHA (Avoid Hasty Abstractions)**

- **Goal**: Prefer duplication over wrong abstraction, abstract when obvious
- **Strength**: Emphasizes understanding before abstracting
- **Weakness**: Requires discipline to recognize "right" moment
- **Best for**: Ongoing maintenance, balancing DRY and WET

## Pattern

```javascript
// SCENARIO: Building a notification system

// ITERATION 1: First use case (email notifications)
function sendEmailNotification(user, message) {
  const email = buildEmail(user.email, message);
  smtp.send(email);
  log.info(`Email sent to ${user.email}`);
}

// ITERATION 2: Second use case (SMS notifications) - WET approach
function sendSmsNotification(user, message) {
  const sms = buildSms(user.phone, message);
  smsApi.send(sms);
  log.info(`SMS sent to ${user.phone}`);
}
// DON'T abstract yet — let requirements emerge

// ITERATION 3: Third use case (push notifications) - AHA moment
// NOW the pattern is clear: different channels, same flow
// Abstract with confidence:

interface NotificationChannel {
  send(recipient: string, message: string): Promise<void>;
  format(recipient: string, message: string): any;
}

class EmailChannel implements NotificationChannel {
  async send(email: string, message: string) {
    const formatted = this.format(email, message);
    await smtp.send(formatted);
  }
  format(email: string, message: string) {
    return buildEmail(email, message);
  }
}

class SmsChannel implements NotificationChannel { /* ... */ }
class PushChannel implements NotificationChannel { /* ... */ }

// Generic notification sender (DRY)
async function sendNotification(
  channel: NotificationChannel,
  recipient: string,
  message: string
) {
  await channel.send(recipient, message);
  log.info(`Notification sent via ${channel.constructor.name}`);
}
```

## Common Mistakes

- **Abstracting at instance #1** — No evidence the abstraction fits multiple use cases; likely to be wrong
- **Never refactoring WET code** — Duplication becomes entrenched, leads to divergence and bugs
- **Mistaking similar syntax for same knowledge** — Code looks similar but serves different business purposes
- **Treating AHA as "never abstract"** — AHA means "wait for the right moment," not "avoid abstraction forever"
- **Ignoring the pain signal** — If changing duplicated code is painful, it's time to abstract (even if only 2 instances)

## See Also

- [Kent C. Dodds - AHA Programming](https://kentcdodds.com/blog/aha-programming)
- [Sandi Metz - The Wrong Abstraction](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction)
- [Dan Abramov - The WET Codebase](https://overreacted.io/the-wet-codebase/)
