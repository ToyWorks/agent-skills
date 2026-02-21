# Auditor Output Templates

## Purpose

Ensure **reproducible** and **stable** T3 audit results. Each Auditor must output scoring tables per this template. Table format is fixed; do not change column structure.

---

## General Rules

- **Required**: Each Auditor outputs a full report including the scoring table
- **Table columns**: Check ID | Check Name | Max | Score | Brief Reason (≤50 chars)
- **Brief reason**: One sentence plus evidence source (e.g. S1, S2)
- **Forbidden**: Empty cells; skipping checks; merging/splitting columns

---

## Tool Auditor Table

**Basis**: Tony Fadell "Build" checklist  
**Total**: 100 pts

| Check ID | Check Name | Max | Score | Brief Reason (≤50 chars) |
|----------|------------|-----|-------|--------------------------|
| 1.1 | Identifies clear, concrete pain points? | 10 |  |  |
| 1.2 | Solution directly targets pain point? | 10 |  |  |
| 1.3 | Better than existing solutions? | 10 |  |  |
| 2.1 | Every interaction thoughtfully designed? | 10 |  |  |
| 2.2 | Consistent design language? | 10 |  |  |
| 2.3 | Hides unnecessary complexity? | 5 |  |  |
| 3.1 | Follows "less is more"? | 10 |  |  |
| 3.2 | Operations efficient? | 10 |  |  |
| 3.3 | Design unobtrusive? | 5 |  |  |
| 4.1 | Stable and reliable? | 10 |  |  |
| 4.2 | Quality control emphasized? | 10 |  |  |
| **Total** |  | **100** |  |  |

**Reason examples**: `Pain point clear but no independent verification; S2`, `User feedback questions accuracy; S2`

---

## Toy Auditor Table

**Basis**: Don Norman "Design of Everyday Things" checklist  
**Total**: 100 pts

| Check ID | Check Name | Max | Score | Brief Reason (≤50 chars) |
|----------|------------|-----|-------|--------------------------|
| 1.1 | Visually appealing design? | 10 |  |  |
| 1.2 | Quality materials and craftsmanship? | 10 |  |  |
| 1.3 | Pleasant interaction feedback? | 10 |  |  |
| 2.1 | Surprising design elements? | 10 |  |  |
| 2.2 | Encourages exploration and discovery? | 10 |  |  |
| 2.3 | Hidden "easter eggs" or details? | 5 |  |  |
| 3.1 | Evokes positive emotions? | 10 |  |  |
| 3.2 | Builds emotional connection? | 10 |  |  |
| 3.3 | Personalization/customization? | 5 |  |  |
| 4.1 | Functional depth? | 10 |  |  |
| 4.2 | Encourages experimentation? | 10 |  |  |
| **Total** |  | **100** |  |  |

**Reason examples**: `Decorative form + multiple colors; S2`, `Haptic feedback has positive user feedback; S2`

---

## Trash Auditor Table

**Basis**: Dieter Rams principles violation checklist  
**Total**: 100 pts

| Check ID | Check Name | Max | Score | Brief Reason (≤50 chars) |
|----------|------------|-----|-------|--------------------------|
| 1.1 | Violates "innovative" principle? | 5 |  |  |
| 1.2 | Violates "useful" principle? | 5 |  |  |
| 1.3 | Violates "aesthetic" principle? | 5 |  |  |
| 1.4 | Violates "understandable" principle? | 5 |  |  |
| 1.5 | Violates "honest" principle? | 5 |  |  |
| 1.6 | Violates "durable" principle? | 5 |  |  |
| 2.1 | Creates new problems? | 10 |  |  |
| 2.2 | Adds user burden? | 10 |  |  |
| 2.3 | Unnecessary complexity? | 5 |  |  |
| 3.1 | Clear value proposition? | 10 |  |  |
| 3.2 | Worth the user's cost? | 10 |  |  |
| 3.3 | Sustainable value? | 5 |  |  |
| 4.1 | Easily replaceable? | 10 |  |  |
| 4.2 | Sufficient reason to exist? | 10 |  |  |
| **Total** |  | **100** |  |  |

**Reason examples**: `Privacy claims vs acoustic processing tension; S3`, `Core capability negatively reviewed; S2`

**Red flags**: When applying [trash-red-flags.md](trash-red-flags.md), if a check score is adjusted upward, note in reason: "Trigger: [pattern name]".

---

## Output Requirements

### 1. Markdown reports

Each Auditor report (whether .md or .json) **must** include the full scoring table above with all cells filled.

### 2. JSON structure

`checklist_items` must match the table. `reason` ≤ ~50 chars (or ~80 for English); use `evidence` array for details.

### 3. extract_for_report (required for 99-audit-report aggregation)

Each Auditor JSON **must** include `extract_for_report` for aggregation:

```json
{
  "extract_for_report": {
    "litmus_test_answer": "No",
    "litmus_test_reason": "One-two sentence explanation",
    "strengths_bullets": ["Strength 1; source S2", "Strength 2; S3"],
    "weaknesses_bullets": ["Weakness 1; S2", "Weakness 2"],
    "key_evidence": ["Check 1.2: evidence; S2", "Check 3.2: evidence; S2"],
    "critical_issues": []
  }
}
```

- **Tool/Toy**: `critical_issues` optional or empty
- **Trash**: `critical_issues` required; list key issues (including red-flag triggers)
- Content must be concrete and citable for 99-audit-report

### 4. Reproducibility

- Fixed row count: Tool 12+total, Toy 12+total, Trash 14+total
- Fixed columns: Check ID, Check Name, Max, Score, Brief Reason
- Any empty cell = incomplete report
- `extract_for_report` must not be omitted
