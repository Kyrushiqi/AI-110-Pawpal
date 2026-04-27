# unittest.TestCase — Beginner Notes
Full official docs: https://docs.python.org/3/library/unittest.html

---

## What is unittest.TestCase?

Think of it like a **checklist template** for testing your code.

Python comes with a built-in testing tool called `unittest`. To use it, you create a class that
inherits from `unittest.TestCase`. That class becomes a container for a group of related tests,
and inheriting from `TestCase` gives your class a set of ready-made checking tools
(the `assert*` methods) plus automatic setup and cleanup behavior.

In plain terms:
- **`unittest`** = the testing toolbox that comes with Python (no install needed)
- **`TestCase`** = the base class you inherit from to get access to that toolbox
- **test methods** = functions inside your class whose names start with `test_`; Python finds and runs them automatically

```python
import unittest

class MyTests(unittest.TestCase):      # inherit from TestCase
    def test_addition(self):           # must start with "test_"
        self.assertEqual(1 + 1, 2)    # use the built-in checking tools
```

---

## Lifecycle — What Runs and When

You don't call these yourself. Python calls them for you in order.

```
setUpClass()        ← runs once before ALL tests in the class
    │
    ├── setUp()     ← runs before EACH test method
    ├── test_one()
    ├── tearDown()  ← runs after EACH test method (even if test failed)
    │
    ├── setUp()
    ├── test_two()
    ├── tearDown()
    │
tearDownClass()     ← runs once after ALL tests in the class
```

**Rule of thumb:** use `setUp()` to create fresh objects so each test starts clean and
doesn't accidentally depend on what a previous test did.

---

## Quick Reference — Assert Methods

Every method below is called on `self` inside a test. If the condition is NOT met, the test fails
and prints a helpful message telling you exactly what went wrong.

### Equality
| Method | Passes when |
|---|---|
| `self.assertEqual(a, b)` | `a == b` |
| `self.assertNotEqual(a, b)` | `a != b` |

### Boolean
| Method | Passes when |
|---|---|
| `self.assertTrue(x)` | `x` is truthy |
| `self.assertFalse(x)` | `x` is falsy |

### None checks
| Method | Passes when |
|---|---|
| `self.assertIsNone(x)` | `x is None` |
| `self.assertIsNotNone(x)` | `x is not None` |

### Membership
| Method | Passes when |
|---|---|
| `self.assertIn(a, b)` | `a in b` |
| `self.assertNotIn(a, b)` | `a not in b` |

### Type check
| Method | Passes when |
|---|---|
| `self.assertIsInstance(obj, Type)` | `isinstance(obj, Type)` |

### Comparisons
| Method | Passes when |
|---|---|
| `self.assertGreater(a, b)` | `a > b` |
| `self.assertGreaterEqual(a, b)` | `a >= b` |
| `self.assertLess(a, b)` | `a < b` |
| `self.assertLessEqual(a, b)` | `a <= b` |

### Exceptions
Use this when you *expect* your code to raise an error:
```python
with self.assertRaises(ValueError):
    pet.addTask(task_with_duplicate_priority)
```
The test passes if `ValueError` is raised inside the `with` block. It fails if no error is raised.

### Custom failure messages
Every assert method accepts an optional `msg=` argument shown when the test fails:
```python
self.assertEqual(len(pet.tasks), 1, msg="addTask() did not append the task")
```

---

## `assert` (keyword) vs `self.assert*` (TestCase methods)

These look similar but are very different.

| | `assert` keyword | `self.assertEqual()` etc. |
|---|---|---|
| What it is | Built-in Python statement | Method inherited from `TestCase` |
| Available everywhere? | Yes, works in any Python file | Only inside a `TestCase` subclass |
| Failure message | Generic: `AssertionError` | Detailed: shows actual vs expected values |
| Can be turned off? | Yes (`python -O` disables all `assert`) | No, always runs |
| Best used for | Quick sanity checks in regular code | Writing proper tests |

**Example of the difference in failure output:**

```python
# Using the assert keyword — vague output
assert len(pet.tasks) == 1
# AssertionError   ← that's all you get

# Using TestCase method — clear output
self.assertEqual(len(pet.tasks), 1)
# AssertionError: 0 != 1   ← tells you exactly what the values were
```

**Bottom line:** always use `self.assert*` methods inside tests. Save the bare `assert` keyword
for non-test code where you just want a quick guard.

---

## Things Every Beginner Should Know

### 1. Test methods MUST start with `test_`
Python's test runner scans for methods named `test_*`. If you name a method `check_something()`
it will be silently ignored and never run.

### 2. Each test should check one thing
If a test checks five things at once and fails, you won't know which of the five broke.
One assertion per test (or a tight group of closely related assertions) makes failures easy to diagnose.

### 3. Tests should not depend on each other
Never write a test that assumes another test ran first. Each test must be able to run on its own
in any order. That's what `setUp()` is for — it rebuilds the state fresh every time.

### 4. A passing test is only as good as its assertions
A test with no assertions always passes, even if your code is completely broken. Make sure
your test actually checks something meaningful.

### 5. How to run your tests
```bash
# Run a specific test file
python -m pytest tests/test_pawpal.py -v

# Run all tests in the project
python -m pytest -v

# Using unittest directly (no pytest needed)
python -m unittest tests/test_pawpal.py
```

### 6. Reading test output
```
PASSED  — the assertions held, code behaves as expected
FAILED  — an assertion was wrong, output shows expected vs actual
ERROR   — the test crashed before it could even assert (e.g. an import error)
```

---

## Is unittest Part of the Development Cycle?

Yes — testing is a standard step in the everyday coding loop:

```
Write / change code
        ↓
Run tests  (python -m pytest -v)
        ↓
All pass? → commit and move on
        ↓
A test fails? → read the failure message → fix the code → run again
```

This cycle is called **Red → Green → Refactor**:
- **Red**: write a test that fails (because the feature doesn't exist yet)
- **Green**: write just enough code to make it pass
- **Refactor**: clean up the code, keep running tests to make sure nothing broke

unittest (and pytest, which can run unittest-style tests) is the standard tool for this in Python.
You don't need to install anything — `unittest` ships with Python itself.