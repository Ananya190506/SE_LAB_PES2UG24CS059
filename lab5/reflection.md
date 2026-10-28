# Lab 5 Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest:** The mechanical ones. Replacing `hashlib.md5` with `hashlib.sha256`, replacing `random.randint` with `secrets.randbelow`, removing the unused imports (`sys`, `logging`), adding docstrings and renaming functions to snake_case. Each was a small change with a clear instruction from the tool, and I could confirm the fix by rerunning the tool. Flake8's line-length warnings were also easy because they only needed lines shortened or split.

**Hardest:** The ones where fixing the warning meant changing how the program behaves.
- `eval()` in `calculate_dosage`. I could not just delete it, because the program still has to compute formulas like `250 * 2`. I had to write a small evaluator using the `ast` module that only allows numbers and `+ - * /`.
- Replacing `pickle` with `json`. The save and load code had to change, and the global `medicines` variable had to be handled differently (`clear()` and `update()` instead of reassigning it).
- The silent `try/except/pass` in `dispense_medicine`. Removing it exposed the real problem (dispensing a medicine that isn't in stock), so I had to decide what the correct behaviour should be: raise a clear error, and also refuse to dispense more than the stock available.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

Bandit's **B324** (weak MD5 hash, High severity) on `patient_id` is arguably a false positive or at least an overstated one. The MD5 hash was used to make an identifier from a name and phone number, not to protect a password or sign data, so the High rating exaggerates the risk. Bandit itself suggests `usedforsecurity=False` for cases like this. I still switched to SHA-256 because it costs nothing and removes the warning, but the severity did not match the real risk. Also, an unsalted hash of a name and phone number is easy to guess, so a hash alone is not real privacy protection.

Similar cases are **B311** on `generate_rx_number` (a prescription number is not a secret, though `secrets` is a harmless upgrade) and **B403** (the warning for simply importing `pickle`), which is noise once the actual `pickle.load` call is flagged separately.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **In the editor:** run Pylint and Flake8 live (for example through VS Code) so problems show up while I type.
- **Pre-commit hooks:** use the `pre-commit` framework so Flake8, Pylint and Bandit run on every commit and a commit with new issues is blocked.
- **In CI:** run all three tools in a pipeline such as GitHub Actions on every push and pull request. The build fails if Bandit finds Medium or High issues, if Flake8 reports anything, or if the Pylint score drops below an agreed threshold (for example 9.5).
- **In code review:** reviewers can then focus on design and logic instead of style.
- **Configuration:** keep a config file (`.pylintrc`, `setup.cfg` or `.flake8`) so the whole team uses the same rules. Any warning that is deliberately ignored (like the MD5 case) should be suppressed on that line with a comment explaining why, not turned off globally.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Pylint score** went from 4.83/10 to 10.00/10. **Bandit** went from 8 findings (2 High, 2 Medium, 4 Low) to none, and **Flake8** went to a clean report.
- **Security:** no more arbitrary code execution through `eval`, no shell command injection through `os.system`, no unsafe `pickle` loading, and the hardcoded password is gone because the code now reads it from an environment variable.
- **Robustness:** the program no longer accepts negative stock or a numeric medicine name (`404`). It reports an error instead of failing silently when a medicine is missing (Insulin), refuses to dispense more than the stock available, and refuses to bill expired medicine. Medicines at zero stock are also no longer deleted from the report. None of these logic bugs were reported by the tools. I only found them by running the program and reading its output carefully, so static analysis helps but does not replace testing.
- **Readability and maintainability:** consistent naming, docstrings on every function, f-strings, `with` blocks that close files automatically, no `global` statement, and a `main()` guard so importing the module doesn't run the demo. The shared mutable default `audit=[]` is also fixed, so audit logs no longer leak between calls.
