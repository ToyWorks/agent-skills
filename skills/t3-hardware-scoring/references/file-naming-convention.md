# Report File Naming Convention

## Purpose

Ensure T3 audit report filenames and directory layout are **fixed and reproducible** for automation and leaderboard integration.

---

## Report Directory

```
tmp/reports/t3-{YYYY-MM-DD}-{case-id}/
```

- `YYYY-MM-DD`: Audit date
- `case-id`: Sequence (e.g. `case-001`) or slug from URL (e.g. `nunatechnology`)

---

## Fixed Filenames

| # | Filename | Description |
|---|----------|-------------|
| 00 | `00-isolation-manifest.md` | Isolation statement, page list version |
| 01 | `01-level0-source-urls.md` | S1..Sn table: URL, type, status |
| 02 | `02-level0-extracts.md` | Raw text extracts per S1..Sn |
| 10 | `10-level1-brand-blinded-fact-sheet.json` | Debranded fact sheet |
| 11 | `11-level1-objective-data-and-completeness.json` | Objective data completeness |
| 20 | `20-auditor-tool.initial.json` | Tool initial score |
| 21 | `21-auditor-toy.initial.json` | Toy initial score |
| 22 | `22-auditor-trash.initial.json` | Trash initial score |
| 30 | `30-peer-review.cross-reviews.json` | Peer Review |
| 40 | `40-auditor-tool.optimized.json` | Tool optimized |
| 41 | `41-auditor-toy.optimized.json` | Toy optimized |
| 42 | `42-auditor-trash.optimized.json` | Trash optimized |
| 50 | `50-final-judge.json` | Final Judge |
| 99 | `99-audit-report.md` | **唯一** final report (YAML metadata + narrative) |

---

## Disallowed Aliases

- Do not use: `99-report-summary.md`, `99-audit-summary.md`, etc.
- Use only: `99-audit-report.md`

---

## Alignment with 00-isolation-manifest

When creating new reports, File access rules in `00-isolation-manifest.md` must match this list: Level 0 = 01, 02; Level 1 = 10, 11, 20–22, 30, 40–42, 50, 99.
