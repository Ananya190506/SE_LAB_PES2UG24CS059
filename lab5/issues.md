# Lab 5: Static Code Analysis - Issues Table

**File analysed:** `pharmacy_manager.py`
**Tools used:** Pylint, Bandit, Flake8

## Baseline results (before fixes)

| Tool | Result |
|------|--------|
| Pylint | 4.83/10 |
| Bandit | 8 issues (2 High, 2 Medium, 4 Low) |
| Flake8 | 22 issues (unused imports, blank lines, line length, bare except) |

Issues are listed with high and medium severity first. Line numbers refer to the original file.

## Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `os.system` with `name` (B605, High) | Security | 68 | A shell command is built from the `name` input, so command injection is possible | Replace with `print(...)` |
| MD5 used for patient ID (B324, High) | Security | 51 | MD5 is a weak, broken hash | Use `hashlib.sha256` |
| `eval(formula)` (B307 / W0123, Medium) | Security | 48 | Executes arbitrary code taken from the doctor's note | Validate the formula with a regex, then multiply the two numbers |
| `pickle.load` (B301, Medium) | Security | 64 | A tampered `pharmacy.dat` can execute code when loaded | Switch to `json.dump` / `json.load` |
| `import pickle` (B403, Low) | Security | 3 | Bandit flags the pickle module itself | Removed by the switch to `json` |
| Hardcoded password (B105, Low) | Security | 11 | Password is stored in plain text in the source code | Read it from an environment variable and compare with `hmac.compare_digest` |
| `random` for Rx number (B311, Low) | Security | 54 | `random` is predictable and not suitable for security use | Use `secrets.randbelow` |
| Bare `except: pass` (B110 / W0702 / E722) | Bug | 27-28 | Swallows every error, so dispensing a missing medicine ("Insulin") fails silently | Catch `KeyError` only and report that the medicine was not found |
| Mutable default argument `audit=[]` (W0102) | Bug | 13 | One list is shared across every call to `addMedicine` | Default to `None` and create the list inside the function |
| Inconsistent return statements (R1710) | Bug | 13 | `addMedicine` returns `None` on one path and `audit` on another | Make every path return a value |
| Negative quantity and numeric name accepted | Bug | 13-20 | Output showed `Cetirizine 10mg -> -10 units` and a medicine named `404` | Check that `name` is a non-empty string and `qty >= 0` |
| Expired stock can be billed | Bug | 40-44 | Amoxicillin was billed after its expiry date | Call `is_expired` in `bill_amount` and reject expired items |
| Stock not reconciled on dispense and bill | Bug | 22-28, 40-44 | Dispensing more than available is not rejected, and billing does not reduce stock | Check available quantity before dispensing and deduct billed stock |
| `global` statement (W0603) | Quality | 63 | Rebinds a module-level variable inside a function | Use `medicines.clear()` and `medicines.update(...)` |
| File opened without `with` (R1732) | Quality | 57, 62 | The file may stay open if an error occurs | Use `with open(..., encoding="utf-8")` |
| Simplifiable if/else (R1703, R1705) | Quality | 35, 79 | `if ...: return True else: return False` is redundant | Return the expression directly |
| `main()` runs on import | Quality | 108 | There is no `__main__` guard, so importing the file runs the demo | Add `if __name__ == "__main__":` |
| Old-style `%` formatting (C0209) | Style | 19 | The string could be an f-string | Use an f-string |
| Unused imports `sys`, `logging` (W0611 / F401) | Style | 2, 6 | Dead imports | Delete them |
| camelCase function names (C0103) | Style | 13, 22, 30, 33, 40, 46, 50, 53, 56, 61, 67, 70, 78, 84 | 14 functions do not follow snake_case | Rename them and update every call in `main()` |
| Missing docstrings (C0114, C0116) | Style | 1 and every function | No module or function documentation | Add a module docstring and a short docstring for each function |
| Lines too long (C0301, E501) | Style | 19, 87, 98 | Lines exceed 79 characters | Split the lines |
| Missing blank lines (E302, E305) | Style | Many, and 108 | Two blank lines are needed around top-level definitions | Add blank lines (or run `black -l 79`) |

## Fix plan

1. **Commit 1, Bandit:** fix all 8 findings (`os.system`, MD5, `eval`, `pickle`, hardcoded password, `random`, bare `except`).
2. **Commit 2, Pylint:** rename functions, add docstrings, fix the mutable default, returns, `global`, `with open`, simplifiable ifs, f-string, unused imports, and add the `__main__` guard. Target score above 9.5.
3. **Commit 3, Flake8:** fix blank lines and line length until `flake8` prints nothing.

## Results after fixes

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.83/10 | _fill in_ |
| Bandit | 8 issues | _fill in_ |
| Flake8 | 22 issues | _fill in_ |
