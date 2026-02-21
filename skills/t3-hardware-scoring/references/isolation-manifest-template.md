# Information Isolation Manifest (Case {case_id})

## Purpose

Guarantee that **no branded data** (brand names, trademarks, company names, domains, emails, app identifiers containing the brand, marketing slogans) is visible to the three auditors.

## Isolation model

### Level 0 — Sealed (raw/branded)

- Allowed content: original website text, product names, trademarks, domain/URLs, policy boilerplate, emails, app links/IDs, marketing copy.
- Allowed readers: **Brand-Blinding step** + **Final Judge (comparison only)**.
- Forbidden readers: **Tool Auditor**, **Toy Auditor**, **Trash Auditor**.

### Level 1 — Auditor-visible (brand-blinded)

- Allowed content: neutral product category description, objective specs, constraints, and **source IDs** (e.g. `S2`) without URLs/domains.
- Forbidden content: any brand identifier; any URL/domain; any email; any app identifier that includes the brand string.
- Allowed readers: all three auditors + peer review + final judge scoring.

## File naming (see [file-naming-convention.md](file-naming-convention.md))

| 编号 | 文件名 | 说明 |
|------|--------|------|
| 00 | `00-isolation-manifest.md` | 隔离声明 |
| 01 | `01-level0-source-urls.md` | 按 S1..Sn 表格，含 URL、类型、status |
| 02 | `02-level0-extracts.md` | 按 S1..Sn 分块原始文本 |
| 10 | `10-level1-brand-blinded-fact-sheet.json` | 去品牌化事实表 |
| 11 | `11-level1-objective-data-and-completeness.json` | 客观数据完整性 |
| 20 | `20-auditor-tool.initial.json` | Tool 初评 |
| 21 | `21-auditor-toy.initial.json` | Toy 初评 |
| 22 | `22-auditor-trash.initial.json` | Trash 初评 |
| 30 | `30-peer-review.cross-reviews.json` | Peer Review |
| 40 | `40-auditor-tool.optimized.json` | Tool 优化 |
| 41 | `41-auditor-toy.optimized.json` | Toy 优化 |
| 42 | `42-auditor-trash.optimized.json` | Trash 优化 |
| 50 | `50-final-judge.json` | Final Judge |
| 99 | `99-audit-report.md` | 唯一最终报告（含 YAML + 文字分析） |

## File access rules

### Level 0 (sealed)

- `01-level0-source-urls.md`
- `02-level0-extracts.md`

### Level 1 (auditor-visible + output)

- `10-level1-brand-blinded-fact-sheet.json`
- `11-level1-objective-data-and-completeness.json`
- `20-auditor-tool.initial.json`
- `21-auditor-toy.initial.json`
- `22-auditor-trash.initial.json`
- `30-peer-review.cross-reviews.json`
- `40-auditor-tool.optimized.json`
- `41-auditor-toy.optimized.json`
- `42-auditor-trash.optimized.json`
- `50-final-judge.json`
- `99-audit-report.md`

## Leakage check (self-audit)

Before writing/using any Level 1 file:

- [ ] Replace brand/product/trademark names with neutral descriptors.
- [ ] Replace URLs/domains with `S#` source IDs only.
- [ ] Remove vendor email addresses.
- [ ] Remove app package names / TestFlight codes if they contain brand strings (keep only "app listing exists" as a fact).
- [ ] Remove marketing slogans; keep only testable claims.
