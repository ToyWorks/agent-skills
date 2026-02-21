#!/usr/bin/env python3
"""
Product info crawler (enhanced)
Uses Jina AI Reader API to extract web content and parse product info; collects complete objective data
"""

import argparse
import json
import sys
import re
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup


def crawl_webpage(url: str) -> dict:
    """
    Crawl webpage content using Jina AI Reader API.

    Args:
        url: Product page URL

    Returns:
        Dict with webpage content and metadata
    """
    try:
        # Use Jina AI Reader API
        jina_api_url = f"https://r.jina.ai/http://{url}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = requests.get(jina_api_url, headers=headers, timeout=30)
        response.raise_for_status()

        return {
            "status": "success",
            "url": url,
            "content": response.text,
            "raw_html": response.text
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "url": url,
            "error": f"Crawl failed: {str(e)}"
        }


def extract_objective_specs(text_content: str) -> dict:
    """
    Extract objective data from text.

    Args:
        text_content: Webpage text content

    Returns:
        Dict of objective data
    """
    specs = {}

    # Processor info
    processor_patterns = [
        r'(\w+)\s+(\d+)-core\s*(?:processor|CPU)',
        r'(Intel\s+\w+\s+\w+|AMD\s+\w+\s+\w+|Snapdragon\s+\w+)',
        r'(M\d|M\d\s+Pro|M\d\s+Max)',
    ]
    for pattern in processor_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['processor'] = matches[0] if isinstance(matches[0], str) else ' '.join(matches[0])
            break

    # Storage capacity
    storage_patterns = [
        r'(\d+)\s*(?:GB|TB)\s*(?:SSD|HDD|storage|memory)',
        r'(\d+)\s*GB\s*(?:ROM|Storage)',
    ]
    for pattern in storage_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['storage'] = matches[0]
            break

    # RAM
    ram_patterns = [
        r'(\d+)\s*GB\s*(?:RAM|memory)',
        r'(\d+)GB\s+LPDDR\d+',
    ]
    for pattern in ram_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['ram'] = matches[0]
            break

    # Screen params
    screen_patterns = [
        r'(\d+\.?\d*)\s*(?:inch|")\s*(\d+x\d+)',
        r'(\d+Hz)\s*refresh\s*rate',
    ]
    for pattern in screen_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            if 'screen' not in specs:
                specs['screen'] = {}
            for match in matches:
                if isinstance(match, tuple):
                    if 'x' in match[1]:
                        specs['screen']['resolution'] = match[1]
                    else:
                        specs['screen']['size'] = match[0]
                else:
                    specs['screen']['refresh_rate'] = match

    # Battery capacity
    battery_patterns = [
        r'(\d+)\s*mAh',
        r'(\d+)\s*Wh',
    ]
    for pattern in battery_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['battery_capacity'] = matches[0]
            break

    # Battery life
    battery_life_patterns = [
        r'(?:up\s*to\s*)?(\d+)\s*hours?\s*(?:battery|life)',
        r'(\d+)\s*h\s*battery',
    ]
    for pattern in battery_life_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['battery_life_claimed'] = f"{matches[0]} hours"
            break

    # IP rating
    ip_patterns = [
        r'IP(\d+)',
    ]
    for pattern in ip_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['ip_rating'] = f"IP{matches[0]}"
            break

    # WiFi version
    wifi_patterns = [
        r'Wi-Fi\s*(\d+)',
        r'WiFi\s*(\d+)',
    ]
    for pattern in wifi_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['wifi_version'] = f"Wi-Fi {matches[0]}"
            break

    # Bluetooth version
    bluetooth_patterns = [
        r'Bluetooth\s*(\d+\.\d+)',
        r'BT\s*(\d+\.\d+)',
    ]
    for pattern in bluetooth_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['bluetooth_version'] = f"Bluetooth {matches[0]}"
            break

    # Sensor list
    sensor_keywords = ['accelerometer', 'gyroscope', 'heart rate', 'blood oxygen',
                      'temperature', 'humidity', 'GPS', 'proximity', 'ambient light']
    sensors = []
    for keyword in sensor_keywords:
        if keyword.lower() in text_content.lower():
            sensors.append(keyword)
    if sensors:
        specs['sensors'] = sensors

    # Weight
    weight_patterns = [
        r'(\d+\.?\d*)\s*(?:g|kg|grams?|kilograms?)',
    ]
    for pattern in weight_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['weight'] = matches[0]
            break

    # Dimensions
    dimension_patterns = [
        r'(\d+\.?\d*)\s*[x×]\s*(\d+\.?\d*)\s*[x×]\s*(\d+\.?\d*)\s*(?:mm|cm)',
    ]
    for pattern in dimension_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['dimensions'] = f"{matches[0][0]}x{matches[0][1]}x{matches[0][2]}mm"
            break

    return specs


def extract_market_data(soup: BeautifulSoup, url: str) -> dict:
    """
    Extract market data.

    Args:
        soup: BeautifulSoup object
        url: Original URL

    Returns:
        Market data dict
    """
    market_data = {}

    # Review count
    review_patterns = [
        r'(\d+(?:,\d+)*)\s*reviews?',
        r'(\d+(?:,\d+)*)\s*ratings?',
    ]
    text_content = soup.get_text()
    for pattern in review_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            market_data['review_count'] = matches[0].replace(',', '')
            break

    # Average rating
    rating_patterns = [
        r'(\d\.?\d*)\s* out of \d+',
        r'(\d\.?\d*)\s*/\s*\d+',
    ]
    for pattern in rating_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            market_data['average_rating'] = matches[0]
            break

    # Release date (infer from URL or content)
    date_patterns = [
        r'(\d{4})',
        r'(?:released|launched)\s*(?:in\s*)?(\d{4})',
    ]
    for pattern in date_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            # Take max year (most recent product)
            years = [int(m) if isinstance(m, str) else m for m in matches]
            max_year = max([y for y in years if 2000 <= y <= 2030])
            market_data['release_year'] = max_year
            break

    return market_data


def extract_reliability_data(text_content: str) -> dict:
    """
    Extract reliability data.

    Args:
        text_content: Text content

    Returns:
        Reliability data dict
    """
    reliability = {}

    # Warranty
    warranty_patterns = [
        r'(\d+)-year\s*warranty',
        r'(\d+)\s*year\s*warranty',
        r'(\d+)\s*months?\s*warranty',
    ]
    for pattern in warranty_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            warranty_value = int(matches[0])
            if 'month' in pattern.lower():
                reliability['warranty_months'] = warranty_value
            else:
                reliability['warranty_years'] = warranty_value
            break

    # IP rating (extracted above)

    return reliability


def extract_sustainability_data(text_content: str) -> dict:
    """
    Extract sustainability data.

    Args:
        text_content: Text content

    Returns:
        Sustainability data dict
    """
    sustainability = {}

    # Material keywords
    material_keywords = {
        'aluminum': 'aluminum',
        'steel': 'steel',
        'glass': 'glass',
        'plastic': 'plastic',
        'bamboo': 'bamboo',
        'recyclable': 'recyclable_material',
        'biodegradable': 'biodegradable',
        'eco-friendly': 'eco_friendly'
    }

    materials = []
    for keyword, material_type in material_keywords.items():
        if keyword.lower() in text_content.lower():
            materials.append(material_type)

    if materials:
        sustainability['materials'] = materials

    # Energy efficiency
    energy_keywords = ['energy star', 'energy efficient', 'low power', 'energy saving']
    for keyword in energy_keywords:
        if keyword.lower() in text_content.lower():
            sustainability['energy_efficient'] = True
            break

    # Repairability
    repair_keywords = ['repairable', 'replaceable battery', 'modular', 'user-replaceable']
    for keyword in repair_keywords:
        if keyword.lower() in text_content.lower():
            sustainability['repairable'] = True
            break

    return sustainability


def extract_product_info(url: str, content: str) -> dict:
    """
    Extract product info from webpage content (enhanced).

    Args:
        url: Original URL
        content: Webpage content

    Returns:
        Structured product info dict (including complete objective data)
    """
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Extract title
    title = ""
    if soup.title:
        title = soup.title.string.strip()
    elif soup.h1:
        title = soup.h1.get_text().strip()

    # Extract meta description
    description = ""
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        description = meta_desc.get('content', '')

    # Extract main content paragraphs
    main_content = ""
    paragraphs = soup.find_all('p')
    if paragraphs:
        main_content = "\n\n".join([p.get_text().strip() for p in paragraphs[:10] if p.get_text().strip()])

    # Extract price
    price = ""
    price_patterns = [
        r'\$\d+[\d,]*(?:\.\d{2})?',
        r'USD\s*\d+[\d,]*(?:\.\d{2})?',
        r'￥\d+[\d,]*(?:\.\d{2})?',
        r'¥\d+[\d,]*(?:\.\d{2})?',
    ]
    text_content = soup.get_text()
    for pattern in price_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            price = matches[0]
            break

    # Extract feature list
    features = []
    feature_lists = soup.find_all(['ul', 'ol'])
    for ul in feature_lists:
        items = [li.get_text().strip() for li in ul.find_all('li') if li.get_text().strip()]
        if items:
            features.extend(items)

    features = features[:20] if len(features) > 20 else features

    # Extract domain
    domain = urlparse(url).netloc

    # Extract objective data
    text_content_lower = text_content.lower()

    # Technical specs
    objective_specs = extract_objective_specs(text_content)

    # Market data
    market_data = extract_market_data(soup, url)

    # Reliability data
    reliability_data = extract_reliability_data(text_content)

    # Sustainability data
    sustainability_data = extract_sustainability_data(text_content)

    # Cost data
    cost_data = {}
    subscription_patterns = [
        r'\$(\d+(?:\.\d+)?)\s*(?:per month|monthly|subscription)',
        r'(\d+)\s*(?:dollars?|USD)\s*(?:per month|monthly)',
    ]
    for pattern in subscription_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            cost_data['subscription_cost_monthly'] = f"${matches[0]}/month"
            break

    return {
        "url": url,
        "domain": domain,
        "title": title,
        "description": description,
        "main_content": main_content,
        "price": price,
        "features": features,
        "extraction_method": "beautifulsoup",
        "content_length": len(content),

        # Objective data summary
        "objective_data": {
            "technical_specs": objective_specs,
            "market_data": market_data,
            "reliability_data": reliability_data,
            "sustainability_data": sustainability_data,
            "cost_data": cost_data
        },

        # Data completeness
        "data_completeness": {
            "technical_specs_score": len(objective_specs) / 10,
            "market_data_score": len(market_data) / 4,
            "reliability_data_score": len(reliability_data) / 3,
            "sustainability_data_score": len(sustainability_data) / 3,
            "overall_score": 0  # computed below
        }
    }


def main():
    parser = argparse.ArgumentParser(description='Crawl product page info (enhanced)')
    parser.add_argument('--url', required=True, help='Product page URL')
    parser.add_argument('--output', '-o', help='Output file path (JSON)')
    parser.add_argument('--pretty', action='store_true', help='Pretty-print JSON output')

    args = parser.parse_args()

    # Crawl webpage
    print(f"Crawling: {args.url}", file=sys.stderr)
    result = crawl_webpage(args.url)

    if result["status"] == "error":
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # Extract product info
    print("Parsing product info...", file=sys.stderr)
    product_info = extract_product_info(args.url, result["content"])

    # Compute overall data completeness score
    completeness = product_info["data_completeness"]
    completeness["overall_score"] = (
        completeness["technical_specs_score"] * 0.4 +
        completeness["market_data_score"] * 0.2 +
        completeness["reliability_data_score"] * 0.2 +
        completeness["sustainability_data_score"] * 0.2
    )

    # Output result
    if args.pretty:
        print(json.dumps(product_info, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(product_info, ensure_ascii=False))

    # Save to file (optional)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.pretty:
                json.dump(product_info, f, ensure_ascii=False, indent=2)
            else:
                json.dump(product_info, f, ensure_ascii=False)
        print(f"\nResult saved to: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
