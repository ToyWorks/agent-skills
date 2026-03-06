#!/usr/bin/env python3
"""
T3 Product Info Crawler — v2.0
Multi-strategy crawl: Jina AI Reader (primary) → direct requests (fallback)
Returns clean markdown-based chain-of-evidence for Brand Blinding.
"""

import argparse
import json
import re
import sys
from urllib.parse import urlparse
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: 'requests' not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)


# ─── Crawl strategies ─────────────────────────────────────────────────────────

def crawl_via_jina(url: str, timeout: int = 30) -> Optional[str]:
    """
    Crawl via Jina AI Reader. Returns clean markdown or None on failure.
    Jina endpoint: https://r.jina.ai/{full_url}
    """
    jina_url = f"https://r.jina.ai/{url}"
    headers = {
        "Accept": "text/plain",
        "User-Agent": "Mozilla/5.0 (compatible; T3Auditor/2.0)",
    }
    try:
        resp = requests.get(jina_url, headers=headers, timeout=timeout)
        if resp.status_code == 200 and len(resp.text) > 200:
            return resp.text
        return None
    except requests.RequestException:
        return None


def crawl_direct(url: str, timeout: int = 20) -> Optional[str]:
    """
    Direct HTTP GET with basic text extraction. Fallback when Jina fails.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        # Very light extraction: strip HTML tags
        text = re.sub(r"<[^>]+>", " ", resp.text)
        text = re.sub(r"\s{3,}", "\n\n", text)
        return text[:20000]  # cap at 20k chars
    except requests.RequestException:
        return None


def crawl(url: str) -> dict:
    """
    Try Jina first, then direct. Returns dict with content + strategy used.
    """
    print(f"[crawl] Trying Jina: {url}", file=sys.stderr)
    content = crawl_via_jina(url)
    if content:
        return {"status": "success", "strategy": "jina", "url": url, "content": content}

    print("[crawl] Jina failed, trying direct HTTP...", file=sys.stderr)
    content = crawl_direct(url)
    if content:
        return {"status": "success", "strategy": "direct", "url": url, "content": content}

    return {
        "status": "error",
        "strategy": "none",
        "url": url,
        "content": "",
        "error": "All crawl strategies failed. Use Exa MCP or manual paste as fallback.",
    }


# ─── Spec extraction ──────────────────────────────────────────────────────────

SPEC_PATTERNS = {
    "weight":       r"(\d+\.?\d*)\s*(?:g|grams?)\b",
    "battery_mah":  r"(\d{3,5})\s*mAh",
    "battery_life": r"(?:up to\s+)?(\d+\.?\d*)\s*hours?\s*(?:battery|life|of use)",
    "ip_rating":    r"\b(IP\d{2}[A-Z]?)\b",
    "storage_gb":   r"(\d+)\s*GB\s*(?:storage|onboard|internal|ROM)",
    "camera_mp":    r"(\d+\.?\d*)\s*MP",
    "video_res":    r"(\d{3,4}p(?:\s*@\s*\d+\s*fps)?)",
    "bluetooth":    r"Bluetooth\s*(\d+\.\d+)",
    "wifi":         r"Wi-?Fi\s*(\d+(?:\.\d+)?|[a-z/]+)",
    "display":      r"(\d+\.?\d*)\s*[\"']\s*(?:display|screen|OLED|LCD|AMOLED)",
    "price_usd":    r"\$\s*(\d{1,4}(?:,\d{3})?(?:\.\d{2})?)",
    "subscription": r"\$(\d+\.?\d*)\s*(?:/\s*month|per\s*month|monthly)",
}


def extract_specs(text: str) -> dict:
    specs = {}
    for key, pattern in SPEC_PATTERNS.items():
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            specs[key] = m.group(1) if m.lastindex and m.lastindex >= 1 else m.group(0)
    return specs


def identify_site_type(url: str, content: str) -> str:
    """Identify e-commerce platform type."""
    domain = urlparse(url).netloc.lower()
    if "shopify" in content[:2000] or "cdn.shopify" in content:
        return "Shopify"
    if "kickstarter.com" in domain:
        return "Kickstarter"
    if "indiegogo.com" in domain:
        return "Indiegogo"
    if "amazon.com" in domain:
        return "Amazon"
    return "Unknown"


def extract_reviews(text: str, max_quotes: int = 8) -> list:
    """
    Extract review-like sentences: short, opinionated, with sentiment indicators.
    """
    sentiment_words = [
        "love", "hate", "great", "terrible", "amazing", "awful", "excellent",
        "poor", "perfect", "disappointed", "worth", "recommend", "avoid",
        "impressed", "surprised", "ridiculous", "brilliant", "flimsy", "robust",
        "impossible", "frustrating", "intuitive", "confusing", "flimsy",
    ]
    sentences = re.split(r"(?<=[.!?])\s+", text)
    reviews = []
    for s in sentences:
        s = s.strip()
        if 20 < len(s) < 300:
            sl = s.lower()
            if any(w in sl for w in sentiment_words):
                reviews.append(s)
        if len(reviews) >= max_quotes:
            break
    return reviews


# ─── Exa hint ─────────────────────────────────────────────────────────────────

EXA_FALLBACK_HINT = """
NOTE: Crawl returned insufficient content.
Use Exa MCP as fallback:

  mcporter call 'exa.web_search_exa(query: "{product} specs review", numResults: 5)'
  mcporter call 'exa.company_research_exa(companyName: "{brand}", numResults: 3)'

Then manually paste the results as additional source text.
"""


# ─── Main ─────────────────────────────────────────────────────────────────────

def build_output(url: str, raw: dict) -> dict:
    content = raw.get("content", "")
    strategy = raw.get("strategy", "none")
    sufficient = len(content) > 500

    specs = extract_specs(content) if sufficient else {}
    reviews = extract_reviews(content) if sufficient else []
    site_type = identify_site_type(url, content) if sufficient else "Unknown"

    result = {
        "status": raw["status"],
        "crawl_strategy": strategy,
        "url": url,
        "site_type": site_type,
        "content_length": len(content),
        "content_sufficient": sufficient,
        "extracted_specs": specs,
        "review_quotes": reviews,
        "raw_content": content[:15000],  # cap for downstream LLM context
    }

    if not sufficient:
        domain = urlparse(url).netloc.replace("www.", "")
        result["fallback_hint"] = EXA_FALLBACK_HINT.replace("{product}", domain).replace("{brand}", domain)

    return result


def main():
    parser = argparse.ArgumentParser(description="T3 Product Crawler v2.0")
    parser.add_argument("--url", required=True, help="Product page URL")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()

    raw = crawl(args.url)
    output = build_output(args.url, raw)

    indent = 2 if args.pretty else None
    out_str = json.dumps(output, ensure_ascii=False, indent=indent)
    print(out_str)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"Saved to: {args.output}", file=sys.stderr)

    if not output["content_sufficient"]:
        print(output.get("fallback_hint", ""), file=sys.stderr)
        sys.exit(2)  # exit 2 = soft failure, needs manual supplement


if __name__ == "__main__":
    main()
