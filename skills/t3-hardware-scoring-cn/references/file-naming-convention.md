# 报告文件命名规范

## 目的

确保 T3 审计报告的文件名与目录结构**固定且可复现**，便于自动化处理与 leaderboard 调用。

---

## 报告目录

```
tmp/reports/t3-{YYYY-MM-DD}-{case-id}/
```

- `YYYY-MM-DD`：审计日期
- `case-id`：`case-001`、`case-002` 等序号，或从 URL 生成的 slug（如 `nunatechnology`）

---

## 固定文件名清单

| 编号 | 文件名 | 说明 |
|------|--------|------|
| 00 | `00-isolation-manifest.md` | 隔离声明、页面清单版本 |
| 01 | `01-level0-source-urls.md` | 固定格式：按 S1..Sn 表格，含 URL、类型、status |
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
| 99 | `99-audit-report.md` | **唯一**最终报告（含 YAML 元数据 + 文字分析） |

---

## 禁止使用的别名

- 禁止：`99-report-summary.md`、`99-audit-summary.md` 等
- 统一：`99-audit-report.md`

---

## 与 00-isolation-manifest 的配合

创建新报告时，`00-isolation-manifest.md` 中的 File access rules 须与本清单一致，Level 0 为 01、02，Level 1 为 10、11、20–22、30、40–42、50、99。
