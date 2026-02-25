# Peer Review Guide

## Overview

### Purpose

Through cross-Auditor review, identify hallucinated quotes, ignored data, and misapplied 0-3 scoring rules to ensure total deterministic accuracy before the Final Judge makes a ruling.

### Core Principles

* **Evidence-Centric**: Arguments must revolve around the presence or absence of explicit quotes in the Brand-Blinded text.
* **Fact-Checking**: Verify that the `verbatim_evidence` actually supports the assigned 0-3 score.
* **Trigger Auditing**: Ensure Eagle Eye triggers were not missed (or falsely applied).
* **Iterative improvement**: Optimize reports based on review results.

### Information Isolation

* During Peer Review, Auditors may see **other Auditors' Brand-Blinded reports** (including their extracted quotes and scores).
* Review is based *only* on the Brand-Blinded information and the strict 0-3 rubric rules.

---

## Peer Review Process

### Round 1: Cross-Review (Fact-Checking)

Each Auditor reviews the other two Auditors' reports:

**🟢 Tool Auditor reviews**:

* 🟡 Toy Auditor's report
* 🔴 Trash Auditor's report

**🟡 Toy Auditor reviews**:

* 🟢 Tool Auditor's report
* 🔴 Trash Auditor's report

**🔴 Trash Auditor reviews**:

* 🟢 Tool Auditor's report
* 🟡 Toy Auditor's report

### Round 2: Report Optimization (Rebuttal & Revision)

Each Auditor improves their own report based on review feedback:

* Assess if the reviewer correctly identified a missing quote or rubric misapplication.
* Accept reasonable suggestions, adjust the 0-3 score, and update the `verbatim_evidence`.
* Provide rebuttal if the reviewer's suggestion violates the strict isolation or extraction rules.
* Document all changes.

### Round 3: Final Submission

Each Auditor submits an optimized final report to the Final Judge.

---

## Review Focus Points

### 🟢 Tool Auditor Reviewing 🟡 Toy Report

**Focus**:

1. **Quote Hallucination**: Did Toy extract a quote that doesn't exist to justify a Score of 3 for Emotional Connection?
2. **Rubric Misapplication**: Did Toy give a Score of 3 for Item 1.1 (Appearance) based on a vague claim ("looks nice") instead of required quantified data (e.g., "92% satisfaction")?
3. **Cross-category evidence**: Did Toy overlook a quote detailing a workflow efficiency improvement that should be in `cross_category_evidence`?

### 🟢 Tool Auditor Reviewing 🔴 Trash Report

**Focus**:

1. **False Eagle Eye Triggers**: Did Trash apply a "Core Flaw" veto (Score 3) based on a minor bug rather than explicit failure of the primary feature?
2. **Contextual Misinterpretation**: Did Trash score a 3 for "Unnecessary Complexity" on a feature that a specific quote proves actually saves time?
3. **Missing Baseline**: Did Trash give a 3 for "Low ROI" without a quote explicitly comparing it to a cheaper alternative?

### 🟡 Toy Auditor Reviewing 🟢 Tool Report

**Focus**:

1. **Ignored CMF Data**: Did Tool ignore explicit quotes about premium materials (Aluminum, custom haptics) that should be noted in `cross_category_evidence`?
2. **Efficiency vs. Delight**: Did Tool misclassify a purely aesthetic UI animation as a "workflow efficiency" feature?
3. **Over-scoring Reliability**: Did Tool give a 3 for Reliability (Item 4.1) based purely on a marketing claim without extracting quantified uptime/failure rate data?

### 🟡 Toy Auditor Reviewing 🔴 Trash Report

**Focus**:

1. **Aesthetic Penalization**: Did Trash give a Score 3 for "Uselessness" (Item 1.2) simply because a feature is designed for non-functional sensory delight (Easter eggs)?
2. **Missed Customization**: Did Trash flag the product as having "No Value" while ignoring explicit quotes about deep personalization or modding communities?
3. **Eagle Eye Accuracy**: Verify that any "Privacy Tension" triggers extracted actual conflicting quotes.

### 🔴 Trash Auditor Reviewing 🟢 Tool Report

**Focus**:

1. **Missed Eagle Eye Triggers**: Did Tool give a 3 for "Solves Pain Points" while completely ignoring a quote stating the device hallucinates 60% of the time?
2. **Marketing Blindness**: Did Tool accept a "zero learning curve" claim (Score 2 or 3) despite text evidence showing a massive onboarding manual is required?
3. **Subscription Traps**: Did Tool praise long-term efficiency while missing a quote about a mandatory subscription that bricks the device?

### 🔴 Trash Auditor Reviewing 🟡 Toy Report

**Focus**:

1. **Ignored Friction**: Did Toy praise the "fun" of an interaction while ignoring a quote stating the interaction takes 5 times longer than a traditional button?
2. **False Praise**: Did Toy give a 3 for "Honesty" when there is an explicit contradiction in the text regarding data collection?
3. **E-waste Verification**: Did Toy overlook that the "fun" device has a sealed battery that dies in 6 months?

---

## Optimized Report Format

### Review Comment Format (Strict JSON)

```json
{
  "reviewer": "Trash Auditor",
  "target": "Tool Auditor",
  "review_date": "2024-01-01",
  "overall_assessment": {
    "rating": "Major Corrections Needed",
    "summary": "Tool Auditor missed a critical Eagle Eye trigger regarding feature reliability."
  },
  "specific_feedback": [
    {
      "item_id": "1.2",
      "dimension": "Solves Pain Points",
      "original_score": 3,
      "suggested_score": 0,
      "reason": "You scored a 3, but missed the quote: 'Users report the OCR fails 40% of the time.' This contradicts your extracted evidence.",
      "evidence_requested": "Must incorporate the 40% failure rate quote and adjust score."
    },
    {
      "item_id": "4.1",
      "dimension": "Engineering Reliability",
      "original_score": 2,
      "suggested_score": 1,
      "reason": "The quote extracted ('Built to last') is a marketing claim, not quantified data. Rubric requires a Score of 1.",
      "evidence_requested": "Downgrade to 1 unless specific IP-rating or failure rate data can be extracted."
    }
  ],
  "cross_category_evidence": [
    {
      "type": "supports_trash",
      "description": "Device requires continuous cloud sync despite local-processing claims.",
      "evidence": ["Quote: 'Uploads telemetry data every 5 minutes'"]
    }
  ]
}

```

### Optimized Report Format (Post-Review Update)

```json
{
  "auditor": "Tool",
  "original_report_total": 26,
  "optimized_report": {
    "total_score": 22,
    "max_possible_score": 33,
    "changes": [
      {
        "item_id": "1.2",
        "before_score": 3,
        "after_score": 1,
        "reason": "Accepted Trash Auditor review. The extracted quote was incomplete and ignored the 40% failure rate limitation.",
        "accepted": true,
        "reviewer": "Trash Auditor"
      },
      {
        "item_id": "4.1",
        "before_score": 2,
        "after_score": 2,
        "reason": "Rejected Trash Auditor review. A secondary quote was found confirming 'IP68 water resistance', justifying the Score of 2.",
        "accepted": false,
        "rebuttal": "Quote found: 'Certified IP68 rating'.",
        "reviewer": "Trash Auditor"
      }
    ]
  },
  "peer_review_summary": {
    "reviews_received": 2,
    "changes_accepted": 1,
    "changes_rejected": 1,
    "net_score_change": -4,
    "eagle_eye_flags_added": 0
  }
}

```

---

## Review Checklist

### 🟢 Tool Auditor Review Checklist

* [ ] Did Toy/Trash extract an exact quote for every score > 1?
* [ ] Did Toy misclassify a workflow efficiency as a "fun" feature?
* [ ] Did Trash apply a veto based on subjective feelings rather than explicit text?
* [ ] Are there workflow metrics (time saved, accuracy) ignored by the other auditors?

### 🟡 Toy Auditor Review Checklist

* [ ] Did Tool/Trash hallucinate a quote?
* [ ] Did Tool ignore CMF (Color, Material, Finish) data?
* [ ] Did Trash penalize an explicitly declared "Easter Egg" as a useless distraction?
* [ ] Did the other auditors miss quotes proving deep user emotional attachment?

### 🔴 Trash Auditor Review Checklist

* [ ] Did Tool/Toy give a Score of 3 to an item that actually triggers an Eagle Eye Veto (e.g., Privacy Tension, Core Flaw)?
* [ ] Did Tool accept a marketing claim as a "Quantified" (Score 2) or "Validated" (Score 3) fact?
* [ ] Did Toy ignore quotes regarding severe battery drain, high pricing, or subscription lock-ins?
* [ ] Are any extracted quotes taken out of context to sound positive when the surrounding text is negative?