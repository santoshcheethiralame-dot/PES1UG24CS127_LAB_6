# Lab 6 coverage evidence

Run from `Lab 6` with Python 3.8+, pytest, and coverage.py available:

```powershell
python -m coverage run --data-file=.coverage_code --source=water_utility_billing -m pytest -q CodeCoverageTest_PES1UG24CS127_application.py
python -m coverage report --data-file=.coverage_code
python -m coverage run --branch --data-file=.coverage_branch --source=water_utility_billing -m pytest -q BranchCoverageTest_PES1UG24CS127_application.py
python -m coverage report --data-file=.coverage_branch
```

Results: code coverage 100% (46/46 statements); branch coverage 100% (34/34 branches, 0 partial).
