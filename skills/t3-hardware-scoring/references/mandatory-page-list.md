# Mandatory Page List

## Purpose

Ensure **consistent data input** for every T3 audit by using a fixed crawl list per site type. The Agent must follow this list and not add or remove page types arbitrarily.

---

## Site Type Identification

| Site Type | Detection | List Used |
|-----------|-----------|-----------|
| **Shopify** | URL contains `myshopify.com`, or typical paths like `*.com/pages/`, `*.com/policies/` | Shopify list |
| **Kickstarter** | URL contains `kickstarter.com/projects/` | Kickstarter list |
| **Unrecognized** | None of above | Default to Shopify S1, S2; rest optional |

---

## Shopify List

Parse `{domain}` from user URL (e.g. `nunatechnology.com`), then construct URLs as below.

| # | Page Type | URL Derivation | Required | Use |
|---|-----------|----------------|----------|-----|
| S1 | Homepage | `https://{domain}/` | **Yes** | Product overview, marketing, main product links |
| S2 | Product | User-provided product URL or main product from S1 | **Yes** | Price, specs, reviews, in-the-box |
| S3 | How it works | `https://{domain}/pages/how-it-works` | No | Technical description, how it works |
| S4 | FAQ | `https://{domain}/pages/faq` | No | Q&A, subscription, connectivity |
| S5 | Refund/Warranty | `https://{domain}/policies/refund-policy` | No | Returns, warranty |
| S6 | Shipping | `https://{domain}/policies/shipping-policy` | No | Delivery, DOA |
| S7 | Privacy | `https://{domain}/policies/privacy-policy` | No | Data, cloud, privacy |
| S8 | User guide / Support | `https://{domain}/pages/user-guide` or `.../pages/support` | No | App links, troubleshooting |

### Shopify Rules

- **S1, S2** required; if unavailable, note reason
- **S3–S8** try in order; if 404 or inaccessible, mark `status: unavailable` in `01-level0-source-urls.md`
- In `02-level0-extracts.md`, use `## S{n} — [Type]\n(not retrieved)` for missing sections
- For S8, try `/pages/user-guide` first, then `/pages/support` if 404

---

## Kickstarter List

Project URL format: `https://www.kickstarter.com/projects/{creator}/{slug}`

| # | Page Type | URL Derivation | Required | Use |
|---|-----------|----------------|----------|-----|
| S1 | Project main | User-provided project URL | **Yes** | Description, goal, rewards, risks, story |
| S2 | Updates | `{project_url}/posts` or updates section on main page | No | Progress updates |
| S3 | Comments | Comments section on main page or `{project_url}/comments` | No | Backer feedback |

### Kickstarter Rules

- **S1** required; main page usually has most info
- **S2, S3** supplementary; Updates/comments may be embedded; try separate URLs or parse main page sections
- If S2/S3 have no separate URL or cannot be separated, note `(in main page or not separable)`

---

## Output Format

### 01-level0-source-urls.md

```markdown
# Level 0 (Sealed) — Source URLs

Collected on: YYYY-MM-DD
Site type: Shopify | Kickstarter

| ID | Type | URL | Status |
|----|------|-----|--------|
| S1 | Homepage | https://... | ok |
| S2 | Product | https://... | ok |
| S3 | How it works | https://... | unavailable |
...
```

- `Status`: `ok` | `unavailable`
- Keep S1, S2, … order; do not skip IDs

### 02-level0-extracts.md

```markdown
# Level 0 (Sealed) — Raw Extracts

## S1 — Homepage
(crawled content)

## S2 — Product
(crawled content)

## S3 — How it works
(not retrieved)
...
```

- Each S{n} maps to a `## S{n} — [Type]` block
- Use `(not retrieved)` for unavailable sections; do not omit blocks

---

## Integration with SKILL Flow

In Step 2 “Get Product Information”:

1. **Read** this file `mandatory-page-list.md`
2. Identify site type from user URL
3. Fetch per list, record results
4. Write `01-level0-source-urls.md` and `02-level0-extracts.md` per format above
