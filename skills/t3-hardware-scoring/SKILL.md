---
name: t3-hardware-scoring
description: >-
  MantaBase T3 Hardware Audit System. Objectively classifies hardware products via
  Brand Blinding, Triple-Auditor (Tool/Toy/Trash) specialized scoring, and Peer
  Review based on design theory. Triggers: product links, T3 audit, Tool/Toy/Trash
  classification, hardware evaluation, VC investment advice
compatibility: Network access (for product page crawling)
metadata:
  version: "1.0"
---

# MantaBase T3 Hardware Audit System

## Objectives
- This Skill: Automatically crawls product information from hardware product links, applies Brand Blinding for debranding, has three independent Auditors score using authoritative reference checklists, performs Peer Review for mutual critique, and produces objective Tool/Toy/Trash classification
- Capabilities: Web scraping, Brand Blinding filtering, Triple-Auditor specialized scoring, Peer Review, Final Judge synthesis
- Triggers: User provides hardware product links requesting T3 audit or classification
- Core principles: Transparency first, objective evaluation, parallel audits, expert review, continuous improvement

## Prerequisites
- No extra setup; the system handles web content extraction

## Procedure

### Standard Flow

#### 1. Get User Input
- Ask user for hardware product links (e-commerce, official sites, review sites, etc.)
- Optional: Ask about specific dimensions or audit focus

#### 2. Get Product Information (Pipeline Tools)

Identify site type (Shopify / Kickstarter) and crawl product pages for consistent data input.

- Use `crawlProductInfo` to collect source URLs and raw extracts.
- Write outputs to `01-level0-source-urls.md` and `02-level0-extracts.md`.
- Then run organize phase before defluffing:
  - Read [references/organize-guide.md](references/organize-guide.md)
  - Merge multi-page extracts into a single chain-of-evidence markdown
  - Preserve source tags so downstream auditors can cite exact evidence

#### 3. Brand Blinding (Agent)
- Read [references/defluff-guide.md](references/defluff-guide.md) for Brand Blinding rules
- Agent performs debranding:
  - Remove brand names and trademark references
  - Remove marketing language and hype
  - Identify and remove emotional adjectives
  - Keep functional and objective information
  - Preserve factual accuracy
- Output: Brand-Blinded objective product info

#### 4. Triple Auditor Specialized Scoring (Agent, Parallel)
- Each Auditor evaluates **independently and in parallel**
- Each Auditor reads only their own guide, not others’ guides or reports

**🟢 Tool Auditor**
- Read [references/tool-auditor.md](references/tool-auditor.md)
- Focus: Pain-point solving, practicality, reliability
- Reference: Tony Fadell "Build" checklist
- Dimensions:
  - Pain point identification (30 pts)
  - Attention to detail and consistency (25 pts)
  - Simplicity and efficiency (25 pts)
  - Engineering reliability (20 pts)
- Output: Scoring report (100 pts total) with item scores, reasons, evidence
- Litmus Test: If it broke tomorrow, would the user’s workflow stall?

**🟡 Toy Auditor**
- Read [references/toy-auditor.md](references/toy-auditor.md)
- Focus: Emotional value, enjoyment, aesthetic design
- Reference: Don Norman "The Design of Everyday Things" checklist
- Dimensions:
  - Sensory pleasure (30 pts)
  - Surprise and discovery (25 pts)
  - Emotional connection (25 pts)
  - Explorability (20 pts)
- Output: Scoring report (100 pts total) with item scores, reasons, evidence
- Litmus Test: Would the user put it on display or keep it as a collectible?

**🔴 Trash Auditor**
- Read [references/trash-auditor.md](references/trash-auditor.md)
- **Required** [references/trash-red-flags.md](references/trash-red-flags.md) high-sensitivity triggers
- Focus: Logical flaws, marketing deception, design violations
- Reference: Dieter Rams Ten Principles violation checklist
- Dimensions:
  - Principle violations (30 pts)
  - Problem creation (25 pts)
  - Value deficit (25 pts)
  - Replaceability (20 pts)
- Output: Scoring report (0–100 pts, higher = more Trash) with item scores, reasons, evidence
- Litmus Test: If this product disappeared tomorrow, would the world be better or worse?

**Key Principles**:
- **Information isolation**: Auditors only see Brand-Blinded info; never raw product info
- **Checklist-based**: Must use the reference checklists
- **Evidence-driven**: Every score backed by evidence
- **Independent**: Three Auditors evaluate in parallel, no cross-talk
- **Objective**: Report findings, not defend a category
- **Honest**: Record evidence even when it supports another category

#### 5. Peer Review (Agent, Parallel)
- Read [references/peer-review-guide.md](references/peer-review-guide.md)
- Each Auditor reviews the other two reports:

**Cross-review**:
- Tool reviews: Toy + Trash
- Toy reviews: Tool + Trash
- Trash reviews: Tool + Toy

**Review focus**:
- Are scores reasonable?
- Is evidence sufficient?
- Any cross-category evidence missed?
- Bias or omissions?

**Output**:
- Review comments (with suggestions and reasons)
- Score adjustment suggestions
- Cross-category evidence

#### 6. Auditor Report Optimization (Agent)
- Each Auditor refines their report using review feedback:
  - Assess validity of feedback
  - Accept valid suggestions and update report
  - For invalid suggestions, give rebuttal
  - Log all changes and reasons

**Output**:
- Original report
- Optimized report
- Change log (accepted/rejected comments and reasons)

#### 7. Final Judge Synthesis (Agent)
- Read [references/t3-classification.md](references/t3-classification.md)
- Read all three optimized Auditor reports
- Synthesize conclusions and evidence
- Apply T3 rules:
  - Composite = max(Tool, Toy) - Trash
  - Determine primary category (≥2 conditions met)
  - Determine secondary category (if any)
  - Apply Litmus Test consistency check
- Output: Final classification, confidence, reasoning, improvement suggestions

#### 8. Generate Audit Report

**Output file**: Always `99-audit-report.md`. Directory: `tmp/reports/t3-{YYYY-MM-DD}-{case-id}/`.

**Report structure** (see [references/report-schema.md](references/report-schema.md)):
1. **YAML metadata** (wrapped in `---`): For leaderboard parsing: `case_id`, `source_url`, `scores`, `chart_data`, `litmus_tests`, `classification`, etc.
2. **Text analysis**: Aggregated from Auditors’ `extract_for_report`: Product Overview, Tool Highlights, Toy Highlights, Trash Highlights, Final Judge Reasoning, Improvement Suggestions

**Must include**:
- Basic product info (raw vs Brand-Blinded)
- Triple Auditor score tables (format required by each auditor guide)
- Peer Review summary
- Final Judge result

### Optional Branches

- **Insufficient product info**: Ask user for more description or references
- **Near boundary scores**: Analyze dominant factors, explain classification
- **Auditor disagreement**: Final Judge explains trade-off logic
- **Controversy**: Offer multi-perspective analysis with evidence for each category

## Resource Index

- **Pipeline tools**:
  - `crawlProductInfo` + `identifySiteType` — Crawl source pages and produce raw extracts
  - `organizeExtracts` — Build organized chain-of-evidence markdown for downstream phases

- **References**:
  - [references/organize-guide.md](references/organize-guide.md) — Organizing phase rules and output structure
  - [references/report-schema.md](references/report-schema.md) — Step 8, required; YAML schema
  - [references/tool-auditor.md](references/tool-auditor.md) — Tool Auditor scoring
  - [references/toy-auditor.md](references/toy-auditor.md) — Toy Auditor scoring
  - [references/trash-auditor.md](references/trash-auditor.md) — Trash Auditor scoring
  - [references/trash-red-flags.md](references/trash-red-flags.md) — Trash high-sensitivity triggers
  - [references/t3-classification.md](references/t3-classification.md) — Final Judge classification
  - [references/defluff-guide.md](references/defluff-guide.md) — Brand Blinding
  - [references/peer-review-guide.md](references/peer-review-guide.md) — Peer Review

## Important Notes

- **🚨 Information isolation (critical)**:
  - Auditors may only access Brand-Blinded info
  - Never raw product info, brand names, or marketing copy
  - Auditor tasks must state they evaluate based solely on Brand-Blinded info
  - Audit report must include "information source" field

- **📊 Objective data completeness**:
  - Collect complete objective data (specs, performance, reliability, market, sustainability, cost)
  - Brand Blinding must **retain** all objective data
  - Scores must be backed by verifiable objective data
  - Report must include objective data summary and completeness score

- **Brand Blinding**:
  - Must precede Auditor evaluation
  - Remove brand and marketing; keep objective data

- **Checklist-based scoring**: Use reference checklists; each score must link to checklist items and evidence

- **Triple Auditor independence**: Evaluate in parallel, no information sharing

- **Peer Review objectivity**: Evidence-based; specific suggestions; open to feedback

- **Transparency**: Process, reasoning, and evidence clearly documented

- **Agent-led**: Brand Blinding, scoring, Peer Review, Final Judge run by agent; scripts only for crawl and formatting

## Examples

### Example 1: Full T3 Audit
- **Flow**: Full Brand Blinding + scoring + Peer Review + Final Judge
- **Execution**: Agent crawls → Brand Blinding → parallel Auditors → Peer Review → optimization → Final Judge → report
- **Output**: Full audit report with all sections

### Example 2: Quick T3 Classification
- **Flow**: Simplified; focus on Brand Blinding and core scoring
- **Focus**: Core value proposition, Litmus Tests, key checklist items

### Example 3: Competitor Audit
- **Flow**: Batch crawl + parallel Auditors + Peer Review + comparison
- **Output**: Comparison table + per-product reports

## Audit Flow Diagram

```
User input URL
    ↓
Crawl product info (raw)
    ↓
Brand Blinding (Agent debrands)
    ├─ Raw info 🔒 (sealed)
    └─ Brand-Blinded info ✅ (only input for Auditors)
    ↓
┌─────────────────────────────────────────┐
│ Triple Auditor Scoring (Agent, parallel)│
│ 🔒 Isolation: Each Auditor only sees    │
│    Brand-Blinded info                   │
├───────────────┬─────────────┬────────────┤
│ 🟢 Tool       │ 🟡 Toy      │ 🔴 Trash   │
└───────┬───────┴─────┬───────┴──────┬────┘
        └─────────────┼──────────────┘
                      ↓
         Peer Review
                      ↓
         Auditor Optimization
                      ↓
         Final Judge
                      ↓
         99-audit-report.md
```

## 🔒 Information Isolation

1. **Raw (Level 0)**: Brand names, marketing, emotional language — sealed, only Brand Blinding and Final Judge (for comparison)
2. **Brand-Blinded (Level 1)**: Functional and objective data — accessible to Auditors and Final Judge

Agent checklist when acting as Auditor:
- [ ] Explicitly state use of Brand-Blinded info only
- [ ] Base scores on reference checklists
- [ ] No brand names referenced
- [ ] No marketing language referenced
- [ ] Report includes "Information source: Brand-Blinded product info"
- [ ] Report includes "Scoring basis: [checklist name]"
