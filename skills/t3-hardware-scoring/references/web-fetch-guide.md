# Agent Web Information Extraction Complete Guide

## Shopify and Kickstarter Mandatory Crawl List

**Must** read [mandatory-page-list.md](mandatory-page-list.md) and execute the mandatory crawl list per site type to ensure consistent data input for each audit.

### Execution Points

1. **Identify site type**: URL contains `kickstarter.com/projects/` → Kickstarter; otherwise default to Shopify
2. **Fetch in list order**: S1, S2 are required; S3 and beyond try in order; 404 or inaccessible = mark `status: unavailable`
3. **Fixed output format**:
   - `01-level0-source-urls.md`: Table columns `ID | Type | URL | Status`
   - `02-level0-extracts.md`: Blocks by `## S1 — [Type]`, `## S2 — [Type]`, etc.; write `(not retrieved)` for failed fetches
4. **Do not add/remove page types**: Pages outside the list may supplement, but S1–Sn structure must be preserved

### URL Derivation and 404 Handling

- **Shopify**: Parse `{domain}` from user URL; construct S3–S8 URLs per `mandatory-page-list.md` (e.g., `{domain}/pages/how-it-works`)
- **Kickstarter**: S1 = user-provided project URL; S2 try `{project_url}/posts`
- **404**: That page `status: unavailable`; in `02-level0-extracts.md` write `(not retrieved)` for that block; do not omit the block

---

## Table of Contents
- [Shopify and Kickstarter Mandatory Crawl List](#shopify-and-kickstarter-mandatory-crawl-list)
- [Common Issues](#common-issues)
- [Multi-Strategy Extraction Methods](#multi-strategy-extraction-methods)
- [Key Information Extraction Checklist](#key-information-extraction-checklist)
- [Strategies by Website Type](#strategies-by-website-type)
- [Data Completeness Validation](#data-completeness-validation)

## Common Issues

### Why is Agent Information Incomplete?

**Cause analysis**:

1. **Dynamic content loading**
   - Price, inventory, etc. may load via JavaScript
   - web_fetch may only get initial HTML
   - Solution: Visit multiple pages or use pagination parameters

2. **Complex page structure**
   - E-commerce sites may use heavy CSS/JS rendering
   - Key info may be in iframes, modals, or tabs
   - Solution: Try different URL variants

3. **Anti-scraping**
   - Some sites limit access rate
   - May need specific User-Agent or Cookie
   - Solution: Retry with different access strategies

4. **Content truncation**
   - web_fetch `limit` may truncate content
   - Single fetch may not get full page
   - Solution: Paginated fetch, increase `limit`

5. **Login wall or region restriction**
   - Some info requires login
   - May vary by region
   - Solution: Find public spec pages

## Multi-Strategy Extraction Methods

### Strategy 1: Multi-Page Access

**Problem**: Single product page may have incomplete info

**Solution**: Visit multiple related pages

```
Page combination:
1. Product detail page - Basic info, price, features
2. Product spec page - Tech parameters, dimensions, weight
3. User review page - User feedback, usage experience
4. Comparison page - Competitor comparison
5. Official support page - Reliability, warranty
```

**Execution**:
```
# Step 1: Visit product detail page
web_fetch(url="product_detail_url", limit=8000)

# Step 2: Visit spec page (if separate)
web_fetch(url="product_spec_url", limit=8000)

# Step 3: Visit review page (if available)
web_fetch(url="review_page_url", limit=8000)
```

### Strategy 2: URL Variant Attempts

**Problem**: Same product may have multiple URL entry points

**Solution**: Try different URL formats

**E-commerce URL patterns**:
```
Base URL: https://www.example.com/product/123

Possible variants:
- https://www.example.com/product/123/specs
- https://www.example.com/product/123/reviews
- https://www.example.com/p/123
- https://www.example.com/item/123
- https://m.example.com/product/123 (mobile)
```

**Execution**:
```
# Try different URL variants
web_fetch(url="base_url")
web_fetch(url="base_url/specs")
web_fetch(url="base_url/reviews")
```

### Strategy 3: Paginated Fetch

**Problem**: web_fetch `limit` may truncate content

**Solution**: Use `offset` for paginated fetch

```
# Page 1
web_fetch(url="product_url", offset=0, limit=4000)

# Page 2
web_fetch(url="product_url", offset=4000, limit=4000)

# Page 3
web_fetch(url="product_url", offset=8000, limit=4000)
```

### Strategy 4: Search Engine Assistance

**Problem**: Direct product page has incomplete info

**Solution**: Use search to find more sources

```
# Use web_search for product info
web_search(query="product_model + specs")
web_search(query="product_model + review")
web_search(query="product_model + price")

# Visit authoritative pages from results
web_fetch(url="search_result_page_url")
```

## Key Information Extraction Checklist

### Required Information

#### 1. Basic Information
- [ ] Product name (full model)
- [ ] Brand (for pre-Brand Blinding record)
- [ ] Product category
- [ ] Release/launch date

#### 2. Price
- [ ] Current price
- [ ] Original/retail price
- [ ] Discount info
- [ ] Regional price differences

**Price extraction challenges and solutions**:
```
Challenge 1: Dynamic price
- Solve: Look for schema.org structured data
- Solve: Look for JSON-LD or Microdata markup
- Solve: Look for price history pages

Challenge 2: Multi-variant price
- Solve: Record base price and variant prices
- Solve: Clearly mark "starting at"

Challenge 3: Region difference
- Solve: Mark price region clearly
- Solve: Record currency
```

#### 3. Technical Specs
- [ ] Core parameters (dimensions, weight, materials)
- [ ] Performance (speed, capacity, power)
- [ ] Connectivity (interfaces, wireless protocols)
- [ ] Battery life (if portable)
- [ ] Compatibility requirements

#### 4. User Reviews
- [ ] Average rating
- [ ] Review count
- [ ] Common positives
- [ ] Common negatives
- [ ] Use case feedback

#### 5. Reliability Data
- [ ] Warranty period
- [ ] Failure rate (if available)
- [ ] Common issues
- [ ] After-sales quality

#### 6. Sustainability
- [ ] Materials (eco-friendly)
- [ ] Energy rating
- [ ] Repairability
- [ ] Packaging sustainability

## Strategies by Website Type

### E-commerce (Amazon, JD, Taobao, etc.)

**Characteristics**:
- Rich but complex structure
- Heavy dynamic loading
- Possible anti-scraping

**Strategy**:
```
1. Visit product detail page
2. Visit product spec page (if separate)
3. Visit review section
4. Use paginated fetch for full content
5. Find "Product details" or "Parameters" section
```

**Key info locations**:
- Price: Usually top of page; may include tax, shipping
- Specs: May be in "Details", "Parameters" tab
- Reviews: Separate section or bottom of page

### Official Sites (Apple, Dyson, etc.)

**Characteristics**:
- Accurate but possibly marketing-heavy
- Good design may affect scraping
- Regional differences possible

**Strategy**:
```
1. Visit product homepage
2. Visit "Technical specifications" page
3. Visit "Compare" page
4. Find PDF manual or spec sheet
5. Find support page for reliability
```

### Review Sites (The Verge, Engadget, etc.)

**Characteristics**:
- Objective and in-depth
- Professional perspective
- Possible comparison tests

**Strategy**:
```
1. Visit review homepage
2. Find pros/cons summary
3. Find performance test data
4. Find competitor comparison
```

## Data Completeness Validation

### Validation Checklist

After extraction, Agent should verify:

```markdown
## Data Completeness Check

### Basic Information (must be complete)
- [ ] Product name: Retrieved
- [ ] Price: Retrieved OR missing reason stated
- [ ] Main features: Retrieved

### Technical Specs (at least 50%)
- [ ] Core parameters: Retrieved ___ items, missing ___ items
- [ ] Missing key parameters: [list]

### User Feedback (at least one)
- [ ] Rating: Retrieved
- [ ] OR review count: Retrieved
- [ ] OR typical feedback: Retrieved

### Reliability Data (optional but important)
- [ ] Warranty: Retrieved OR not found
- [ ] Failure data: Retrieved OR not found
```

### Handling Missing Information

**When key info is missing**:

1. **Price missing**
   ```
   Solutions:
   - Try cart page (may show price)
   - Search "product name + price"
   - Find same product on other platforms
   - Clearly note "Price information missing" in report
   ```

2. **Technical specs missing**
   ```
   Solutions:
   - Find official PDF manual
   - Search "product model + specs"
   - Find tech databases (e.g., GSMArena for phones)
   - Visit competitor comparison page (may include specs)
   ```

3. **User reviews missing**
   ```
   Solutions:
   - Find third-party review sites
   - Search "product model + review"
   - Find forum discussions (Reddit, etc.)
   - Note "Limited user feedback sample" in report
   ```

### Supplementary Sources

When primary source is incomplete, Agent should:

```
Supplementary source priority:
1. Official support page (reliability data)
2. Third-party review sites (objective reviews)
3. User forums and communities (real feedback)
4. Technical databases (detailed specs)
5. Competitor comparison pages (relative advantages)
```

## Agent Execution Recommendations

### Best Practices

1. **Multi-page access**: Do not rely on a single page
2. **Stepwise extraction**: Get basics first, then add details
3. **Proactive validation**: Check completeness after extraction; supplement missing info
4. **Honest documentation**: Clearly note what could not be retrieved and why

### Execution Template

```markdown
## Product Information Extraction Record

### Step 1: Visit product homepage
- URL: [product_url]
- Retrieved: [list]
- Missing: [list]

### Step 2: Visit spec page
- URL: [spec_url]
- Retrieved: [list]
- Missing: [list]

### Step 3: Visit review/review page
- URL: [review_url]
- Retrieved: [list]
- Missing: [list]

### Step 4: Search for supplementary info
- Query: [search_terms]
- Found: [supplementary info]

### Data Completeness Assessment
- Basic info: Complete / Partial / Incomplete
- Technical specs: Complete / Partial / Incomplete
- User feedback: Complete / Partial / Incomplete
- Reliability data: Complete / Partial / Incomplete

### Unavailable Information and Reasons
- [item]: [reason]
```

## Notes

1. **Do not assume data**: If price not found, do not infer from other info
2. **Multi-source verification**: Important info should be verified across sources
3. **Honest documentation of gaps**: Clearly state what could not be retrieved
4. **Stay objective**: Do not let missing info bias assessment
5. **Use Agent capabilities**: Agent can understand context and is more flexible than scripts

## Integration with Brand Blinding

After extraction, Brand Blinding is required:

```
Raw information → Brand Blinding → Brand-Blinded information

Retain: Technical specs, performance data, user reviews
Remove: Brand names, marketing language, emotional descriptions
```

See [references/defluff-guide.md](defluff-guide.md) for details.
