# 99-audit-report.md YAML Schema

## Purpose

Enables leaderboard parsing of `99-audit-report.md` YAML metadata. Field names and types are fixed for programmatic use.

---

## File Structure

```markdown
---
# YAML metadata block (parsed between ---)
...
---

# Narrative content (Markdown)
...
```

---

## YAML Field Spec

### Top-level

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `case_id` | string | Yes | e.g. `t3-2026-02-21-case-003` |
| `source_url` | string | Yes | Product/project source URL |
| `audit_date` | string (YYYY-MM-DD) | Yes | Audit date |
| `site_type` | string | No | `Shopify` \| `Kickstarter` |
| `product_category` | string | Yes | Brand-blinded product category |
| `price_usd` | number \| null | No | Price (USD); null if unknown |
| `classification` | object | Yes | See below |
| `scores` | object | Yes | See below |
| `chart_data` | object | Yes | See below |
| `litmus_tests` | object | Yes | See below |
| `checklist_tables` | object | No | Full Auditor checklist tables for charts |

### classification

| Field | Type | Description |
|-------|------|-------------|
| `primary` | string | `Tool` \| `Toy` \| `Trash` |
| `secondary` | array of string | e.g. `["Toy"]` |
| `final_label` | string | e.g. `Trash + Toy` |

### scores

| Field | Type | Description |
|-------|------|-------------|
| `tool` | number | Tool total (0-100) |
| `toy` | number | Toy total (0-100) |
| `trash` | number | Trash total (0-100) |
| `composite` | number | max(tool, toy) - trash |

### chart_data

Dimension subscores for radar/bar charts.

**Fixed dimension keys**:
- **tool**: `Pain point identification`, `Detail and consistency`, `Simplicity and efficiency`, `Engineering reliability`
- **toy**: `Sensory pleasure`, `Surprise and discovery`, `Emotional connection`, `Explorability`
- **trash**: `Principle violations`, `Problem creation`, `Value deficit`, `Replaceability`

### litmus_tests

| Field | Type | Description |
|-------|------|-------------|
| `tool` | string | e.g. `No`, `Yes` |
| `toy` | string | e.g. `Maybe`, `Yes`, `No` |
| `trash` | string | e.g. `No effect or better`, `Better`, `Worse` |

### checklist_tables (optional)

Full checklist scores for table/chart rendering.

---

## Narrative Section Structure

Fixed section headers; content from `extract_for_report`:

- `## Product Overview`
- `## Tool Highlights`
- `## Toy Highlights`
- `## Trash Highlights`
- `## Final Judge Reasoning`
- `## Improvement Suggestions`

---

## Validation Checklist

- [ ] YAML block starts and ends with `---`
- [ ] `case_id`, `source_url`, `audit_date`, `classification`, `scores`, `chart_data`, `litmus_tests` exist
- [ ] `scores.tool`, `scores.toy`, `scores.trash` are 0–100 numbers
- [ ] `chart_data.*.dimensions` keys match the fixed lists above
