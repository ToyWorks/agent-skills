# T3 Classification and Final Judge Guide

## Table of Contents
- [T3 Classification Definition](#t3-classification-definition)
- [Litmus Test](#litmus-test)
- [Final Judge Role](#final-judge-role)
- [Classification Decision Logic](#classification-decision-logic)
- [Composite Score Calculation](#composite-score-calculation)
- [Classification Decision Flow](#classification-decision-flow)

## T3 Classification Definition

### Tool
**Core characteristic**: Solves real, well-defined problems

**Key metrics**:
- **Practicality**: Solves real pain points
- **Reliability**: High stability, unobtrusive
- **Efficiency**: Becomes part of user workflow
- **Dependency**: User needs to use regularly

**Examples**:
- 🟢 Premium tools: Apple AirPods, Dyson vacuum
- 🟡 With Toy attributes: Premium coffee maker (functional + beautiful)

### Toy
**Core characteristic**: Brings sensory pleasure, surprise, and emotional satisfaction

**Key metrics**:
- **Fun**: Direct emotional satisfaction
- **Surprise**: Exceeds expectations with positive experiences
- **Emotional connection**: Establishes emotional bonds and memories
- **Explorability**: Provides space for exploration and discovery

**Examples**:
- 🟡 With Tool attributes: Game console (entertainment + functionality)
- 🔴 Approaching Trash: Viral products with no practical value

### Trash
**Core characteristic**: Violates design principles, lacks clear value, creates problems rather than solving them

**Key metrics**:
- **Design violation**: Violates fundamental design principles
- **Problem creation**: Creates new problems
- **Value deficit**: Lacks clear value proposition
- **Replaceability**: Easily replaceable or obsolete

**Examples**:
- 🔴 Pure Trash: Knockoff products, pseudo-innovation
- 🟡 Approaching Trash: Over-marketed mediocre products

### Mixed Classifications

Real-world products often have multiple classification characteristics:

**Tool + Toy** (most common)
- Examples: Apple AirPods, premium coffee maker, smartwatch
- Characteristics: Both practical and beautiful; solves problems and brings pleasure

**Toy + Trash**
- Examples: Viral small appliances (attractive but no practical value)
- Characteristics: Appealing appearance but lacks actual functionality

**Tool + Trash**
- Examples: Essential but poorly designed products
- Characteristics: Functionally necessary but poor user experience

## Litmus Test

### Tool Litmus Test
**Question**: "If it broke tomorrow, would the user's workflow come to a halt?"
- **Yes** → Tool
- **No** → Not a pure Tool

### Toy Litmus Test
**Question**: "Would users display it prominently to 'show off' or collect it?"
- **Yes** → Toy
- **No** → Not a pure Toy

### Trash Litmus Test
**Question**: "If this product disappeared tomorrow, would the world become better or worse?"
- **Better** → Trash
- **Worse** → Not Trash
- **No impact** → Possibly Trash (no raison d'être)

## Final Judge Role

### Core Responsibilities
The Final Judge (final arbiter) makes the final classification decision based on three independent Auditor reports.

### Working Principles
1. **Objective and fair**: Based on objective data and facts; avoid subjective bias
2. **Information isolation**: Does not access original brand information; uses Brand-Blinded information only
3. **Comprehensive weighing**: Consider scores and evidence from all three Auditors
4. **Transparent decisions**: Classification decisions must have clear rationale and basis

### Input
- Tool Auditor report (total score 0-100)
- Toy Auditor report (total score 0-100)
- Trash Auditor report (total score 0-100, inverted scoring)

### Output
- Final classification result
- Classification rationale
- Primary classification
- Secondary classification (if any)
- Composite score

## Classification Decision Logic

### Step 1: Calculate Composite Score

```python
def calculate_composite_score(tool_score, toy_score, trash_score):
    """
    Calculate composite score

    Args:
        tool_score: Tool Auditor score (0-100, positive)
        toy_score: Toy Auditor score (0-100, positive)
        trash_score: Trash Auditor score (0-100, positive)

    Returns:
        composite_score: Composite score (-100 to 100)
    """
    # Composite = max(Tool, Toy) - Trash
    # Product led by Tool or Toy, take dominant advantage minus Trash negative score
    composite = max(tool_score, toy_score) - trash_score
    return composite
```

**Score interpretation**:
- **Composite > 30**: Strong Tool/Toy bias
- **Composite 0-30**: Tool/Toy bias
- **Composite -30 to 0**: Trash bias
- **Composite < -30**: Strong Trash bias

### Step 2: Determine Primary Classification

#### Determine if Tool is primary
**Conditions** (satisfy 2+):
- Tool score ≥ 70
- Tool score > Toy score + 15
- Tool score > Trash score + 15
- Litmus Test result is "Yes"

#### Determine if Toy is primary
**Conditions** (satisfy 2+):
- Toy score ≥ 70
- Toy score > Tool score + 15
- Toy score > Trash score + 15
- Litmus Test result is "Yes"

#### Determine if Trash is primary
**Conditions** (satisfy 2+):
- Trash score ≥ 70 (positive scoring; higher = more Trash)
- Trash score > Tool score + 15
- Trash score > Toy score + 15
- Litmus Test result is "Better"

### Step 3: Determine Secondary Classification

**When Tool is primary, secondary classification**:
- Toy score ≥ 60 and Toy score > Trash score + 15 → Secondary: Toy
- Trash score ≥ 60 and Trash score > Toy score + 15 → Secondary: Trash

**When Toy is primary, secondary classification**:
- Tool score ≥ 60 and Tool score > Trash score + 15 → Secondary: Tool
- Trash score ≥ 60 and Trash score > Toy score + 15 → Secondary: Trash

**When Trash is primary, secondary classification**:
- Tool score ≥ 50 → Secondary: Tool
- Toy score ≥ 50 → Secondary: Toy
- Both Tool and Toy ≥ 50 → Secondary: Tool + Toy

### Step 4: Special Case Handling

**No clear primary**:
- All three scores close (difference <15) → Mixed classification
- Composite between -15 and 15 → Mixed classification

**Contradictory scores**:
- High Tool score but Trash Litmus Test "Better" → Deep review
- High Toy score but low Trash score → Deep review
- Need to re-examine objective data

## Composite Score Calculation

### Score Weights
- **Tool Auditor**: 1.0 (positive)
- **Toy Auditor**: 1.0 (positive)
- **Trash Auditor**: -1.0 (negative)

### Formula
```
Composite Score = max(Tool Score, Toy Score) - Trash Score
```

### Score Range
- **Minimum**: -100 (max(Tool,Toy)=0, Trash=100)
- **Maximum**: 100 (max(Tool,Toy)=100, Trash=0)
- **Midpoint**: 0 (max(Tool,Toy)=Trash, e.g., all three = 50)

### Score Interpretation

| Composite Score Range | Classification Bias | Description |
|-----------------------|---------------------|-------------|
| 70-100 | Strong Tool/Toy | Clear Tool or Toy characteristics |
| 40-69 | Clear Tool/Toy | Obvious Tool/Toy characteristics |
| 15-39 | Tool/Toy bias | Tool/Toy characteristics dominant |
| -14 to 14 | Mixed | Balanced characteristics, no clear bias |
| -39 to -15 | Trash bias | Trash characteristics dominant |
| -69 to -40 | Clear Trash | Obvious Trash characteristics |
| -100 to -70 | Strong Trash | Clear Trash characteristics |

## Classification Decision Flow

### Complete Flow Diagram

```
┌─────────────────────────────────────┐
│ 1. Receive three Auditor reports    │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ 2. Calculate composite score        │
│    Composite = max(Tool, Toy) - Trash│
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ 3. Determine primary classification │
│    - Check conditions for each type   │
│    - Determine 1 primary             │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ 4. Determine secondary (if any)      │
│    - Check other category scores     │
│    - Check secondary conditions      │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ 5. Generate final classification     │
│    - Record rationale               │
│    - Generate classification report  │
└─────────────────────────────────────┘
```

### Decision Template

```json
{
  "final_judge": {
    "timestamp": "2024-01-01T00:00:00Z",
    "auditor_reports": {
      "tool": {
        "total_score": 82,
        "litmus_test": {"answer": "Yes", "confidence": "High"}
      },
      "toy": {
        "total_score": 75,
        "litmus_test": {"answer": "Yes", "confidence": "Medium"}
      },
      "trash": {
        "total_score": 25,
        "litmus_test": {"answer": "No impact", "confidence": "Medium"}
      }
    },
    "composite_score": 44.0,
    "classification": {
      "primary": "Tool",
      "secondary": ["Toy"],
      "final_label": "Tool + Toy"
    },
    "decision_reasoning": {
      "primary_reason": "Tool score highest (82), significantly above Trash (57-point gap), clearly meets Tool characteristics",
      "secondary_reason": "Toy score relatively high (75), second only to Tool, product has Toy attributes",
      "composite_interpretation": "Composite 44, Tool/Toy bias",
      "litmus_test_consistency": "Both Tool and Toy Litmus Test results 'Yes', consistent with classification"
    },
    "confidence": "High",
    "information_source": "Brand-Blinded product information (three independent Auditor reports)"
  }
}
```

## Classification Report Format

### Required Information

1. **Basic information**
   - Timestamp
   - Product identifier (Brand-Blinded)
   - Information source declaration

2. **Auditor report summary**
   - Three Auditors' total scores
   - Three Litmus Test results

3. **Composite score**
   - Composite score calculation result
   - Score interpretation

4. **Classification decision**
   - Primary classification
   - Secondary classification (if any)
   - Final classification label

5. **Decision rationale**
   - Primary classification rationale
   - Secondary classification rationale (if any)
   - Composite score interpretation
   - Litmus Test consistency analysis

6. **Confidence**
   - Decision confidence (High/Medium/Low)
   - Uncertain factors (if any)

## Notes

1. **Information isolation**: Final Judge may only access Brand-Blinded information
2. **Objective data**: Classification decisions must be based on objective data
3. **Transparent decisions**: Classification rationale must be clear and explicit
4. **Handle contradictions**: When encountering contradictory scores, conduct deep review
5. **Complete documentation**: All decision process must be fully recorded
