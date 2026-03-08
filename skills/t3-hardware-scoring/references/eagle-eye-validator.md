# Eagle Eye Validator — AI-Driven QA (v2.1)

## Purpose
A single-pass AI QA subagent that replaces the 3-way Peer Review.
It validates the highest-risk items: Eagle Eye triggers, score=3 evidence, and **Architectural Plausibility** of on-device claims.

This is an **AI reasoning task**, not a deterministic script — the validator must apply engineering judgment, especially for Architectural Implausibility assessments.

## When to Run
Run the validator if ANY of the following is true:
- Trash report `critical_issues` is non-empty
- Any auditor has any item scored **3**
- Composite score is in Gray Zone (-10 to +10)

Otherwise: skip and proceed to synthesis.

## Inputs
The main agent passes **file paths** (not inline content) to the validator subagent:
- `02-brand-blinded.md` — original product text
- `03-tool-auditor.json` (only if contains score=3 items)
- `03-toy-auditor.json` (only if contains score=3 items)
- `03-trash-auditor.json` (always, since it contains critical_issues)

## Output
Print JSON to stdout (main agent writes file):

```json
{
  "validator": "Eagle Eye Validator v2.1",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "items_checked": 4,
  "adjustments": [
    {
      "auditor": "Trash",
      "item_id": "1.5",
      "before": 3,
      "after": 3,
      "action": "upheld",
      "reason": "Privacy Tension confirmed. Architectural Implausibility strengthens: on-device claim not credible for form factor."
    },
    {
      "auditor": "Trash",
      "item_id": "3.2",
      "before": 3,
      "after": 2,
      "action": "downgraded",
      "reason": "Price is high but independent review confirms core feature works. Downgrade to 2."
    }
  ],
  "architectural_plausibility": {
    "assessed": true,
    "claim_verbatim": "<exact on-device/local processing claim from text>",
    "form_factor": "<device form factor>",
    "ai_workload": "<description of AI tasks claimed>",
    "verdict": "implausible | plausible | insufficient_data",
    "reasoning": "<engineering assessment — see framework below>",
    "affects_items": ["1.5"]
  },
  "critical_issues_final": [
    "Triggered: <Pattern Name>. <evidence summary>",
    "..."
  ],
  "score_changes": {
    "trash_before": 0,
    "trash_after": 0,
    "net_change": 0
  }
}
```

## Checks (executed in order)

### A) Eagle Eye Trigger Validity
For each entry in `trash.critical_issues`:
1. Extract the required verbatim quotes from `02-brand-blinded.md`
2. Verify the trigger condition is met **without inference** (except Architectural Implausibility)
3. If a trigger is **not supported** by text: downgrade score from 3 → 1 or 2

**Rule:** Missing data ≠ contradiction. Do not uphold Eagle Eye without explicit textual evidence.

### B) Architectural Plausibility Assessment (NEW in v2.1)
**Trigger:** Product claims "on-device" / "local" / "fully private" AI processing.

The validator must assess whether the claimed AI workload is technically feasible within the product's form factor. This is the one check where **engineering reasoning** is expected.

**Assessment framework:**

| Factor | Question | Red Flag |
|--------|----------|----------|
| **Compute** | What AI tasks are claimed? (ASR, NLP, LLM, emotion classification, multimodal fusion) | LLM inference or complex multimodal fusion in a device with no disclosed chipset |
| **Power** | What form factor? (pendant, ring, watch, glasses) | Battery-constrained form + continuous AI = implausible without cloud offload |
| **Architecture** | Is a specific edge AI chip, model size, or framework disclosed? | "Proprietary AI" with no architecture detail |
| **Precedent** | Do comparable products exist that achieve this locally? | No known precedent for the claimed capability in similar form factor |

**Verdict options:**
- `"plausible"` — engineering is credible (e.g., known edge chip + lightweight model)
- `"implausible"` — workload exceeds form factor constraints → strengthens Privacy Tension / Honest violation
- `"insufficient_data"` — can't assess (no AI detail disclosed) → flag but don't override score

**If verdict is "implausible":**
- Uphold or upgrade item 1.5 (Honest) to score 3
- Add "Architectural Implausibility" to reason
- Add to `critical_issues_final`

### C) Score=3 Evidence Check
For any item scored 3 (any auditor):
- Confirm `verbatim_evidence` includes at least 1 quote supporting the 3-level rubric
- If not: downgrade to 2 or 1

### D) Missed Trigger Spot-check
Quick scan for the 6 canonical Eagle Eye triggers:
- Privacy Tension
- Inconsistent Claims
- Broken "Never" Promise
- Price vs. Doubt
- App Redundancy
- Architectural Implausibility (v2.1)

Only flag if **clear textual evidence** exists for a trigger that was missed.

## Token Guardrails
- Do NOT re-score every item — only inspect flagged ones
- Extract at most 2 quotes per trigger
- Total output should be ≤ 800 tokens
- Subagent timeout: 120s
