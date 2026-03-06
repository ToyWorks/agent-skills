# Tool Auditor Score Table Template

## Scoring Table (Mandatory — fill all rows)

| Item ID | Item Name | Max Score | Score | Brief Reason (≤50 chars) |
|---------|-----------|-----------|-------|--------------------------|
| 1.1 | Pain Point Identification | 3 | _ | |
| 1.2 | Solution Addresses Pain | 3 | _ | |
| 1.3 | Efficiency / Workflow Gain | 3 | _ | |
| 2.1 | Friction Reduction | 3 | _ | |
| 2.2 | Design Consistency | 3 | _ | |
| 2.3 | Complexity Hidden | 3 | _ | |
| 3.1 | Less is More | 3 | _ | |
| 3.2 | Learning Curve | 3 | _ | |
| 3.3 | Unobtrusive Design | 3 | _ | |
| 4.1 | Operational Stability | 3 | _ | |
| 4.2 | Quality Control | 3 | _ | |
| **TOTAL** | | **33** | **_** | |

## Scoring Scale Reminder

| Score | Meaning | Requirement |
|-------|---------|-------------|
| 0 | None | No mention of this feature/metric in data |
| 1 | Claimed | Feature present but no numerical/specific validation |
| 2 | Quantified | Feature + specific supporting data (specs, times, %s) |
| 3 | Validated | Quantified + compared to baseline OR external validation |

## JSON Output Template

```json
{
  "auditor": "Tool",
  "auditor_type": "Tool Auditor",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "information_source": "Brand-Blinded product information (original brand information isolated)",
  "information_isolation_confirmed": true,
  "scoring_basis": "Tony Fadell Build checklist (0-3 Deterministic Scale)",
  "checklist_compliance_confirmed": true,
  "checklist_items": {
    "1. Pain Point Identification and Resolution": {
      "total": 0,
      "items": {
        "1.1": { "verbatim_evidence": ["<exact quote>"], "score": 0, "max_score": 3, "reason": "<≤50 chars>" },
        "1.2": { "verbatim_evidence": ["<exact quote>"], "score": 0, "max_score": 3, "reason": "<≤50 chars>" },
        "1.3": { "verbatim_evidence": ["<exact quote>"], "score": 0, "max_score": 3, "reason": "<≤50 chars>" }
      }
    },
    "2. Attention to Detail and Consistency": {
      "total": 0,
      "items": {
        "2.1": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" },
        "2.2": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" },
        "2.3": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" }
      }
    },
    "3. Simplicity and Efficiency": {
      "total": 0,
      "items": {
        "3.1": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" },
        "3.2": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" },
        "3.3": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" }
      }
    },
    "4. Engineering Reliability": {
      "total": 0,
      "items": {
        "4.1": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" },
        "4.2": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" }
      }
    }
  },
  "strengths": [],
  "weaknesses": [],
  "cross_category_evidence": {
    "supports_toy": [],
    "supports_trash": []
  },
  "litmus_gate": "No",
  "litmus_test_result": {
    "test": "Does the data explicitly mention a measurable decrease in task completion time or direct workflow replacement?",
    "answer": "No",
    "reason": "",
    "confidence": "Low"
  },
  "extract_for_report": {
    "litmus_test_answer": "No",
    "litmus_test_reason": "",
    "strengths_bullets": [],
    "weaknesses_bullets": [],
    "key_evidence": []
  },
  "total_score": 0,
  "max_possible_score": 33
}
```

## Filling Rules

1. `verbatim_evidence` MUST be extracted from the Brand-Blinded text **before** assigning a score
2. If no exact quote exists → score must be 0 (or 1 if the feature is vaguely mentioned)
3. `reason` field ≤ 50 characters
4. `litmus_gate` top-level field: `"Yes"` or `"No"` — used by `synthesize_results.py`
5. `total_score` = sum of all 11 item scores
