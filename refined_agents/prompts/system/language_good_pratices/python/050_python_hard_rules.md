---
id: python_hard_rules
priority: 50
tags: [always, python]
---

# Python Engineering Rules — Hard Constraints

These rules are **non-negotiable** and apply to all Python production code.

---

# Correctness and Safety

- Production code must not rely on implicit behavior when explicit behavior is clearer.
- Do not use global mutable state to coordinate business logic.
- Do not hide side effects inside utility functions.
- Avoid monkey patching unless the project explicitly requires it and the behavior is isolated and documented.

---

# Error Handling

- Do not use exceptions for normal control flow.
- Do not swallow exceptions using:
except:
except Exception:


unless all of the following are true:

- the exception is logged with context
- the exception is intentionally handled or transformed
- a comment explains why broad catching is required.

Every raised exception must include **useful diagnostic context**.

Libraries should raise **typed exceptions** when domain-specific failures matter.

Applications may translate internal exceptions into:

- user-facing errors
- API errors
- infrastructure failures.

---

# Logging

`print()` must **never be used for application logging** in production code.

All logs must go through a **centralized logging system**.

Logging must follow these rules:

- Use Python’s `logging` module or an approved structured logging framework.
- Logging configuration must be centralized in a dedicated logging module.
- Log format, handlers, and log levels must be configured through environment-driven configuration.
- Application modules must obtain loggers using:

```python
import logging
logger = logging.getLogger(__name__)

Logging messages must include useful operational context.
Prefer structured logging where important contextual fields are included separately.
Example:


```python
logger.info(
    "Order executed",
    extra={"order_id": order_id, "asset": asset_name}
)
```

The following must never be logged:
secrets
passwords
private keys
authentication tokens
sensitive user data.
Forbidden Patterns
The following are forbidden in production code:
print() for application logging
bare except:
pass inside exception handlers
eval() or exec() on untrusted input
assert for runtime validation
from module import *
TODO placeholders without a tracked issue
commented-out code used as history.
Input Validation
Never trust external input.
All inputs must be validated when coming from:
APIs
files
message queues
databases
environment variables
third-party services.
Deserialization must always be followed by validation.
Dependency Policy
Dependencies introduce risk and must be justified.
Before adding a dependency evaluate:
maintenance status
ecosystem adoption
security history
transitive dependency cost.
Prefer standard library solutions when they are sufficient.
Avoid obscure or unmaintained packages.
State and Mutability
Shared mutable state must be minimized.
Mutable default values in function signatures are forbidden.
Example of forbidden code:

```python
def add_item(item, items=[]):
    items.append(item)
```

Always use explicit initialization.
Incomplete Code
The following must not appear in production paths:
NotImplementedError
incomplete features without guards
placeholder implementations
dead feature flags.
