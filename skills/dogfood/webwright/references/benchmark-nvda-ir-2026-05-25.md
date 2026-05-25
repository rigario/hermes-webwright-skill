# NVIDIA IR Benchmark Notes — 2026-05-25

Benchmark task: start from NVIDIA Investor Relations, locate the latest Quarterly Results 10-Q, and extract structured filing metadata.

## Observed Result

Webwright-style scripted workflow outperformed regular browser operation once the task crossed into a PDF/report extraction boundary.

- Regular browser found the NVIDIA IR `Quarterly Results` section and 10-Q link, but the browser PDF viewer exposed only shell metadata/page count/accession-like title. `document.body.innerText` on the PDF page returned empty.
- Webwright used Playwright for source provenance, then downloaded the IR-linked PDF and parsed `pdfinfo` / `pdftotext` into a durable result.

Final extracted answer:

- NVIDIA Corporation Form 10-Q
- Accession/PDF title: `0001045810-26-000052`
- Filing date: `2026-05-20`
- Period ending: `2026-04-26` / April 26, 2026
- IR-linked PDF: `https://s201.q4cdn.com/141608511/files/doc_financials/2027/q1/927dc2d6-a76c-4006-9f34-8769b2c665fb.pdf`

## Efficiency Finding

- Regular browser full path: ~806s and still needed non-browser extraction to finish.
- Webwright clean final run: 7.50s.
- Webwright repeat run: 9.11s.
- Ratio: ~107.5x faster than full regular browser path; ~47.2x faster than link-only browser path.

## Pitfalls Found

1. Regexes around SEC cover pages can be subtly wrong. A naive registrant regex captured `Delaware` instead of `NVIDIA CORPORATION`.
2. First-page dates are not all filing dates. In this case `May 15, 2026` was shares-outstanding date, while `pdfinfo` subject gave the actual `filed on 2026-05-20` metadata.
3. Browser PDF viewers may not expose extractable text to accessibility/DOM snapshots. Treat report/PDF extraction as an artifact step, not only a page interaction step.

## Recommended Pattern for IR / SEC PDFs

- Use Playwright/browser only to prove official source provenance and extract the report link from the IR site.
- Download the linked PDF into the run folder.
- Run `pdfinfo` first; parse `Subject`, `Title`, pages, and creation date.
- Run `pdftotext -f 1 -l 2` for cover-page period/title/filer checks.
- Cross-check date labels: `filed on`, `period ending`, `shares outstanding as of`, and press-release dates are different facts.
