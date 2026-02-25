# Organize Guide

## Purpose

Merge multiple crawled pages into a single, well-structured markdown document for downstream processing. Crucially, this document must act as a **Chain of Evidence**, preserving exact phrasing and source traceability so downstream Auditors can extract exact quotes for their 0-3 rubrics.

## Input

Raw extracts from crawl: multiple sections (e.g. `## S1 — Homepage`, `## S2 — Product`, `## S3 — Tech`) with content from different pages.

## Output Structure

Produce a single markdown document with these sections. **You must retain the Source Tags (e.g., [S1], [S2]) next to the information** so Auditors can cite where a quote came from.

1. **Product Overview** — Core product description, model name, category, key value proposition.
2. **Product Features and Capabilities** — Features, apps, integrations (QuickNote, Dashboard, Teleprompt, etc.).
3. **Technical Specifications** — Specs when available (display, battery, connectivity, sensors, weight, dimensions).
4. **User Feedback & Reviews** — (Critical for Auditors) Exact quotes from testimonials or reviews.
5. **Policies & Support** — Shipping, returns, warranty, user guide, FAQ.

## Rules

* **Preserve Exact Phrasing** — Do not aggressively paraphrase. Downstream auditors rely on exact quotes for their `verbatim_evidence` arrays. If a metric or claim is made, keep the original sentence structure.
* **Maintain Traceability** — Append the source tag to bullet points or paragraphs (e.g., "Battery lasts 18 hours. [S3]").
* **Deduplicate Carefully** — When the same info appears on multiple pages, keep the version with the most specific, quantified data.
* **Handle missing sections** — If a section has no content, omit it. Do not add placeholder text.

## Example

**Input** (fragments):

```markdown
## S1 — Homepage
Experience the ultimate workflow with our 4K teleprompter.
## S3 — Tech
Display: 4K OLED. Weight: 1.2kg.

```

**Output**:

```markdown
# Product Information (Organized)

## Product Overview
Experience the ultimate workflow with our 4K teleprompter. [S1]

## Technical Specifications
- Display: 4K OLED [S3]
- Weight: 1.2kg [S3]

