# Webwright CLI Tool Mode

Use this when the user asks to craft, parameterize, reuse, or turn a browser task into a CLI.

## Plan Add-on

Add a Parameters table:

```markdown
# Parameters
| name | type | source phrase | default | allowed / format |
|------|------|---------------|---------|------------------|
| query | str | "..." | "..." | free text |
```

## Script Shape

- One reusable function with typed args and a Google-style docstring.
- `argparse` under `if __name__ == '__main__':`.
- No browser launch, network call, or file write at import time.
- First log line: `step 0 params: name=value ...`.
- Running with no args reproduces the original task.

## Import Safety Smoke Test

```bash
python - <<'PY'
import importlib.util
spec = importlib.util.spec_from_file_location('fs', 'final_runs/run_1/final_script.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print([n for n in dir(mod) if not n.startswith('_')])
PY
```

This must complete without launching a browser or writing files.
