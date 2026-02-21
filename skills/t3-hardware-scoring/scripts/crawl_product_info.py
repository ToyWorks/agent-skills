#!/usr/bin/env python3
"""
产品信息爬取脚本（增强版）
使用Jina AI Reader API提取网页内容并解析产品信息，完整收集客观数据
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
    使用Jina AI Reader API爬取网页内容

    参数:
        url: 产品页面URL

    返回:
        包含网页内容和元数据的字典
    """
    try:
        # 使用Jina AI Reader API
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
            "error": f"爬取失败: {str(e)}"
        }


def extract_objective_specs(text_content: str) -> dict:
    """
    从文本中提取客观数据

    参数:
        text_content: 网页文本内容

    返回:
        客观数据字典
    """
    specs = {}

    # 处理器信息
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

    # 存储容量
    storage_patterns = [
        r'(\d+)\s*(?:GB|TB)\s*(?:SSD|HDD|storage|memory)',
        r'(\d+)\s*GB\s*(?:ROM|Storage)',
    ]
    for pattern in storage_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['storage'] = matches[0]
            break

    # 内存
    ram_patterns = [
        r'(\d+)\s*GB\s*(?:RAM|memory)',
        r'(\d+)GB\s+LPDDR\d+',
    ]
    for pattern in ram_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['ram'] = matches[0]
            break

    # 屏幕参数
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

    # 电池容量
    battery_patterns = [
        r'(\d+)\s*mAh',
        r'(\d+)\s*Wh',
    ]
    for pattern in battery_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['battery_capacity'] = matches[0]
            break

    # 续航时间
    battery_life_patterns = [
        r'(?:up\s*to\s*)?(\d+)\s*hours?\s*(?:battery|life)',
        r'(\d+)\s*h\s*battery',
    ]
    for pattern in battery_life_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['battery_life_claimed'] = f"{matches[0]} hours"
            break

    # 防护等级
    ip_patterns = [
        r'IP(\d+)',
    ]
    for pattern in ip_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['ip_rating'] = f"IP{matches[0]}"
            break

    # WiFi版本
    wifi_patterns = [
        r'Wi-Fi\s*(\d+)',
        r'WiFi\s*(\d+)',
    ]
    for pattern in wifi_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['wifi_version'] = f"Wi-Fi {matches[0]}"
            break

    # 蓝牙版本
    bluetooth_patterns = [
        r'Bluetooth\s*(\d+\.\d+)',
        r'BT\s*(\d+\.\d+)',
    ]
    for pattern in bluetooth_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['bluetooth_version'] = f"Bluetooth {matches[0]}"
            break

    # 传感器列表
    sensor_keywords = ['accelerometer', 'gyroscope', 'heart rate', 'blood oxygen',
                      'temperature', 'humidity', 'GPS', 'proximity', 'ambient light']
    sensors = []
    for keyword in sensor_keywords:
        if keyword.lower() in text_content.lower():
            sensors.append(keyword)
    if sensors:
        specs['sensors'] = sensors

    # 重量
    weight_patterns = [
        r'(\d+\.?\d*)\s*(?:g|kg|grams?|kilograms?)',
    ]
    for pattern in weight_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            specs['weight'] = matches[0]
            break

    # 尺寸
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
    提取市场数据

    参数:
        soup: BeautifulSoup对象
        url: 原始URL

    返回:
        市场数据字典
    """
    market_data = {}

    # 用户评价数量
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

    # 平均评分
    rating_patterns = [
        r'(\d\.?\d*)\s* out of \d+',
        r'(\d\.?\d*)\s*/\s*\d+',
    ]
    for pattern in rating_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            market_data['average_rating'] = matches[0]
            break

    # 上市日期（从URL或内容中推断）
    date_patterns = [
        r'(\d{4})',
        r'(?:released|launched)\s*(?:in\s*)?(\d{4})',
    ]
    for pattern in date_patterns:
        matches = re.findall(pattern, text_content, re.IGNORECASE)
        if matches:
            # 取最大的年份（最近的产品）
            years = [int(m) if isinstance(m, str) else m for m in matches]
            max_year = max([y for y in years if 2000 <= y <= 2030])
            market_data['release_year'] = max_year
            break

    return market_data


def extract_reliability_data(text_content: str) -> dict:
    """
    提取可靠性数据

    参数:
        text_content: 文本内容

    返回:
        可靠性数据字典
    """
    reliability = {}

    # 质保期
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

    # 防护等级（已在上一步提取，这里只标记）
    #防水等级等

    return reliability


def extract_sustainability_data(text_content: str) -> dict:
    """
    提取可持续性数据

    参数:
        text_content: 文本内容

    返回:
        可持续性数据字典
    """
    sustainability = {}

    # 材料关键词
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

    # 能耗相关
    energy_keywords = ['energy star', 'energy efficient', 'low power', 'energy saving']
    for keyword in energy_keywords:
        if keyword.lower() in text_content.lower():
            sustainability['energy_efficient'] = True
            break

    # 维修性
    repair_keywords = ['repairable', 'replaceable battery', 'modular', 'user-replaceable']
    for keyword in repair_keywords:
        if keyword.lower() in text_content.lower():
            sustainability['repairable'] = True
            break

    return sustainability


def extract_product_info(url: str, content: str) -> dict:
    """
    从网页内容中提取产品信息（增强版）

    参数:
        url: 原始URL
        content: 网页内容

    返回:
        结构化的产品信息字典（包含完整客观数据）
    """
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(content, 'html.parser')

    # 提取标题
    title = ""
    if soup.title:
        title = soup.title.string.strip()
    elif soup.h1:
        title = soup.h1.get_text().strip()

    # 提取meta描述
    description = ""
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc:
        description = meta_desc.get('content', '')

    # 提取主要内容段落
    main_content = ""
    paragraphs = soup.find_all('p')
    if paragraphs:
        main_content = "\n\n".join([p.get_text().strip() for p in paragraphs[:10] if p.get_text().strip()])

    # 提取价格
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

    # 提取特性列表
    features = []
    feature_lists = soup.find_all(['ul', 'ol'])
    for ul in feature_lists:
        items = [li.get_text().strip() for li in ul.find_all('li') if li.get_text().strip()]
        if items:
            features.extend(items)

    features = features[:20] if len(features) > 20 else features

    # 提取域名
    domain = urlparse(url).netloc

    # 🆕 提取客观数据
    text_content_lower = text_content.lower()

    # 技术规格
    objective_specs = extract_objective_specs(text_content)

    # 市场数据
    market_data = extract_market_data(soup, url)

    # 可靠性数据
    reliability_data = extract_reliability_data(text_content)

    # 可持续性数据
    sustainability_data = extract_sustainability_data(text_content)

    # 成本相关
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

        # 🆕 客观数据汇总
        "objective_data": {
            "technical_specs": objective_specs,
            "market_data": market_data,
            "reliability_data": reliability_data,
            "sustainability_data": sustainability_data,
            "cost_data": cost_data
        },

        # 数据完整性标记
        "data_completeness": {
            "technical_specs_score": len(objective_specs) / 10,  # 假设10个关键规格
            "market_data_score": len(market_data) / 4,  # 假设4个关键市场数据
            "reliability_data_score": len(reliability_data) / 3,
            "sustainability_data_score": len(sustainability_data) / 3,
            "overall_score": 0  # 将在下面计算
        }
    }


def main():
    parser = argparse.ArgumentParser(description='爬取产品页面信息（增强版）')
    parser.add_argument('--url', required=True, help='产品页面URL')
    parser.add_argument('--output', '-o', help='输出文件路径（JSON格式）')
    parser.add_argument('--pretty', action='store_true', help='美化JSON输出')

    args = parser.parse_args()

    # 爬取网页内容
    print(f"正在爬取: {args.url}", file=sys.stderr)
    result = crawl_webpage(args.url)

    if result["status"] == "error":
        print(f"错误: {result['error']}", file=sys.stderr)
        sys.exit(1)

    # 提取产品信息
    print("正在解析产品信息...", file=sys.stderr)
    product_info = extract_product_info(args.url, result["content"])

    # 计算整体数据完整性分数
    completeness = product_info["data_completeness"]
    completeness["overall_score"] = (
        completeness["technical_specs_score"] * 0.4 +
        completeness["market_data_score"] * 0.2 +
        completeness["reliability_data_score"] * 0.2 +
        completeness["sustainability_data_score"] * 0.2
    )

    # 输出结果
    if args.pretty:
        print(json.dumps(product_info, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(product_info, ensure_ascii=False))

    # 保存到文件（可选）
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.pretty:
                json.dump(product_info, f, ensure_ascii=False, indent=2)
            else:
                json.dump(product_info, f, ensure_ascii=False)
        print(f"\n结果已保存到: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
