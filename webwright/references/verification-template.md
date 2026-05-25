# Webwright Verification Template

Use this in `plan.md` or the final report.

```markdown
# Task
<verbatim user task>

# Critical Points
- [ ] CP1: <requirement>
  - Evidence: `final_runs/run_<id>/screenshots/final_execution_1_<action>.png`; log line `step 1 action: ...`
- [ ] CP2: <requirement>
  - Evidence: ...

# Final Run
- Workspace: `<path>`
- Script: `<path>/final_runs/run_<id>/final_script.py`
- Log: `<path>/final_runs/run_<id>/final_script_log.txt`
- Final answer: `<value or n/a>`

# Blockers / Limits
- `<none or specific evidence-backed blocker>`
```

A CP is not complete until the evidence proves exact state. Hidden selections, broadened date ranges, or search-query-only filters are not enough.
