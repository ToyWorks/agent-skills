---
name: t3-hardware-scoring
description: >-
  T3 Hardware Audit System. Brand Blinding, Triple-Auditor (Tool/Toy/Trash) scoring,
  and Peer Review for objective hardware classification. Triggers: product links,
  T3 audit, hardware evaluation
dependency:
  python:
    - requests==2.32.5
    - beautifulsoup4==4.12.3
metadata:
  version: "2.0"
---

# MantaBase T3 Hardware Audit System — v2.0

## Objectives
- Crawl product information → Brand Blind → Triple-Auditor independent scoring → Peer Review → Final Judge synthesis
- Output: objective Tool / Toy / Trash classification with Eagle Eye safety veto
- Core principles: evidence-first, parallel audits, zero hallucination, transparent math

## Data Collection Strategy (Step 1-2)

### Primary: crawl_product_info.py
```bash
python3 scripts/crawl_product_info.py --url https://example.com/product --pretty
```
Uses Jina AI Reader first, then direct HTTP fallback.
Exit code 2 = content insufficient → trigger Exa fallback.

### Fallback: Exa MCP (use when crawl fails or is insufficient)
```bash
mcporter call 'exa.web_search_exa(query: "{product name} specs review", numResults: 5)'
mcporter call 'exa.company_research_exa(companyName: "{brand}", numResults: 3)'
```
Exa is the **preferred fallback** — always available, no API key required.
Collect at least **3 independent sources** before proceeding.

### Additional sources (check in order)
1. Official product page (specs, pricing, marketing claims)
2. Third-party reviews (TechAdvisor, The Verge, Tom's Guide, TrustedReviews)
3. Community discussion (Reddit, forums) for real-user pain points
4. Investigation/news coverage (privacy issues, lawsuits, controversies)

### Minimum data threshold
Proceed only when you have:
- [ ] At least one official source with **tech specs + price**
- [ ] At least one **third-party review** with hands-on findings
- [ ] Marketing claims verbatim (needed for Eagle Eye Honest check)

---

## Procedure

### Step 1: Collect Raw Data
- Run `crawl_product_info.py` on official product URL
- If exit code 2, run Exa MCP queries
- Save raw extracts to `01-level0-extracts.md` with source tags [S1], [S2], etc.

### Step 2: Organize + Brand Blind (combined step)
- Read [references/organize-guide.md](references/organize-guide.md)
- Read [references/defluff-guide.md](references/defluff-guide.md)
- Merge all sources into one structured document
- Apply Brand Blinding inline (replace brand names with [BRAND], [PRODUCT], [FEATURE])
- **Preserve ALL adjectives and marketing claims verbatim** — needed by downstream auditors
- Save to `02-brand-blinded.md`

### Step 3: Triple Auditor Scoring (independent, can be parallel)

Each Auditor sees **only the Brand-Blinded text** from Step 2.

#### 🟢 Tool Auditor
- Read [references/tool-auditor.md](references/tool-auditor.md)
- Use template: [references/tool-auditor-template.md](references/tool-auditor-template.md)
- Score 11 items (0-3 scale), max 33 points
- Extract `verbatim_evidence` BEFORE assigning score
- Output `litmus_gate: "Yes"/"No"` at top level (used by synthesize_results.py)

#### 🟡 Toy Auditor
- Read [references/toy-auditor.md](references/toy-auditor.md)
- Use template: [references/toy-auditor-template.md](references/toy-auditor-template.md)
- Score 11 items (0-3 scale), max 33 points
- Output `litmus_gate: "Yes"/"No"` at top level

#### 🔴 Trash Auditor
- Read [references/trash-auditor.md](references/trash-auditor.md)
- Read [references/trash-red-flags.md](references/trash-red-flags.md) (**required** for Eagle Eye)
- Score 14 items (0-3 scale), max 42 points
- Eagle Eye triggers **auto-set score to 3** for flagged items
- `critical_issues` list is used by synthesize_results.py for Eagle Eye Veto
- Output `litmus_gate: "Yes"/"No"` and `critical_issues: [...]` at top level

**Key principles**:
- Each auditor works from Brand-Blinded text only
- No cross-talk between auditors during scoring
- Evidence FIRST, then score — no score without a verbatim quote
- If a feature isn't in the text, it scores 0

### Step 4: Peer Review
- Read [references/peer-review-guide.md](references/peer-review-guide.md)
- Tool reviews Toy + Trash reports
- Toy reviews Tool + Trash reports
- Trash reviews Tool + Toy reports
- Focus: hallucinated quotes? missed Eagle Eye triggers? rubric misapplication?
- Each auditor updates their report with valid feedback

### Step 5: Final Judge Synthesis

Option A — Script:
```bash
python3 scripts/synthesize_results.py --input auditor_reports.json --text
```

Option B — Manual (per t3-classification.md):
1. Normalize scores: Tool=(raw/33)×100, Toy=(raw/33)×100, Trash=(raw/42)×100
2. Composite = max(NormTool, NormToy) - NormTrash
3. Check primary conditions (need 2+ of 4 conditions per category)
4. Check secondary conditions
5. Apply Eagle Eye Veto (if Trash `critical_issues` non-empty → force Trash into label)
6. Read [references/t3-classification.md](references/t3-classification.md) for full logic

### Step 6: Generate Audit Report

**Output file**: `99-audit-report.md`
**Directory**: `tmp/reports/t3-{YYYY-MM-DD}-{slug}/`

Follow YAML schema in [references/report-schema.md](references/report-schema.md).

---

## Output Format for Messaging Surfaces (WhatsApp / Telegram)

When delivering results in a chat interface, **do not paste the full file**.
Use this condensed format instead:

```
🏷️ T3 Audit — {Product Name}
Price: ${price} | Date: {YYYY-MM-DD}

📊 Scores
🟢 Tool:  {raw}/{33} → {norm}/100
🟡 Toy:   {raw}/{33} → {norm}/100
🔴 Trash: {raw}/{42} → {norm}/100
Composite: {composite:+.1f}

🏆 Classification: {final_label}
Confidence: {confidence}

{If Eagle Eye:}
🚨 Eagle Eye: {trigger name}
"{verbatim quote A}"
vs.
"{verbatim quote B}"

🟢 Tool highlights (3 bullets)
🟡 Toy highlights (3 bullets)
🔴 Trash issues (3 bullets)

💬 One-line verdict
```

Rules for messaging output:
- No markdown tables (WhatsApp doesn't render them)
- Use **bold** for emphasis, bullet lists for details
- Keep total message under 600 words
- If Eagle Eye triggered, always show the conflicting quotes

---

## Important Constraints

### 🚨 Information Isolation (critical)
- Brand-Blinded text is the ONLY input for auditors
- Auditors must never see original brand names, marketing copy, or each other's reports during scoring
- Final Judge reads only the three auditor JSON outputs, not original product text

### 📊 Objective data completeness
- Collect specs, performance, reliability, market, and cost data
- Brand Blinding must **retain** all specs and numbers
- Every score must link to extracted verbatim evidence

### Eagle Eye enforcement
- Trash Auditor MUST check every item against [references/trash-red-flags.md](references/trash-red-flags.md)
- Eagle Eye trigger → automatic score 3 → populate `critical_issues[]`
- Final Judge must respect Eagle Eye Veto regardless of composite math

### synthesize_results.py input format
The script expects a JSON file like:
```json
{
  "tool":  { "total_score": <int 0-33>, "litmus_gate": "Yes|No", ... },
  "toy":   { "total_score": <int 0-33>, "litmus_gate": "Yes|No", ... },
  "trash": { "total_score": <int 0-42>, "litmus_gate": "Yes|No",
             "critical_issues": ["<eagle eye trigger text>", ...], ... }
}
```

---

## Resource Index

### Scripts
- `scripts/crawl_product_info.py` — Multi-strategy product crawler (Jina → direct HTTP fallback)
- `scripts/synthesize_results.py` — Final Judge math (normalization + Eagle Eye + Litmus Gate)

### References
| File | Used In |
|------|---------|
| [organize-guide.md](references/organize-guide.md) | Step 2 |
| [defluff-guide.md](references/defluff-guide.md) | Step 2 |
| [tool-auditor.md](references/tool-auditor.md) | Step 3 |
| [tool-auditor-template.md](references/tool-auditor-template.md) | Step 3 |
| [toy-auditor.md](references/toy-auditor.md) | Step 3 |
| [toy-auditor-template.md](references/toy-auditor-template.md) | Step 3 |
| [trash-auditor.md](references/trash-auditor.md) | Step 3 |
| [trash-red-flags.md](references/trash-red-flags.md) | Step 3 (Eagle Eye) |
| [peer-review-guide.md](references/peer-review-guide.md) | Step 4 |
| [t3-classification.md](references/t3-classification.md) | Step 5 |
| [report-schema.md](references/report-schema.md) | Step 6 |
