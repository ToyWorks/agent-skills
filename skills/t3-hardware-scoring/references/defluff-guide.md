# Brand Blinding Guide

## Contents
- [Purpose](#purpose)
- [Principles](#principles)
- [Filtering Rules](#filtering-rules)
- [Process](#process)
- [Examples](#examples)
- [Common Pitfalls](#common-pitfalls)

## Purpose

### Why Brand Blinding?

Brand influence can bias hardware product evaluation:
- **Brand halo**: Famous brands tend to be overrated
- **Marketing noise**: Hype and emotional language skew analysis
- **Social bias**: Popular products get over-praised

### Goals

- **Objectivity**: Remove subjective brand-related influence
- **Consistency**: Same evaluation standards for all products
- **Fairness**: No bias from brand recognition
- **First principles**: Focus on product function and logic

## Principles

### 1. Preserve Facts
- Keep all technical specs and parameters
- Keep true functional descriptions
- Keep real usage scenarios

### 2. Remove Subjectivity
- Remove brand names and trademark references
- Remove marketing language and hype
- Remove emotional adjectives and opinions

### 3. Neutral Wording
- Rephrase subjective claims as neutral facts
- Rephrase brand-related content as generic descriptions
- Preserve accuracy and completeness

## Filtering Rules

### Rule 1: Remove Brand Names

**Remove**:
- Brand names (e.g. Apple, Dyson, Tesla)
- Product line names (e.g. iPhone, AirPods)
- Trademark references (e.g. AirTag, Kindle)

**Replace with**: Generic category (e.g. "smartwatch", "wireless earbuds", "tracker")
- If brand defines the category, use a generic description

**Example**:
```
Raw: Apple Watch Series 9
Brand-Blinded: Smartwatch (9th generation)
```

### Rule 2: Remove Marketing Language

**Remove marketing terms**:
- Hype: "revolutionary", "groundbreaking", "ultimate", "best-in-class"
- Vague promises: "game-changing", "life-changing", "unprecedented"
- Slogans: "Designed by Apple in California"

**Action**:
- Delete marketing terms
- Keep factual functional descriptions
- If info is missing, state "specific info not provided"

**Example**:
```
Raw: revolutionary new sensor technology
Brand-Blinded: new sensor technology
```

### Rule 3: Remove Emotional Descriptions

**Remove emotional terms**:
- Positive: "amazing", "stunning", "beautiful", "elegant"
- Negative: "terrible", "awful", "poor"
- Subjective: "premium quality", "high-end", "luxury"

**Action**:
- Remove emotional adjectives
- Keep verifiable attributes
- Replace "premium" with concrete materials/specs

**Example**:
```
Raw: premium aluminum alloy body
Brand-Blinded: aluminum alloy body
```

### Rule 4: Preserve Functional Information (Required)

**🔴 Important**: All objective data must be fully preserved; do not remove or alter.

**Must keep** (details in [objective-data-standard.md](objective-data-standard.md)):

- Technical specs: processor, storage, memory, screen, battery, connectivity, sensors, IP rating, weight, dimensions
- Performance: response time, power, thermal, noise
- Reliability: failure rate, warranty, return rate
- Market: launch date, sales, ratings, review count
- Sustainability: materials, recyclability, energy rating, repairability
- Cost: list price, discounts, maintenance, accessories, subscription

### Rule 5: Third-Party Claims

**Remove**:
- Brand-linked claims: "best in class", "industry leader"
- Unverified praise: "highly rated", "critically acclaimed"

**Action**:
- Remove unverified claims
- Keep verifiable third-party certifications (with source)
- Keep specific test data when cited

## Process

1. **Identify brand info**: Brand names, trademarks, marketing language, emotional language
2. **Classify**: Brand / Marketing / Emotional / Functional
3. **Apply**: Remove or replace per rules; preserve functional data
4. **Validate**: Check completeness, no brand residue, accuracy

## Examples

### Smartwatch

**Raw**:
```
Apple Watch Series 9 features Apple's revolutionary S9 chip,
delivering stunning performance with the most advanced display
ever. The beautiful aluminum case is crafted with premium materials,
offering up to 18 hours of battery life. Rated 4.8 stars by users.
```

**Brand-Blinded**:
```
Smartwatch (9th gen) with S9 chip; high-performance display.
Aluminum body; battery life up to 18 hours. User rating: 4.8/5.
```

### Wireless Headphones

**Raw**:
```
Dyson Zone is the groundbreaking noise-canceling headphones with
purifying visor, featuring amazing electrostatic technology. The
elegant design provides ultimate comfort for all-day wear.
```

**Brand-Blinded**:
```
Noise-canceling headphones with purifying visor; electrostatic technology.
Designed for comfortable all-day wear.
```

## Common Pitfalls

1. **Over-deletion**: Losing functional information
2. **Lost context**: Removing marketing leaves gaps — extract and rephrase facts
3. **Brand residue**: Brand names or references remain — verify all mentions
4. **Broken flow**: Text becomes disjointed — use neutral wording for coherence

## Brand Blinding Checklist

- [ ] All brand names removed or replaced
- [ ] All marketing language removed
- [ ] All emotional adjectives removed
- [ ] All technical specs preserved
- [ ] All functional descriptions preserved
- [ ] Narrative is coherent
- [ ] No brand residue
