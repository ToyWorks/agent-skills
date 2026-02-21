# Trash Auditor High-Sensitivity Trigger List (Eagle Eye)

## Purpose

Beyond the standard Dieter Rams checklist, identify **high Trash risk** product patterns and evidence to avoid overly lenient scoring. When the following trigger conditions are satisfied, the Trash Auditor should **proactively adjust scores upward** and strengthen evidence citations.

---

## I. Honesty Principle Reinforcement (1.5 Honest)

### Trigger Conditions

| Trigger Pattern | Evidence Type | Suggested Score Adjustment |
|-----------------|--------------|----------------------------|
| **Privacy claim vs. implementation tension** | Marketing claims "local/no-cloud/doesn't store" + product requires continuous collection of sensitive signals (acoustic, biometric) | +1~2 |
| **Inconsistent claims** | Conflicting statements from different sources (product page vs. privacy policy, FAQ) on the same fact | +1~2 |
| **"Never/Not ever" type promise** | Claims "never listen/store/share" etc., but technical implementation requires collecting or transmitting that type of data | +1~2 |

### Scoring Anchors

- **No trigger**: Score within original 0–5 range
- **Satisfies 1 item**: Honesty item recommendation ≥ 3 points
- **Satisfies 2+ items**: Honesty item recommendation ≥ 4 points
- **If obvious contradiction exists with no reasonable explanation**: Honesty item may receive full 5 points

### Objective Data Requirements

- Cite specific source ID and original text/summary
- Annotate conflicting statements from both sides
- Do not speculate on undisclosed facts; judge only based on disclosed information

---

## II. Usefulness Principle Reinforcement (1.2 Useful)

### Trigger Conditions

| Trigger Pattern | Evidence Type | Suggested Score Adjustment |
|-----------------|--------------|----------------------------|
| **Core capability negatively reviewed by users** | User reviews explicitly question product's claimed core functionality (accuracy, reliability, effectiveness) | +1~2 |
| **Claimed vs. unverified** | Product claims capability (e.g., emotion recognition, AI insight) but has no third-party/independent verification or accuracy data | +1 |
| **False pain point/false need** | "Pain point" addressed lacks verifiable demand evidence, or can be replaced by low-cost means | +1~2 |
| **Health/psychological claims without medical backing** | Claims health/emotion/psychological-related capability but explicitly disclaims non-medical device, and has no clinical or academic verification | +1 |

### Scoring Anchors

- **No trigger**: Score within original 0–5 range
- **Core capability negatively reviewed**: Usefulness recommendation ≥ 3 points
- **Core capability negatively reviewed + unverified**: Usefulness recommendation ≥ 4 points
- **Multiple triggers stacked**: Consider 5 points (complete violation of useful principle)

### Objective Data Requirements

- Cite specific user feedback original text or summary
- Annotate gap between "claimed capability" and "verification status"
- Distinguish "no data" from "negative data"—the latter carries higher weight

---

## III. Value Deficit Reinforcement (3.2 Cost-effectiveness, 3.3 Sustainable Value)

### Trigger Conditions

| Trigger Pattern | Evidence Type | Suggested Score Adjustment |
|-----------------|--------------|----------------------------|
| **High price + core capability in doubt** | Price ≥ $200 and core functionality questioned by users or lacks verification | 3.2 +1~2 |
| **Promise vs. delivery gap** | Clear marketing promise, but user feedback "didn't meet promise", "overhyped" | 3.2 +1~2 |
| **Reliance on unverified algorithm** | Long-term value depends on algorithm/AI effectiveness, but no accuracy, retention, or effectiveness data | 3.3 +1~2 |

### Scoring Anchors

- **High price + core capability in doubt**: 3.2 recommendation ≥ 6 points (low cost-effectiveness)
- **Promise vs. delivery gap**: 3.2 recommendation ≥ 7 points
- **Reliance on unverified algorithm + no long-term data**: 3.3 recommendation ≥ 4 points

---

## IV. Problem Creation Reinforcement (2.1 Creating New Problems)

### Trigger Conditions

| Trigger Pattern | Evidence Type | Suggested Score Adjustment |
|-----------------|--------------|----------------------------|
| **Expectation vs. reality gap** | User disappointment, trust damage due to product not meeting expectations | +1~2 |
| **Privacy/security potential risk** | Product continuously collects sensitive data (audio, biometric), but implementation is opaque or claims conflict | +1~2 |
| **Increased maintenance burden** | Requires charging, pairing, firmware updates, multi-device sync, and troubleshooting documentation exists | +1 |

### Scoring Anchors

- **Expectation gap + involves core value**: 2.1 recommendation ≥ 6 points
- **Privacy/security risk + claim conflict**: 2.1 recommendation ≥ 7 points

---

## V. Replaceability Reinforcement (4.1, 4.2)

### Trigger Conditions

| Trigger Pattern | Evidence Type | Suggested Score Adjustment |
|-----------------|--------------|----------------------------|
| **No unique verification** | Claims unique capability but no third-party accuracy, certification, or comparison data | +1~2 |
| **Low-cost alternatives exist** | Journal app, meditation app, existing wearables, etc. can partly achieve same purpose | +1 |
| **Reason to exist depends on unverified assumption** | "If algorithm works then valuable"—but effectiveness unverified | +1~2 |

### Scoring Anchors

- **No unique verification + alternatives exist**: 4.1, 4.2 each recommendation ≥ 6 points
- **Reason to exist entirely depends on unverified assumption**: 4.2 recommendation ≥ 7 points

---

## VI. Execution Flow

### Insert Point in Trash Auditor Workflow

1. **First pass**: Complete routine scoring per Dieter Rams checklist
2. **Second pass**: Check against this Eagle Eye trigger list item by item
3. **Score adjustment**: For satisfied items, adjust scores upward within reasonable range and add evidence
4. **Documentation**: Note in `reason` "Triggered [specific trigger pattern], score adjusted upward"

### Reflection in Report

- In `checklist_items` `reason` field, cite trigger pattern (e.g., "Triggered: Core capability negatively reviewed by users")
- List satisfied high-sensitivity triggers in `critical_issues`
- Remain objective: Based only on objective facts in Brand-Blinded information; do not guess undisclosed content

---

## VII. Counterexamples: Avoid Over-Adjustment

The following situations **should not** trigger score adjustment based on speculation alone:

- When no user feedback exists, do not heavily penalize usefulness solely for "no verification" (may moderately +1, avoid excessive)
- When no claim conflict evidence exists, do not trigger full Honesty score for assumptions like "possible cloud processing"
- When product has clear advantages (e.g., hardware specs, after-sales), must record in `strengths` and `cross_category_evidence` honestly

**Principle**: Eagle Eye = more sensitive to **existing evidence**, not over-inferring from **missing evidence**.
