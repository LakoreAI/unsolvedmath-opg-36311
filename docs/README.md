# docs/

Everything document-related lives in `docs/`. Nothing that is a document
(write-up, note, report, figure, table, log) should live outside this tree.

## Layout

```
docs/
├── RESEARCH.md           project question, scope, method
├── TODO.md               plan and progress (mirrored at the repo root)
├── analysis/             measured output
│   └── <yyyy-mm-dd>/<topic>/...{md|txt|csv|png|...}
├── reports/              write-ups / reports and their PDFs
│   ├── validation.md     repo-wide validation record
│   └── <topic>/          one directory per paper
│       ├── <topic>.tex, <topic>.pdf
│       ├── figures/      generated figures
│       └── tables/       generated LaTeX tables
└── research/             deep-research workspaces
    └── <topic>/          outline.yaml, fields.yaml, results/, report.md, PLAN.md
```

## Convention for analysis and reports

Analysis outputs and reports are placed under a date then a topic:

```
docs/analysis/<yyyy-mm-dd>/<topic>/...
docs/reports/<yyyy-mm-dd>/<topic>/...
```

Examples:

- `docs/analysis/2026-10-03/subset-sum/bench.md`
- `docs/analysis/2026-10-03/subset-sum/dichotomy.csv`
- `docs/reports/baselines/paper.pdf`
- `docs/reports/representation/representation.pdf`

Rules:

- The first path segment under `analysis/` is a `YYYY-MM-DD` date; group files
  by topic beneath it.
- Each paper lives under `docs/reports/<topic>/`, with its generated `figures/`
  and `tables/` beside it.
- Any format is allowed inside a topic folder (`.md`, `.txt`, `.csv`, images, ...).
- Keep raw results in these folders and link to them from `RESEARCH.md` rather
  than copying numbers by hand.
