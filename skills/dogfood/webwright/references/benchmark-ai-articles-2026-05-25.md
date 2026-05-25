# Five AI Articles Benchmark Notes — 2026-05-25

Benchmark task: compare regular browser vs Webwright for finding one AI-related article from five sources: AP News, CNBC, TechCrunch, The Verge, and MIT Technology Review.

## Observed Result

Webwright still won, but by less than in the NVIDIA IR/PDF benchmark.

- Regular browser: found all five with manual handling; ~1791s wall-clock including interruptions/recovery.
- Webwright: final clean run found all five in 99.90s.
- Ratio: ~17.9x faster.

## Final Webwright Articles

- AP News: `Could anything but profit steer AI? The OpenAI trial offered clues but no verdict`
- CNBC: `SoftBank Group shares soar 20% as Nvidia earnings signal strong AI momentum`
- TechCrunch: `Everyone is navigating AI security in real time — even Google`
- The Verge: `Hackers are learning to exploit chatbot ‘personalities’`
- MIT Technology Review: `Google I/O showed how the path for AI-driven science is shifting`

## Failure Modes / Lessons

1. News/category pages are noisier than IR/report pages. They mix nav links, topic pages, author links, stock quote pages, videos, ads, sponsored posts, and article links.
2. Candidate filters should distinguish text filters from URL filters. Applying a publisher-name exclusion to `text + href` excluded every TechCrunch article because all hrefs contain `techcrunch.com`.
3. Broad regexes like `AI` can match unintended substrings (`details` contains `ai`). Prefer `\bAI\b` or explicit phrases.
4. CNBC direct topic URL returned Not Found; on-site search was the practical source path.
5. Browser state can degrade during manual exploration (The Verge became an empty page after interaction), while script runs can retry and restart cleanly.

## Recommended Pattern for Multi-Source Article Harvests

- Start with an explicit source spec table: source, URL, allowed host, topical regex, text-only excludes, URL-only excludes.
- Use current page provenance screenshots per source.
- Extract anchors, then score candidates; keep `top_candidates` in `result.json` for auditability.
- Use `\bAI\b` rather than raw `AI`; include topic-specific alternates (`OpenAI`, `Nvidia`, `Google`, `Anthropic`, `chatbot`, etc.).
- Treat source-specific fallbacks (e.g., CNBC search page) as part of the final spec once discovered.
