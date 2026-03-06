# Toy Auditor Score Table Template

## Scoring Table (Mandatory — fill all rows)

| Item ID | Item Name | Max Score | Score | Brief Reason (≤50 chars) |
|---------|-----------|-----------|-------|--------------------------|
| 1.1 | Appearance Attractive | 3 | _ | |
| 1.2 | Materials & Craftsmanship | 3 | _ | |
| 1.3 | Interaction Feedback | 3 | _ | |
| 2.1 | Exceeds Expectations | 3 | _ | |
| 2.2 | Encourages Exploration | 3 | _ | |
| 2.3 | Easter Eggs / Hidden Details | 3 | _ | |
| 3.1 | Evokes Positive Emotions | 3 | _ | |
| 3.2 | Emotional Bond | 3 | _ | |
| 3.3 | Personalization Space | 3 | _ | |
| 4.1 | Feature Depth (Mastery) | 3 | _ | |
| 4.2 | Encourages Experimentation | 3 | _ | |
| **TOTAL** | | **33** | **_** | |

## Scoring Scale Reminder

| Score | Meaning | Requirement |
|-------|---------|-------------|
| 0 | None | No mention of this feature/metric in data |
| 1 | Claimed | Feature present but lacks design detail or user data |
| 2 | Specified | Specific CMF / documented Easter egg / specific hardware |
| 3 | Validated | Validated by user feedback, metrics, or community data |

## JSON Output Template

```json
{
  "auditor": "Toy",
  "auditor_type": "Toy Auditor",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "information_source": "Brand-Blinded product information (original brand information isolated)",
  "information_isolation_confirmed": true,
  "scoring_basis": "Don Norman Design Psychology checklist (0-3 Deterministic Scale)",
  "checklist_compliance_confirmed": true,
  "checklist_items": {
    "1. Sensory Pleasure": {
      "total": 0,
      "items": {
        "1.1": { "verbatim_evidence": ["<exact quote>"], "score": 0, "max_score": 3, "reason": "<≤50 chars>" },
        "1.2": { "verbatim_evidence": ["<exact quote>"], "score": 0, "max_score": 3, "reason": "<≤50 chars>" },
        "1.3": { "verbatim_evidence": ["<exact quote>"], "score": 0, "max_score": 3, "reason": "<≤50 chars>" }
      }
    },
    "2. Surprise and Discovery": {
      "total": 0,
      "items": {
        "2.1": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" },
        "2.2": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" },
        "2.3": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" }
      }
    },
    "3. Emotional Connection": {
      "total": 0,
      "items": {
        "3.1": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" },
        "3.2": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" },
        "3.3": { "verbatim_evidence": [], "score": 0, "max_score": 3, "reason": "" }
      }
    },
    "4. Explorability": {
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
    "supports_tool": [],
    "supports_trash": []
  },
  "litmus_gate": "No",
  "litmus_test_result": {
    "test": "Does the data explicitly mention features designed for aesthetic display, deep personalization, or non-functional sensory delight?",
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

1. `verbatim_evidence` MUST be extracted from Brand-Blinded text **before** assigning a score
2. If no exact quote → score must be 0 (or 1 for vague mentions)
3. `reason` field ≤ 50 characters
4. `litmus_gate` top-level field: `"Yes"` or `"No"` — used by `synthesize_results.py`
5. `total_score` = sum of all 11 item scores
