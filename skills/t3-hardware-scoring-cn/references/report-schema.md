# 99-audit-report.md YAML Schema

## 目的

供网站 leaderboard 解析 `99-audit-report.md` 的 YAML 元数据块。字段名与类型固定，便于程序化读取与校验。

---

## 文件结构

```markdown
---
# YAML 元数据块（必须可被 --- 解析）
...
---

# 文字分析内容（Markdown）
...
```

---

## YAML 字段规范

### 顶层字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `case_id` | string | 是 | 如 `t3-2026-02-21-case-003` |
| `source_url` | string | 是 | 产品/项目来源 URL |
| `audit_date` | string (YYYY-MM-DD) | 是 | 审计日期 |
| `site_type` | string | 否 | `Shopify` \| `Kickstarter` |
| `product_category` | string | 是 | Brand-Blinded 产品类别 |
| `price_usd` | number \| null | 否 | 价格（USD），无则 null |
| `classification` | object | 是 | 见下表 |
| `scores` | object | 是 | 见下表 |
| `chart_data` | object | 是 | 见下表 |
| `litmus_tests` | object | 是 | 见下表 |
| `checklist_tables` | object | 否 | 各 Auditor 完整检查项表格，便于图表 |

### classification

| 字段 | 类型 | 说明 |
|------|------|------|
| `primary` | string | `Tool` \| `Toy` \| `Trash` |
| `secondary` | array of string | 如 `["Toy"]` |
| `final_label` | string | 如 `Trash + Toy` |

### scores

| 字段 | 类型 | 说明 |
|------|------|------|
| `tool` | number | Tool Auditor 总分 (0-100) |
| `toy` | number | Toy Auditor 总分 (0-100) |
| `trash` | number | Trash Auditor 总分 (0-100) |
| `composite` | number | max(tool, toy) - trash |

### chart_data

用于 radar/bar chart 的维度小分。

| 字段 | 类型 | 说明 |
|------|------|------|
| `tool` | object | `{ total, dimensions }` |
| `toy` | object | `{ total, dimensions }` |
| `trash` | object | `{ total, dimensions }` |

**dimensions** 键名固定：

- **tool**: `痛点识别与解决`, `注重细节与一致性`, `简洁高效`, `工程可靠性`
- **toy**: `感官愉悦`, `惊喜与发现`, `情感联结`, `可探索性`
- **trash**: `原则违背`, `问题制造`, `价值缺失`, `可替代性`

示例：

```yaml
chart_data:
  tool:
    total: 43
    dimensions:
      痛点识别与解决: 11
      注重细节与一致性: 14
      简洁高效: 13
      工程可靠性: 5
  toy:
    total: 54
    dimensions:
      感官愉悦: 20
      惊喜与发现: 14
      情感联结: 13
      可探索性: 7
  trash:
    total: 58
    dimensions:
      原则违背: 14
      问题制造: 14
      价值缺失: 16
      可替代性: 14
```

### litmus_tests

| 字段 | 类型 | 说明 |
|------|------|------|
| `tool` | string | 如 `否`、`是` |
| `toy` | string | 如 `可能`、`是`、`否` |
| `trash` | string | 如 `无影响或略好`、`更好`、`更糟` |

### checklist_tables（可选）

完整检查项得分，便于网站渲染表格或细粒度图表。

```yaml
checklist_tables:
  tool:
    - { id: "1.1", name: "是否识别出明确的具体痛点？", max: 10, score: 5, reason: "..." }
    - ...
  toy:
    - ...
  trash:
    - ...
```

---

## 文字分析部分结构

固定章节标题，内容从 `extract_for_report` 聚合：

- `## 产品概述`
- `## Tool 要点`
- `## Toy 要点`
- `## Trash 要点`
- `## Final Judge 判断理由`
- `## 改进建议`

---

## 校验清单

网站解析时建议检查：

- [ ] YAML 块以 `---` 开始和结束
- [ ] `case_id`、`source_url`、`audit_date`、`classification`、`scores`、`chart_data`、`litmus_tests` 存在
- [ ] `scores.tool`、`scores.toy`、`scores.trash` 为 0–100 数字
- [ ] `chart_data.*.dimensions` 键名与上述固定列表一致
