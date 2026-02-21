# Objective Data Standard

## Table of Contents
- [Overview](#overview)
- [Objective Data Categories](#objective-data-categories)
- [Data Format Specification](#data-format-specification)
- [Data Source Requirements](#data-source-requirements)
- [Validation Standards](#validation-standards)

## Overview

### Purpose
Ensure all data used in the T3 audit system is objective, verifiable, and complete; avoid subjective assumptions and marketing language interference.

### Core Principles
- **Objectivity**: Data must be facts, not opinions or speculation
- **Verifiability**: Data must be verifiable by third parties
- **Completeness**: Collect as much objective data as possible
- **Consistency**: Data format and sources must be consistent

### Information Isolation
- Objective data **must be retained** during Brand Blinding
- Distinguish "objective data" from "marketing language"
- Objective data is critical evidence for scoring

---

## Objective Data Categories

### 1. Technical Specs

#### 1.1 Processor
- **Required**: Model, core count, base frequency
- **Format**: `{"processor": "Apple M2", "cores": 8, "base_frequency": "3.5 GHz"}`
- **Source**: Official spec sheet, third-party reviews

#### 1.2 Storage
- **Required**: Capacity, storage type
- **Format**: `{"storage": "256GB", "storage_type": "SSD"}`
- **Source**: Official spec sheet

#### 1.3 Memory
- **Required**: Capacity, memory type
- **Format**: `{"ram": "8GB", "ram_type": "LPDDR5"}`
- **Source**: Official spec sheet

#### 1.4 Display
- **Required**: Size, resolution
- **Optional**: Refresh rate, brightness, panel type
- **Format**: `{"screen": {"size": "6.1 inch", "resolution": "2532x1170", "refresh_rate": "60 Hz"}}`
- **Source**: Official spec sheet

#### 1.5 Battery
- **Required**: Capacity, claimed battery life
- **Optional**: Charging power, charging interface
- **Format**: `{"battery_capacity": "3279 mAh", "battery_life_claimed": "17 hours", "charging_power": "20W", "charging_port": "USB-C"}`
- **Source**: Official spec sheet, third-party tests

#### 1.6 Connectivity
- **Required**: WiFi version, Bluetooth version
- **Optional**: NFC, cellular
- **Format**: `{"wifi_version": "Wi-Fi 6", "bluetooth_version": "Bluetooth 5.3", "nfc": true}`
- **Source**: Official spec sheet

#### 1.7 Sensors
- **Required**: Complete sensor list
- **Format**: `{"sensors": ["accelerometer", "gyroscope", "heart rate", "blood oxygen"]}`
- **Source**: Official spec sheet

#### 1.8 Protection Rating
- **Required**: IP rating (if applicable)
- **Format**: `{"ip_rating": "IP68"}`
- **Source**: Official spec sheet

#### 1.9 Physical Specs
- **Required**: Weight, dimensions
- **Format**: `{"weight": "170g", "dimensions": "146.7x71.5x7.65mm"}`
- **Source**: Official spec sheet

### 2. Performance Data

#### 2.1 Runtime Performance
- **Required**: Response time, processing capability
- **Format**: `{"response_time": "< 100ms", "processing_capability": "High"}`
- **Source**: Third-party reviews (e.g., AnTuTu, Geekbench)

#### 2.2 Power Consumption
- **Optional**: Standby power, active power
- **Format**: `{"standby_power": "0.1W", "active_power": "5W"}`
- **Source**: Third-party tests

#### 2.3 Thermal
- **Optional**: Max temperature, temperature distribution
- **Format**: `{"max_temperature": "45°C", "thermal_distribution": "uniform"}`
- **Source**: Third-party reviews

#### 2.4 Noise Level
- **Optional**: Operating noise
- **Format**: `{"noise_level": "< 30 dB"}`
- **Source**: Third-party tests

### 3. Reliability Data

#### 3.1 Failure Rate
- **Optional**: MTBF (Mean Time Between Failures)
- **Format**: `{"mtbf": "50,000 hours"}`
- **Source**: Official warranty data, third-party statistics

#### 3.2 Warranty
- **Required**: Warranty duration
- **Format**: `{"warranty_years": 2, "warranty_months": 24}`
- **Source**: Official warranty policy

#### 3.3 Return Rate
- **Optional**: Return rate data
- **Format**: `{"return_rate": "2%"}`
- **Source**: Third-party statistics, user reports

#### 3.4 User Complaint Rate
- **Optional**: Complaint rate data
- **Format**: `{"complaint_rate": "5%"}`
- **Source**: Consumer reports, user review analysis

### 4. Market Data

#### 4.1 Launch Date
- **Required**: Launch year/date
- **Format**: `{"release_date": "2023-09", "release_year": 2023}`
- **Source**: Official release information

#### 4.2 Sales Data
- **Optional**: Sales volume, market share
- **Format**: `{"sales_volume": "10M units", "market_share": "15%"}`
- **Source**: Market research reports

#### 4.3 User Reviews
- **Required**: Review count, average rating
- **Format**: `{"review_count": 50000, "average_rating": 4.5, "rating_scale": 5}`
- **Source**: E-commerce platforms, third-party review sites

#### 4.4 Third-Party Ratings
- **Optional**: Professional review site ratings
- **Format**: `{"professional_ratings": {"site1": 8.5, "site2": 9.0}}`
- **Source**: Professional review sites

### 5. Sustainability Data

#### 5.1 Material Composition
- **Required**: Primary materials list
- **Format**: `{"materials": ["aluminum", "glass", "recyclable_plastic"]}`
- **Source**: Official material documentation

#### 5.2 Recyclability
- **Optional**: Recyclable proportion
- **Format**: `{"recyclable_percentage": "85%"}`
- **Source**: Official environmental documentation

#### 5.3 Energy Rating
- **Optional**: Energy rating, carbon footprint
- **Format**: `{"energy_rating": "A+", "carbon_footprint": "50kg CO2"}`
- **Source**: Official environmental data, third-party certification

#### 5.4 Repairability
- **Required**: Repairable/disassemblable
- **Format**: `{"repairable": true, "replaceable_battery": true, "repairability_score": 8}`
- **Source**: Official documentation, iFixit score

### 6. Cost Data

#### 6.1 Purchase Cost
- **Required**: List price, discounted price
- **Format**: `{"list_price": "$999", "discounted_price": "$899"}`
- **Source**: Official pricing, e-commerce platforms

#### 6.2 Maintenance Cost
- **Optional**: Annual maintenance cost
- **Format**: `{"annual_maintenance_cost": "$50"}`
- **Source**: Official documentation

#### 6.3 Accessory Cost
- **Optional**: Common accessory prices
- **Format**: `{"accessory_costs": {"charger": "$29", "case": "$49"}}`
- **Source**: Official accessory pricing

#### 6.4 Subscription Cost
- **Optional**: Monthly/yearly fee
- **Format**: `{"subscription_cost_monthly": "$9.99", "subscription_cost_yearly": "$99.99"}`
- **Source**: Official subscription policy

---

## Data Format Specification

### JSON Structure
```json
{
  "objective_data": {
    "technical_specs": {...},
    "performance_data": {...},
    "reliability_data": {...},
    "market_data": {...},
    "sustainability_data": {...},
    "cost_data": {...}
  },
  "data_completeness": {
    "technical_specs_score": 0.8,
    "performance_data_score": 0.5,
    "reliability_data_score": 0.3,
    "market_data_score": 0.75,
    "sustainability_data_score": 0.4,
    "cost_data_score": 0.9,
    "overall_score": 0.6
  }
}
```

### Data Completeness Score
- **0.0-0.2**: Severe data gaps
- **0.3-0.5**: Insufficient data
- **0.6-0.8**: Basically complete
- **0.9-1.0**: Complete

### Data Priority
1. **Tier 1 (Required)**: Technical specs, cost data
2. **Tier 2 (Important)**: Market data, reliability data
3. **Tier 3 (Optional)**: Performance data, sustainability data

---

## Data Source Requirements

### Acceptable Sources
1. **Official sources**:
   - Official product page
   - Official spec sheet
   - Official technical documentation

2. **Third-party reviews**:
   - Professional review sites (e.g., AnTuTu, Geekbench, Tom's Hardware)
   - Media reviews (e.g., The Verge, TechCrunch)
   - Independent review institutions

3. **User data**:
   - E-commerce user reviews (aggregated)
   - Social media user feedback (deduplicated and verified)
   - Consumer reports

4. **Certification data**:
   - Industry certification (e.g., Energy Star, CE, FCC)
   - Third-party certification data

### Unacceptable Sources
1. **Marketing language**: Ads, promotional copy
2. **Unverified claims**: Assertions without evidence
3. **Anonymous reviews**: Unverifiable user reviews
4. **Competitor comparison**: Competitor promotional materials

### Data Verification
- **Cross-validation**: Data consistent across sources is more credible
- **Timestamp**: Note data collection time
- **Source attribution**: Every data point must cite source

---

## Validation Standards

### Objectivity Validation
- [ ] Is data factual rather than opinion?
- [ ] Can data be independently verified?
- [ ] Does data include subjective adjectives?

### Completeness Validation
- [ ] Are all required data items present?
- [ ] Is data completeness score > 0.6?
- [ ] Does missing data affect assessment?

### Consistency Validation
- [ ] Does data format comply with specification?
- [ ] Are units consistent?
- [ ] Are value ranges reasonable?

### Timeliness Validation
- [ ] Is data current?
- [ ] Was data collected within 6 months?
- [ ] Has product been updated?

---

## Objective Data Handling in Brand Blinding

### Objective Data to Retain
- All technical specs (processor, memory, storage, etc.)
- All performance data (test results, measured data)
- All reliability data (failure rate, warranty)
- All market data (sales, reviews)
- All sustainability data (materials, energy)
- All cost data (price, fees)

### Content to Remove
- Brand names
- Marketing language ("revolutionary", "game-changing", etc.)
- Emotional descriptions ("amazing", "stunning", etc.)
- Unverified claims
- Exaggerated claims

### Processing Example
```
Original: Apple M2 chip delivers revolutionary performance
Objective data: processor: "M2", performance_score: "high"
Remove: brand name, "revolutionary" (marketing)
Retain: processor model, performance data
```

---

## Usage Guide

### For Auditors
1. **Use objective data only**: All scores must be based on objective data
2. **Cite data sources**: Every score must cite objective data source
3. **Verify data completeness**: Check data completeness score
4. **Note data gaps**: If data is missing, state in report

### For Brand Blinding
1. **Retain all objective data**: Do not remove any objective data
2. **Distinguish objective data vs. marketing**: Distinguish carefully
3. **Preserve data format**: Keep original format of objective data
4. **Source attribution**: Retain source attribution for objective data

### For Final Judge
1. **Check data completeness**: Verify all objective data is complete
2. **Verify data sources**: Confirm source reliability
3. **Check data consistency**: Verify data format consistency
4. **Assess data impact**: Assess impact of data gaps on judgment
