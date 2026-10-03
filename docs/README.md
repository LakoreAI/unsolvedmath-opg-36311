# docs/

Everything document-related lives in `docs/`. Nothing that is a document
(write-up, note, report, figure, table, log) should live outside this tree.

## Layout

```
docs/
├── RESEARCH.md           project question, scope, method
├── NOTES.md              decisions log (append newest at top)
├── EXPERIMENTS.md        runbook for gated experiments
├── analysis/             analysis artifacts
│   └── <yyyy-mm-dd>/<topic>/...{md|txt|csv|png|...}
└── reports/              write-ups / reports
    └── <yyyy-mm-dd>/<topic>/...{md|txt|csv|png|...}
```

## Convention for analysis and reports

Analysis outputs and reports are placed under a date then a topic:

```
docs/analysis/<yyyy-mm-dd>/<topic>/...
docs/reports/<yyyy-mm-dd>/<topic>/...
```

Examples:

- `docs/analysis/2026-10-03/lr-sweep/curves.png`
- `docs/analysis/2026-10-03/lr-sweep/summary.md`
- `docs/reports/2026-10-03/lr-sweep/report.md`

Rules:

- The first path segment under `analysis/` / `reports/` is a `YYYY-MM-DD` date.
- Group files by topic in a directory beneath the date.
- Any format is allowed inside a topic folder (`.md`, `.txt`, `.csv`, images, ...).
- Keep raw results in these folders and link to them from `RESEARCH.md` /
  `EXPERIMENTS.md` rather than copying numbers by hand.
