# Hermes Webwright Skill

A Hermes-native adaptation of the Webwright pattern: use Playwright as an agent power-browser, then promote stable workflows into reproducible scripts with screenshots, logs, downloaded artifacts, and structured `result.json` output.

This repository contains a single Hermes skill:

```text
webwright/SKILL.md
```

It is designed for Hermes agents that need more reliable web browsing than ephemeral browser snapshots, especially for noisy sites, multi-step extraction, PDFs/reports, QA flows, and workflows that may later become reusable tools.

## What Webwright Means Here

Webwright has two operating modes:

1. **Lightweight browsing mode** — short scratch Playwright scripts used as a better browser for noisy, flaky, multi-step, or extraction-heavy pages.
2. **Durable script mode** — a final rerunnable `final_script.py` with `plan.md`, `final_script_log.txt`, screenshots, downloaded artifacts, and structured `result.json`.

The practical policy is:

> Use the lightest browser layer that gives enough reliability. Browse with Webwright when it makes the current task cleaner; promote to a final script when the source path stabilizes, the task repeats, or audit-grade evidence is needed.

## When To Use It

Use this skill when:

- normal browser snapshots are noisy, slow, flaky, or missing key data;
- the task spans multiple interactions, result pages, filters, date ranges, or downloads;
- structured extraction is needed from anchors, tables, PDFs, reports, or page metadata;
- selectors, filters, dates, quantities, currencies, or sort controls must be verified exactly;
- another agent or human must be able to audit the evidence later;
- a recurring cron or pipeline may reuse the browser path.

Do not use it for quick one-page lookups where standard Hermes browser tools are enough.

## Install

Copy the skill into your Hermes skills directory:

```bash
mkdir -p ~/.hermes/skills
cp -R webwright ~/.hermes/skills/
```

Or, if you prefer symlinking during development:

```bash
mkdir -p ~/.hermes/skills
ln -sfn "$PWD/webwright" ~/.hermes/skills/webwright
```

Start a new Hermes session after installing so the skill loader sees it.

## Prerequisites

In the Hermes environment where the agent runs:

```bash
python -c "import playwright; print('playwright ok')"
playwright install firefox
```

Firefox is the default recommendation because some protected sites reject Playwright Chromium.

## Repository Layout

```text
.
├── README.md
├── LICENSE
├── webwright/
│   ├── SKILL.md
│   └── references/
│       ├── benchmark-ai-articles-2026-05-25.md
│       ├── benchmark-nvda-ir-2026-05-25.md
│       ├── cli-tool-mode.md
│       ├── hermes-adaptation-smoke-2026-05-25.md
│       ├── playwright-patterns.md
│       └── verification-template.md
├── examples/
│   ├── lightweight_browse.py
│   └── final_script_skeleton.py
└── scripts/
    └── validate_skill.py
```

## Initial Benchmark Learnings Included

The skill includes two early local benchmark notes so future agents do not rediscover the same operational lessons. These are **initial tests from one Hermes environment**, not universal performance guarantees. The exact ratios should be treated as directional evidence that Webwright can materially reduce wall-clock time when a task benefits from deterministic Playwright extraction.

| Task | Regular browser path | Webwright path | Directional lesson |
|---|---:|---:|---|
| NVIDIA IR latest 10-Q PDF extraction | ~806s and still needed non-browser extraction | 7.50s clean final run; 9.11s repeat run | Very large speedup in this test, mainly because downloading/parsing the PDF crossed a browser-viewer boundary |
| Five AI articles from AP/CNBC/TechCrunch/The Verge/MIT Technology Review | ~1791s with manual handling/recovery | 99.90s clean final run | Significant speedup in this test, but source-specific filters/fallbacks mattered |

Key takeaways:

- Webwright is strongest when the answer crosses a browser boundary: PDFs, downloads, reports, filings, or structured artifacts.
- Multi-source news/article harvesting benefits from explicit source specs, candidate scoring, and saved `top_candidates`.
- Deterministic Playwright reruns consume effectively **0 LLM tokens** unless the agent inspects the output. The token cost is in authoring and verification.

## Safety / Privacy

This repository intentionally contains no credentials, tokens, cookies, browser profiles, private workspace artifacts, or local run outputs. It contains only the reusable skill, public benchmark notes, examples, and validation tooling.

Before publishing your own fork, run:

```bash
python scripts/validate_skill.py
```

And optionally scan for common secret patterns:

```bash
git grep -nE '(api[_-]?key|secret|token|authorization|password|cookie|BEGIN [A-Z ]*PRIVATE KEY)' -- . ':!README.md'
```

Review any matches manually. The README contains the words `token` and `secret` as documentation, not credentials.

## Attribution

This is a Hermes-native adaptation inspired by Microsoft Webwright's code-as-action browser agent pattern:

- https://github.com/microsoft/Webwright

The skill text is MIT licensed.
