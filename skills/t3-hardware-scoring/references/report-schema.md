# 99-audit-report.md YAML Schema

## Purpose

Enables leaderboard parsing of `99-audit-report.md` YAML metadata. Field names and types are fixed for programmatic use, specifically aligned with the T3 Deterministic Scoring Architecture.

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
| --- | --- | --- | --- |
| `case_id` | string | Yes | e.g. `t3-2026-02-21-case-003` |
| `source_url` | string | Yes | Product/project source URL |
| `audit_date` | string (YYYY-MM-DD) | Yes | Audit date |
| `site_type` | string | No | `Shopify` |
| `product_category` | string | Yes | Brand-blinded product category |
| `price_usd` | number | null | No |
| `classification` | object | Yes | See below |
| `scores` | object | Yes | See below |
| `chart_data` | object | Yes | See below |
| `litmus_gates` | object | Yes | See below |
| `checklist_tables` | object | No | Full Auditor checklist tables with `verbatim_evidence` |

### classification

| Field | Type | Description |
| --- | --- | --- |
| `primary` | string | `Tool` |
| `secondary` | array of string | e.g. `["Toy", "Trash"]` |
| `final_label` | string | e.g. `Tool + Trash` |
| `eagle_eye_veto_activated` | boolean | `true` if Trash Auditor flagged a critical issue overriding the math |
| `confidence` | string | `High` |

### scores

*Note: Include BOTH raw and normalized scores. Raw scores are from auditors (max 33/33/42). Normalized scores are Final Judge outputs (0-100). synthesize_results.py computes normalization automatically from raw scores.*

| Field | Type | Description |
| --- | --- | --- |
| `tool_raw` | number | Raw Tool score (0-33) |
| `tool_max` | number | Always 33 |
| `tool_normalized` | number | Normalized Tool score (0-100) |
| `toy_raw` | number | Raw Toy score (0-33) |
| `toy_max` | number | Always 33 |
| `toy_normalized` | number | Normalized Toy score (0-100) |
| `trash_raw` | number | Raw Trash score (0-42) |
| `trash_max` | number | Always 42 |
| `trash_normalized` | number | Normalized Trash score (0-100) |
| `composite` | number | max(tool_normalized, toy_normalized) - trash_normalized |

### chart_data

Dimension raw subscores for radar/bar charts.

**Fixed dimension keys & Max Values**:

* **tool** (Max 33): `Pain point identification` (9), `Detail and consistency` (9), `Simplicity and efficiency` (9), `Engineering reliability` (6)
* **toy** (Max 33): `Sensory pleasure` (9), `Surprise and discovery` (9), `Emotional connection` (9), `Explorability` (6)
* **trash** (Max 42): `Principle violations` (18), `Problem creation` (9), `Value deficit` (9), `Replaceability` (6)

### litmus_gates

*Note: Strict boolean logic gates based purely on extracted verbatim evidence. Always use `litmus_gates` (not `litmus_tests`) for YAML/JSON consistency with synthesize_results.py.*

| Field | Type | Description |
| --- | --- | --- |
| `tool` | string | `"Yes"` or `"No"` |
| `toy` | string | `"Yes"` or `"No"` |
| `trash` | string | `"Yes"` or `"No"` |

### checklist_tables (optional)

Full checklist scores for table/chart rendering.

---

## Narrative Section Structure

Fixed section headers; content mapped from the JSON `extract_for_report` and Final Judge outputs:

* `## Product Overview`
* `## Final Judge Verdict & Reasoning` *(Must highlight if Eagle Eye Veto was activated)*
* `## Tool Highlights` *(Strengths/Weaknesses bullets)*
* `## Toy Highlights` *(Strengths/Weaknesses bullets)*
* `## Trash Highlights & Critical Issues` *(Must list specific Eagle Eye triggers if any)*
* `## Verbatim Evidence Log` *(Optional: highly recommended to list the core quotes that decided the primary classification)*

---

## Validation Checklist

* [ ] YAML block starts and ends with `---`
* [ ] `case_id`, `source_url`, `audit_date`, `classification`, `scores`, `chart_data`, `litmus_gates` exist.
* [ ] `classification.eagle_eye_veto_activated` is explicitly set to `true` or `false`.
* [ ] `scores.*_normalized` are 0–100 numbers (converted from raw 33/42).
* [ ] `litmus_gates` only contain `Yes` or `No`.
* [ ] `chart_data.*.dimensions` keys match the fixed lists above and do not exceed their new raw maximums (9 or 6).
