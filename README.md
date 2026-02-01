# simple_ctx_log

[![PyPI - Version](https://img.shields.io/pypi/v/simple_ctx_log)](https://pypi.org/project/simple_ctx_log)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simple_ctx_log)](https://pypi.org/project/simple_ctx_log)


A lightweight but **deeply introspective logger** for Python.

`simple_ctx_log` focuses on **context reconstruction**, not just file/line logging.
It is designed to answer the question:

> *“From which object, through which call stack, did this log originate?”*

No external dependencies.
No global state.
No magic decorators.
Just frames, objects, and clarity.

---

## Key Features

- 🔍 Full **call stack reconstruction** (functions and methods)
- 🧠 **Object context traversal** (parent objects, nested architectures)
- 🧵 Safe with recursion, deep nesting, and complex object graphs
- 🛑 Configurable limits:
  - maximum depth
  - stop at module boundary
- 📐 Highly readable **tree-style output**
- ⚡ High performance (uses `sys._getframe`, no `inspect.stack`)
- 🧪 Designed to be test-friendly
- 📦 Standard library only

This logger is particularly useful for:
- debugging complex object-oriented flows
- understanding “who called what” in large systems
- forensic-style debugging
- frameworks, factories, and deeply nested architectures

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Example Output](#example-output)
- [Configuration](#configuration)
- [Design Philosophy](#design-philosophy)
- [Limitations](#limitations)
- [License](#license)

---

## Installation

```console
pip install simple_ctx_log
````

---

## Quick Start

```python
from simple_ctx_log import Logger

logger = Logger()

def my_function(x):
    logger.log("Hello from my_function")

my_function(42)
```

---

## Example Output

For a deeply nested and recursive call:

```text
[2026-01-xxThh:mm:ss.mls] [INFO] [thread=MainThread]
│ module: tests.test_logger_nested_hell
│ call stack:
│ ├─ ExternalArchitect.<unknown>
│ │  attrs:
│ │    creator = 'Hell'
│ │    data = 'Data'
│ ├─ test_logger_called_from_function(capsys=<_pytest.capture.CaptureFixture>)
│ ├─ InternProcess.recursive_log_call(depth=3, msg='Entropy is inevitable.')
│ │  attrs:
│ │    parent = <ExternalArchitect>
│ ├─ InternProcess.recursive_log_call(depth=2, msg='Entropy is inevitable.')
│ │  attrs:
│ │    parent = <ExternalArchitect>
│ ├─ InternProcess.recursive_log_call(depth=1, msg='Entropy is inevitable.')
│ │  attrs:
│ │    parent = <ExternalArchitect>
│ └─ InternProcess.recursive_log_call(depth=0, msg='Entropy is inevitable.')
│    attrs:
│      parent = <ExternalArchitect>
│
└─ message:
   Retrieved message : Entropy is inevitable.
```

This output shows:

* the full call stack (module → logger call)
* recursive calls
* object hierarchy
* method arguments
* instance attributes
* a clean separation between context and message

---

## Configuration

### Logger options

```python
Logger(
    name: str | None = None,
    log_args: bool = True,
    log_attrs: bool = True,
    log_private_attrs: bool = False,
    max_depth: int | None = None,
    log_file: str | None = None,
    stdout: bool = True,
    signing_key: bytes | None = None
)
```

| Option              | Description                                     |
| ------------------- | ----------------------------------------------- |
| `name`              | Logger name (informational)                     |
| `log_args`          | Log function/method arguments                   |
| `log_attrs`         | Log instance attributes                         |
| `log_private_attrs` | Include private attributes (`_attr`)            |
| `max_depth`         | Maximum depth for call stack + object traversal |
| `log_file`          | optional file in which to write logs            |
| `stdout`            | Print logs                                      |
| `signing_key`       | Hash key                                        |

### Module boundary safety

The logger **does not cross module boundaries** by default.
This prevents polluting logs with internals such as:

* `asyncio`
* `threading`
* framework internals

The context stops at the last object belonging to the calling module.

---

## Design Philosophy

`simple_ctx_log` intentionally does **not**:

* wrap or replace `logging`
* rely on decorators
* inject global hooks
* inspect the heap (`gc`)
* traverse object graphs downward

Instead, it:

* walks **upward** through frames
* reconstructs **logical ownership**
* remains deterministic and bounded

The goal is **understanding**, not verbosity.

---

## Limitations

* Uses `sys._getframe` (CPython only)
* Output is currently text-based (no JSON yet)
* No built-in log levels filtering (by design, for now)
* No file handler yet (planned)

These are deliberate trade-offs to preserve performances.

---

## License

`simple_ctx_log` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
