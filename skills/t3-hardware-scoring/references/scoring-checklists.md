# Scoring Checklists Index

## Overview

This file consolidates the checklist index for all Auditors in the T3 hardware scoring system. Each Auditor has a dedicated full guide document.

## Checklist Index

### Tool Auditor Checklist
- **File path**: [tool-auditor.md](tool-auditor.md)
- **Checklist name**: Tony Fadell *Build* Dedicated Checklist
- **Scoring logic**: Positive scoring (0-100)
- **Evaluation dimensions**:
  1. Pain Point Identification and Resolution (30 points)
  2. Attention to Detail and Consistency (25 points)
  3. Simplicity and Efficiency (25 points)
  4. Engineering Reliability (20 points)
- **Litmus Test**: If it broke tomorrow, would the user's workflow come to a halt?

### Toy Auditor Checklist
- **File path**: [toy-auditor.md](toy-auditor.md)
- **Checklist name**: Don Norman Design Psychology Dedicated Checklist
- **Scoring logic**: Positive scoring (0-100)
- **Evaluation dimensions**:
  1. Sensory Pleasure (30 points)
  2. Surprise and Discovery (25 points)
  3. Emotional Connection (25 points)
  4. Explorability (20 points)
- **Litmus Test**: Would users display it prominently to "show off" or collect it?

### Trash Auditor Checklist
- **File path**: [trash-auditor.md](trash-auditor.md)
- **Checklist name**: Dieter Rams Ten Principles Violation Checklist
- **Scoring logic**: Positive scoring (0-100; higher = stronger Trash characteristics)
- **Evaluation dimensions**:
  1. Principle Violation (30 points)
  2. Problem Creation (25 points)
  3. Value Deficit (25 points)
  4. Replaceability (20 points)
- **Litmus Test**: If this product disappeared tomorrow, would the world become better or worse?

## Checklist Usage Flow

### 1. Information Preparation
- Prepare Brand-Blinded product information
- Ensure objective data is complete
- Reference [objective-data-standard.md](objective-data-standard.md)

### 2. Select Auditor
- Choose Auditor per assessment goal
- Tool Auditor: Assess Tool characteristics
- Toy Auditor: Assess Toy characteristics
- Trash Auditor: Assess Trash characteristics

### 3. Read Checklist
- Open corresponding Auditor guide
- Read full checklist
- Understand scoring logic and standards

### 4. Execute Assessment
- Evaluate each item
- Score based on objective data
- Record rationale and evidence

### 5. Generate Report
- Summarize results
- Produce standard-format report
- Run Litmus Test

## Strict Output Template

**Mandatory** [auditor-templates.md](auditor-templates.md): Every Auditor must output **complete filled scoring table** (columns: Item ID | Item Name | Max Score | Score | Brief Reason ≤50 characters). Row count is fixed; do not omit. Ensure reproducible results.

## Report Format Requirements

All Auditor reports must follow unified JSON format and **output table first, then JSON**, including:
- Basic info (timestamp, Auditor type)
- Information source declaration (Brand-Blinded info)
- Scoring basis declaration (checklist name)
- Total and sub-scores
- Item-level scores
- Objective data summary
- Strengths and weaknesses
- Cross-category evidence
- Litmus Test result

## T3 Classification Guide

- **File path**: [t3-classification.md](t3-classification.md)
- **Content**: T3 classification definitions, Litmus Test, Final Judge guide, classification logic
- **Use**: Final Judge synthesizes three Auditor reports to make final classification decision

## Related References

- [objective-data-standard.md](objective-data-standard.md): Objective data standard
- [t3-taxonomy.md](t3-taxonomy.md): T3 classification details (historical reference)
- [peer-review-guide.md](peer-review-guide.md): Peer Review process guide

## Notes

1. **Independent assessment**: Each Auditor works independently; does not reference other Auditors' reports
2. **Information isolation**: Use Brand-Blinded information only; do not access original brand information
3. **Objective data**: All scores must be based on objective data; avoid subjective judgment
4. **Complete documentation**: Document rationale and evidence in detail
5. **Honest assessment**: Record truthfully even when evidence supports other categories

## Quick Reference

### Scoring Logic Comparison

| Auditor | Scoring Logic | Score Range | Score Meaning |
|---------|---------------|-------------|---------------|
| Tool Auditor | Positive | 0-100 | Higher = stronger Tool characteristics |
| Toy Auditor | Positive | 0-100 | Higher = stronger Toy characteristics |
| Trash Auditor | Positive | 0-100 | Higher = stronger Trash characteristics |

### Litmus Test Comparison

| Auditor | Litmus Test Question | Yes → | No → |
|---------|---------------------|-------|------|
| Tool Auditor | Would workflow halt if it broke tomorrow? | Tool | Not pure Tool |
| Toy Auditor | Would users display it prominently or collect it? | Toy | Not pure Toy |
| Trash Auditor | Would the world be better if it disappeared tomorrow? | Trash | Not Trash |

### Composite Score Calculation

```
Composite Score = max(Tool Score, Toy Score) - Trash Score
```

- All Auditors: positive scoring
- Tool and Toy: Higher = stronger Tool/Toy characteristics
- Trash: Higher = stronger Trash characteristics
- Composite range: -100 to 100
  - Positive: Tool/Toy bias
  - Negative: Trash bias
  - Near 0: Mixed classification
