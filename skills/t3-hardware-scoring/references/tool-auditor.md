# Tool Auditor Standalone Guide

## Table of Contents
- [Role Definition](#role-definition)
- [Core Questions](#core-questions)
- [Information Isolation Principles](#information-isolation-principles)
- [Scoring Logic](#scoring-logic)
- [Tony Fadell "Build" Dedicated Checklist](#tony-fadell-build-dedicated-checklist)
- [Assessment Report Format](#assessment-report-format)

## Role Definition

### 🟢 Tool Auditor
Evaluates products from a "pain point resolution" perspective, focusing on practicality, reliability, and efficiency.

### Core Values
- **Practicality**: Solve real, well-defined problems
- **Reliability**: High stability, unobtrusive design
- **Efficiency**: Become part of the user's workflow

### Scoring Direction
- **Positive scoring**: Higher scores indicate stronger Tool characteristics
- **Score range**: 0-100

## Core Questions

**Primary question**: "Does this product solve the user's real pain points? If it broke tomorrow, would the user's workflow come to a halt?"

**Litmus Test**:
- If it broke tomorrow, would the user's workflow come to a halt?
  - **Yes** → Tool
  - **No** → Not a pure Tool

**Key metrics**:
- **Dependency**: Does the user need to use it regularly?
- **Irreplaceability**: Are there alternative solutions?
- **Efficiency gain**: Does it significantly improve work or life efficiency?

## Information Isolation Principles

### 🚨 Information Isolation (Mandatory)
- **Access only**: Brand-Blinded objective product information
- **Prohibited access**: Original product information, brand names, marketing language
- **Evaluation basis**: Based solely on objective functions, technical specifications, and use cases
- **No speculation**: Must not infer product quality based on brand recognition

### Objective Data Requirements
- Evaluation must be based on complete objective data
- Reference [objective-data-standard.md](objective-data-standard.md)
- All scores must be supported by objective data

## Scoring Logic

### Score Composition
- **Checklist total**: 100 points
- **Scoring rule**: Checklist score = Tool score (0-100)
- **Meaning**: Higher scores indicate stronger Tool characteristics

### Score Ranges
- **0-30**: Does not meet Tool characteristics
- **31-60**: Partially meets Tool characteristics
- **61-80**: Meets Tool characteristics
- **81-100**: Strongly meets Tool characteristics

### Evaluation Dimensions
1. Pain Point Identification and Resolution (30 points)
2. Attention to Detail and Consistency (25 points)
3. Simplicity and Efficiency (25 points)
4. Engineering Reliability (20 points)

## Tony Fadell "Build" Dedicated Checklist

### Source
Tony Fadell, *Build: An Unorthodox Guide to Making Things Worth Making*

### Checklist

#### 1. Pain Point Identification and Resolution (30 points)

**Item 1.1: Are clear, specific pain points identified?** (0-10 points)
- 10: Clearly identified specific, verifiable pain points
- 8: Pain points identified but poorly articulated
- 5: Pain points vague or generalized
- 2: False pain points or non-real needs
- 0: No pain points identified

**Objective data requirements**:
- User pain point descriptions
- Use case analysis
- Demand validation data

**Item 1.2: Does the solution directly address the pain points?** (0-10 points)
- 10: Solution hits the core of the pain point
- 8: Solution effectively alleviates pain points
- 5: Solution partially addresses pain points
- 2: Low correlation between solution and pain points
- 0: Solution unrelated to pain points

**Objective data requirements**:
- Correspondence between features and pain points
- Effectiveness validation data
- User feedback statistics

**Item 1.3: Is it better than existing solutions?** (0-10 points)
- 10: Significantly superior to all existing solutions
- 8: Superior to most existing solutions
- 5: Comparable to existing solutions
- 2: Inferior to existing solutions
- 0: No improvement value

**Objective data requirements**:
- Competitor comparison analysis
- Efficiency improvement data
- User satisfaction comparison

#### 2. Attention to Detail and Consistency (25 points)

**Item 2.1: Is every interaction meticulously designed?** (0-10 points)
- 10: All interaction details are finely crafted
- 8: Most interaction details are well designed
- 5: Interaction details are average
- 2: Obvious design oversights exist
- 0: Rough interaction design

**Objective data requirements**:
- Interaction flow analysis
- User experience test data
- Design consistency check results

**Item 2.2: Is there consistent design language?** (0-10 points)
- 10: Perfect consistency across all touchpoints
- 8: Basically consistent
- 5: Partially inconsistent
- 2: Frequently inconsistent
- 0: Completely inconsistent

**Objective data requirements**:
- Design specification check
- Multi-touchpoint experience analysis

**Item 2.3: Is unnecessary complexity hidden?** (0-5 points)
- 5: Complex technology completely transparent to users
- 3: Most complexity hidden
- 1: Complexity partially visible
- 0: Complexity directly exposed to users

**Objective data requirements**:
- Technical architecture analysis
- User interface design evaluation

#### 3. Simplicity and Efficiency (25 points)

**Item 3.1: Does it follow the "less is more" principle?** (0-10 points)
- 10: Extremely simple, no redundancy
- 8: Simple and efficient, minimal redundancy
- 5: Some redundancy
- 2: Considerable redundancy
- 0: Complex and bloated

**Objective data requirements**:
- Feature redundancy analysis
- Interface element check

**Item 3.2: Are operations efficient?** (0-10 points)
- 10: Extremely fast operations, zero learning cost
- 8: Fast operations, low learning cost
- 5: Average operations, moderate learning cost
- 2: Slow operations, high learning cost
- 0: Cumbersome operations, extremely high learning cost

**Objective data requirements**:
- Task completion time data
- Operation step count statistics
- Learning curve analysis

**Item 3.3: Is the design unobtrusive?** (0-5 points)
- 5: Perfectly integrated into workflow, nearly imperceptible
- 3: Basically unobtrusive
- 1: Occasionally draws attention
- 0: Frequently interrupts users

**Objective data requirements**:
- Usage frequency statistics
- Disruption level assessment
- User feedback data

#### 4. Engineering Reliability (20 points)

**Item 4.1: Is operation stable and reliable?** (0-10 points)
- 10: Extremely stable, failure rate <1%
- 8: Stable and reliable, failure rate 1-5%
- 5: Basically stable, failure rate 5-10%
- 2: Average stability, failure rate 10-20%
- 0: Unstable, failure rate >20%

**Objective data requirements**:
- Quality assurance data
- User feedback statistics
- Third-party test data

**Item 4.2: Is quality control emphasized?** (0-10 points)
- 10: Strict quality control system
- 8: Quality control in place
- 5: Average quality control
- 2: Weak quality control
- 0: No quality control

**Objective data requirements**:
- Quality assurance process
- Test coverage data

## Assessment Report Format

### 🚨 Strict Output Template (Mandatory)

**Must** read [auditor-templates.md](auditor-templates.md) and output according to the **Tool Auditor scoring table template**.

**Mandatory requirements**:
- Output **complete filled scoring table** with columns: Item ID | Item Name | Max Score | Score | Brief Reason (≤50 characters)
- All 11 items (1.1–4.2) and total row must not be omitted
- `reason` field must not exceed ~50 characters; use `evidence` for detailed citations

Table first, then JSON output; both must be consistent.

### Tool Auditor report must include

```json
{
  "auditor": "Tool",
  "auditor_type": "Tool Auditor",
  "timestamp": "2024-01-01T00:00:00Z",

  "information_source": "Brand-Blinded product information (original brand information isolated)",
  "information_isolation_confirmed": true,
  "scoring_basis": "Tony Fadell Build checklist",
  "checklist_compliance_confirmed": true,

  "total_score": 82,
  "checklist_score": 82,

  "checklist_items": {
    "1. Pain Point Identification and Resolution": {
      "total": 28,
      "items": {
        "1.1": {
          "score": 9,
          "max_score": 10,
          "reason": "Clearly identified health monitoring pain points, well targeted",
          "evidence": [
            "Supports 24-hour health monitoring",
            "High data accuracy",
            "User pain point: Unable to continuously understand health status"
          ]
        },
        "1.2": {
          "score": 9,
          "max_score": 10,
          "reason": "Solution directly addresses pain points with significant effect",
          "evidence": [
            "Heart rate monitoring 99% accuracy",
            "Blood oxygen monitoring error <2%",
            "Complete sleep analysis"
          ]
        },
        "1.3": {
          "score": 10,
          "max_score": 10,
          "reason": "Significantly superior to traditional monitoring methods",
          "evidence": [
            "80% cost reduction vs. hospital testing",
            "Data continuity better than periodic checkups",
            "60% user satisfaction improvement"
          ]
        }
      }
    },
    "2. Attention to Detail and Consistency": {
      "total": 20,
      "items": {
        "2.1": {"score": 8, "max_score": 10, "reason": "...", "evidence": [...]},
        "2.2": {"score": 7, "max_score": 10, "reason": "...", "evidence": [...]},
        "2.3": {"score": 5, "max_score": 5, "reason": "...", "evidence": [...]}
      }
    },
    "3. Simplicity and Efficiency": {
      "total": 20,
      "items": {
        "3.1": {"score": 8, "max_score": 10, "reason": "...", "evidence": [...]},
        "3.2": {"score": 7, "max_score": 10, "reason": "...", "evidence": [...]},
        "3.3": {"score": 5, "max_score": 5, "reason": "...", "evidence": [...]}
      }
    },
    "4. Engineering Reliability": {
      "total": 14,
      "items": {
        "4.1": {"score": 7, "max_score": 10, "reason": "...", "evidence": [...]},
        "4.2": {"score": 7, "max_score": 10, "reason": "...", "evidence": [...]}
      }
    }
  },

  "objective_data_summary": {
    "technical_specs": {...},
    "market_data": {...},
    "reliability_data": {...}
  },

  "strengths": [
    "Complete health monitoring features",
    "Accurate data",
    "Long battery life"
  ],

  "weaknesses": [
    "Frequent charging required",
    "Requires phone pairing"
  ],

  "cross_category_evidence": {
    "supports_toy": [
      "Fashionable appearance",
      "Customizable watch faces"
    ],
    "supports_trash": []
  },

  "litmus_test_result": {
    "test": "If it broke tomorrow, would the user's workflow come to a halt?",
    "answer": "Yes",
    "reason": "Users are accustomed to checking health data daily; device failure would affect health management workflow",
    "confidence": "High"
  },

  "extract_for_report": {
    "litmus_test_answer": "Yes",
    "litmus_test_reason": "Users are accustomed to checking health data daily; device failure would affect health management workflow",
    "strengths_bullets": ["Complete health monitoring features; S2", "Accurate data; S2"],
    "weaknesses_bullets": ["Frequent charging required; S2", "Requires phone pairing; S2"],
    "key_evidence": ["Item 1.2: Heart rate monitoring 99% accuracy; S2", "Item 4.1: Failure rate <1%; S2"]
  }
}
```

### Report Requirements

1. **extract_for_report**: Must be included for 99-audit-report aggregation (see [auditor-templates.md](auditor-templates.md))
2. **Information source declaration**: Must declare use of Brand-Blinded information only
3. **Scoring basis declaration**: Must declare use of Tony Fadell *Build* checklist
4. **Objective data support**: Every score must be supported by objective data
5. **Cross-category evidence**: Must list evidence supporting other categories
6. **Litmus Test result**: Must include Litmus Test result

## Workflow

### 1. Receive Task
- Receive Brand-Blinded product information
- Confirm information isolation status
- Verify objective data completeness

### 2. Execute Checklist Scoring
- Read Tony Fadell *Build* checklist
- Evaluate each item one by one
- Score based on objective data
- Record scoring rationale and evidence

### 3. Generate Report
- Summarize scoring results
- Calculate total score
- List strengths and weaknesses
- Identify cross-category evidence
- Execute Litmus Test

### 4. Output Report
- Generate complete Tool Auditor report
- Ensure correct report format
- Verify objective data citations

## Notes

1. **Strict information isolation**: Use Brand-Blinded information only
2. **Based on objective data**: All scores must be supported by objective data
3. **Avoid subjective judgment**: Follow checklist, avoid subjective assumptions
4. **Honest documentation**: Record truthfully even when evidence supports other categories
5. **Maintain independence**: Do not communicate with or reference other Auditors
