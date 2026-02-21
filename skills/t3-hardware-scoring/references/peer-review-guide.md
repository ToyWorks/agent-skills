# Peer Review Guide

## Table of Contents
- [Overview](#overview)
- [Peer Review Process](#peer-review-process)
- [Review Focus Points](#review-focus-points)
- [Optimized Report Format](#optimized-report-format)
- [Review Checklist](#review-checklist)

## Overview

### Purpose
Through cross-Auditor review, identify bias, omissions, and errors in assessments to improve report consistency and accuracy.

### Core Principles
- **Objectivity**: Review based on facts and evidence; not personal
- **Constructive**: Provide specific improvement suggestions, not criticism
- **Bidirectional feedback**: Reviewer provides input; reviewee may rebut
- **Iterative improvement**: Optimize reports based on review results

### Information Isolation
- During Peer Review, Auditors may see **other Auditors' Brand-Blinded reports**
- Still may not see original product information
- Review based only on Brand-Blinded information and the other report

---

## Peer Review Process

### Round 1: Cross-Review

Each Auditor reviews the other two Auditors' reports:

**Tool Auditor reviews**:
- 🟡 Toy Auditor's report
- 🔴 Trash Auditor's report

**Toy Auditor reviews**:
- 🟢 Tool Auditor's report
- 🔴 Trash Auditor's report

**Trash Auditor reviews**:
- 🟢 Tool Auditor's report
- 🟡 Toy Auditor's report

### Round 2: Report Optimization

Each Auditor improves their own report based on review feedback:
- Assess reasonableness of review comments
- Accept reasonable suggestions and revise report
- Provide rebuttal for unreasonable comments
- Document all changes and rationale

### Round 3: Final Confirmation

Each Auditor submits optimized final report:
- Include original and revised versions
- Document all changes and rationale
- Note whether review comments were accepted

---

## Review Focus Points

### Tool Auditor Reviewing Toy Report

**Focus**:
1. **Emotional value over-assessment**
   - Does Toy misclassify practical features as emotional value?
   - Is "pleasure" confused with "efficiency"?

2. **Evidence sufficiency**
   - Is emotional value supported by concrete evidence?
   - Is user experience inferred without basis?

3. **Cross-category evidence**
   - Did Toy overlook Tool-supporting evidence?
   - Were functional strengths missed?

**Review questions**:
- [ ] Is Toy score too high?
- [ ] Is emotional value supported by evidence?
- [ ] Is there overlooked practicality evidence?

### Tool Auditor Reviewing Trash Report

**Focus**:
1. **Logic defects real or not**
   - Does Trash misclassify normal features as logic defects?
   - Is "principle violation" over-interpreted?

2. **Marketing authenticity**
   - Is factual description mislabeled as marketing?
   - Is there brand bias?

3. **Sustainability judgment**
   - Is sustainability based on actual conditions?
   - Is there actual usage evidence?

**Review questions**:
- [ ] Is Trash score reasonable?
- [ ] Are logic defects real?
- [ ] Is marketing authenticity assessment objective?

### Toy Auditor Reviewing Tool Report

**Focus**:
1. **Emotional value overlooked**
   - Does Tool ignore aesthetic design value?
   - Is user emotional need underestimated?

2. **Experience dimension missing**
   - Does it only focus on function, not experience?
   - Are emotional design elements overlooked?

3. **Cross-category evidence**
   - Did Tool overlook Toy-supporting evidence?
   - Were aesthetic or interaction strengths missed?

**Review questions**:
- [ ] Is Tool score too low?
- [ ] Is emotional value overlooked?
- [ ] Is aesthetic design underestimated?

### Toy Auditor Reviewing Trash Report

**Focus**:
1. **Design violation real or not**
   - Does Trash misclassify normal design as principle violation?
   - Is there bias against creative design?

2. **Emotional value misclassified**
   - Is emotional value mislabeled as marketing?
   - Is user emotional experience ignored?

3. **Evidence sufficiency**
   - Do Trash allegations have concrete evidence?
   - Is design issue inferred without basis?

**Review questions**:
- [ ] Is Trash score reasonable?
- [ ] Are design violations real?
- [ ] Is emotional value misclassified?

### Trash Auditor Reviewing Tool Report

**Focus**:
1. **Logic completeness**
   - Does Tool overlook potential logic issues?
   - Are there contradictions between features?

2. **Marketing language detection**
   - Does Tool misclassify marketing as feature description?
   - Is exaggeration overlooked?

3. **Sustainability analysis**
   - Does Tool underestimate long-term cost?
   - Are hidden maintenance burdens present?

**Review questions**:
- [ ] Does Tool overlook logic defects?
- [ ] Is marketing authenticity overlooked?
- [ ] Is sustainability underestimated?

### Trash Auditor Reviewing Toy Report

**Focus**:
1. **Over-emotionalization**
   - Does Toy misclassify marketing as emotional value?
   - Is there brand preference?

2. **Practicality overlooked**
   - Does Toy ignore feature practicality?
   - Are useful features misclassified as toy traits?

3. **Evidence sufficiency**
   - Is emotional value verifiable?
   - Is user emotion inferred without basis?

**Review questions**:
- [ ] Is Toy score too high?
- [ ] Is emotional value evidenced?
- [ ] Is practicality overlooked?

---

## Optimized Report Format

### Review Comment Format

```json
{
  "reviewer": "Tool Auditor",
  "target": "Toy Auditor",
  "review_date": "2024-01-01",
  "overall_assessment": {
    "rating": "Partially agree",
    "summary": "Toy score too high; emotional value lacks evidence",
    "major_concerns": [
      "Emotional value score 90 lacks concrete evidence",
      "Practical features misclassified as emotional value"
    ]
  },
  "specific_feedback": [
    {
      "dimension": "emotional_value",
      "original_score": 90,
      "suggested_score": 65,
      "reason": "Emotional value lacks specific user feedback evidence, mainly inferred",
      "evidence_requested": "Need user emotional feedback data"
    },
    {
      "dimension": "aesthetic_design",
      "original_score": 85,
      "suggested_score": 75,
      "reason": "Appearance design average, no obvious aesthetic advantage",
      "evidence": "Reference similar product comparison"
    }
  ],
  "cross_category_evidence": [
    {
      "type": "supports_tool",
      "description": "Health monitoring feature practical, should raise Tool score",
      "evidence": ["24-hour monitoring", "Medical-grade sensors"]
    }
  ]
}
```

### Optimized Report Format

```json
{
  "auditor": "Toy",
  "original_report": {...},
  "optimized_report": {
    "total_score": 65,
    "changes": [
      {
        "dimension": "emotional_value",
        "before": 90,
        "after": 65,
        "reason": "Re-evaluated emotional value based on Tool Auditor review",
        "accepted": true,
        "reviewer": "Tool Auditor"
      },
      {
        "dimension": "aesthetic_design",
        "before": 85,
        "after": 75,
        "reason": "Accepted review, lowered aesthetic design score",
        "accepted": true,
        "reviewer": "Tool Auditor"
      },
      {
        "dimension": "interactive_fun",
        "before": 80,
        "after": 80,
        "reason": "Rejected Tool Auditor's lower suggestion, kept original score",
        "accepted": false,
        "rebuttal": "Interactive fun exists; user feedback positive",
        "reviewer": "Tool Auditor"
      }
    ],
    "cross_category_evidence_updated": [
      {
        "type": "supports_tool",
        "added": true,
        "description": "Health monitoring feature practical",
        "reviewer": "Tool Auditor"
      }
    ]
  },
  "peer_review_summary": {
    "reviews_received": 2,
    "reviews_accepted": 5,
    "reviews_rejected": 1,
    "score_change": -15,
    "confidence_improved": true
  }
}
```

---

## Review Checklist

### Tool Auditor Review Checklist

#### When reviewing Toy report
- [ ] Is emotional value score reasonable?
- [ ] Is emotional value evidence-supported?
- [ ] Is practicality confused with emotional value?
- [ ] Is aesthetic design score objective?
- [ ] Is interactive fun score reasonable?
- [ ] Does social attribute have actual function?
- [ ] Is Tool evidence overlooked?

#### When reviewing Trash report
- [ ] Is Trash score reasonable?
- [ ] Are logic defects real?
- [ ] Is marketing authenticity assessment objective?
- [ ] Is sustainability judgment grounded?
- [ ] Are design violations real?
- [ ] Is there brand bias?

### Toy Auditor Review Checklist

#### When reviewing Tool report
- [ ] Is Tool score too low?
- [ ] Is emotional value overlooked?
- [ ] Is aesthetic design underestimated?
- [ ] Is experience dimension missing?
- [ ] Is Toy evidence overlooked?

#### When reviewing Trash report
- [ ] Is Trash score reasonable?
- [ ] Are design violations real?
- [ ] Is emotional value misclassified?
- [ ] Is there bias against creative design?
- [ ] Is evidence sufficient?

### Trash Auditor Review Checklist

#### When reviewing Tool report
- [ ] Does Tool overlook logic defects?
- [ ] Is marketing authenticity overlooked?
- [ ] Is sustainability underestimated?
- [ ] Are there feature contradictions?
- [ ] Is there exaggeration?

#### When reviewing Toy report
- [ ] Is Toy score too high?
- [ ] Is emotional value evidenced?
- [ ] Is marketing misclassified as emotional value?
- [ ] Is practicality overlooked?
- [ ] Is there brand preference?

---

## Peer Review Best Practices

### Reviewer
1. **Evidence-based**: All comments must have concrete evidence
2. **Objective**: Avoid subjective bias and emotional language
3. **Specific**: Provide concrete improvement suggestions, not vague criticism
4. **Constructive**: Focus on how to improve, not just on problems
5. **Respectful**: Acknowledge other Auditors' expertise

### Reviewee
1. **Open-minded**: Seriously consider all comments
2. **Rational analysis**: Objectively assess each comment's reasonableness
3. **Honest response**: Accept reasonable comments; rebut unreasonable ones
4. **Complete documentation**: Document all changes and rationale
5. **Consistency**: Keep overall logic consistent after changes

### Final Report
1. **Transparent documentation**: Fully document Peer Review process
2. **Change explanation**: Clearly explain rationale for each change
3. **Rejection rationale**: Provide rebuttal for rejected comments
4. **Impact assessment**: Assess impact of changes on final score
5. **Consistency check**: Ensure internal consistency of revised report
