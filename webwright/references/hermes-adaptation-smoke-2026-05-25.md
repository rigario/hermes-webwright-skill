# Hermes Webwright Adaptation Smoke Test — 2026-05-25

## Why this reference exists

This captures the reusable lesson from adapting Microsoft Webwright for Hermes: do not blindly symlink an upstream multi-client skill if its body is written for another host agent's tool names and slash-command semantics. Preserve the class-level Webwright contract, but translate the workflow into Hermes-native tools and verification gates.

## Primary-source findings

- Upstream repo: `https://github.com/microsoft/Webwright`.
- Upstream README says the same `skills/webwright/` folder can load in Hermes via symlink.
- Upstream bundled skill is written in Claude/Codex language: `Bash`, `Read`, `Write`, `/webwright:run`, `/webwright:craft`.
- Upstream README separately notes Claude/Codex named subcommands are inert in Hermes; Hermes loads only `SKILL.md`.

## Durable implementation pattern

For Hermes, adapt the skill text instead of using it verbatim when host-specific terms appear:

- Map `Bash` → `terminal`.
- Map `Read` on PNGs → `vision_analyze` for screenshot verification, and `read_file` for text logs/scripts.
- Map `Write`/`Edit` → `write_file`/`patch`.
- Treat `/webwright:run` and `/webwright:craft` as concepts, not Hermes slash commands.
- Keep the upstream Webwright core invariant: the final artifact is a rerunnable Playwright script with screenshots/logs, not an ephemeral browser state.

## Smoke-test recipe used

1. Ensure Playwright is importable in the active Hermes environment.
2. Install Firefox for Playwright with `playwright install firefox` if missing.
3. Create `.tmp/webwright/smoke/plan.md` with critical points.
4. Create `.tmp/webwright/smoke/final_runs/run_1/final_script.py` that:
   - launches `playwright.firefox.launch(headless=True)`,
   - sets viewport `1280x1800`,
   - loads a deterministic local `data:text/html` page,
   - asserts exact title and heading,
   - writes `final_script_log.txt`,
   - saves `final_execution_<step>_<action>.png` screenshots,
   - appends `FINAL_RESPONSE: Webwright skill smoke OK`.
5. Run the script from scratch.
6. Inspect final screenshot with vision and tick each critical point only after evidence is concrete.

## Passing artifacts observed

- `final_script.py` ran cleanly.
- `final_script_log.txt` contained all action lines plus final response.
- Three screenshots were produced under `final_runs/run_1/screenshots/`.
- Vision check confirmed heading text `Webwright skill smoke OK` was visible.
- A separate review agent found no required corrections.

## Pitfall

A setup failure like a missing Playwright browser binary is not a durable negative rule about Playwright. Capture the fix (`playwright install firefox`) and rerun the smoke test rather than recording that browser automation is unavailable.
