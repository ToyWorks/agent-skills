#!/usr/bin/env python3
"""
T3审计结果综合脚本
格式化三Auditor的评估报告并计算最终分类
"""

import argparse
import json
import sys
from typing import Dict, List, Any


def synthesize_results(auditor_reports: Dict[str, Any]) -> Dict[str, Any]:
    """
    综合三Auditor的评估报告，计算最终分类
    
    参数:
        auditor_reports: 包含三个Auditor报告的字典
        格式: {
            "tool": {...},
            "toy": {...},
            "trash": {...}
        }
    
    返回:
        完整的审计结果，包含最终分类和置信度
    """
    # 提取三个Auditor的总评分
    tool_score = auditor_reports.get('tool', {}).get('total_score', 50)
    toy_score = auditor_reports.get('toy', {}).get('total_score', 50)
    trash_score = auditor_reports.get('trash', {}).get('total_score', 50)
    
    # 提取各维度得分
    tool_dimensions = auditor_reports.get('tool', {}).get('dimension_scores', {})
    toy_dimensions = auditor_reports.get('toy', {}).get('dimension_scores', {})
    trash_dimensions = auditor_reports.get('trash', {}).get('dimension_scores', {})
    
    # Final Judge判断逻辑
    judgment = determine_final_classification(tool_score, toy_score, trash_score)
    
    # 组合完整结果
    result = {
        'auditor_reports': auditor_reports,
        'final_judgment': judgment,
        'score_comparison': {
            'tool': tool_score,
            'toy': toy_score,
            'trash': trash_score
        },
        'dimension_comparison': {
            'tool': {k: v.get('score', 0) for k, v in tool_dimensions.items()},
            'toy': {k: v.get('score', 0) for k, v in toy_dimensions.items()},
            'trash': {k: v.get('score', 0) for k, v in trash_dimensions.items()}
        },
        'summary': generate_summary(judgment, tool_score, toy_score, trash_score)
    }
    
    return result


def determine_final_classification(tool_score: float, toy_score: float, trash_score: float) -> Dict[str, Any]:
    """
    基于三Auditor评分确定最终分类
    
    判断逻辑（遵循T3分类指南）：
    1. 计算综合评分：Composite = max(Tool, Toy) - Trash
    2. 确定主导分类（满足2个以上条件）
    3. 确定次要分类（如有）
    4. 应用Litmus Test一致性分析
    
    参数:
        tool_score: Tool总评分（0-100，正向）
        toy_score: Toy总评分（0-100，正向）
        trash_score: Trash总评分（0-100，反向）
    
    返回:
        包含分类结果和置信度的字典
    """
    # 计算综合评分
    composite_score = max(tool_score, toy_score) - trash_score
    
    # 确定主导分类
    # Tool为主导的条件：评分≥70，且显著高于其他分类
    tool_dominant = 0
    if tool_score >= 70: tool_dominant += 1
    if tool_score > toy_score + 15: tool_dominant += 1
    if tool_score > trash_score + 30: tool_dominant += 1
    
    # Toy为主导的条件：评分≥70，且显著高于其他分类
    toy_dominant = 0
    if toy_score >= 70: toy_dominant += 1
    if toy_score > tool_score + 15: toy_dominant += 1
    if toy_score > trash_score + 30: toy_dominant += 1
    
    # Trash为主导的条件：评分≥70（正向评分），且显著高于其他分类
    trash_dominant = 0
    if trash_score >= 70: trash_dominant += 1
    if trash_score > tool_score + 15: trash_dominant += 1
    if trash_score > toy_score + 15: trash_dominant += 1
    
    # 确定主导分类（满足2个以上条件）
    dominant_categories = []
    if tool_dominant >= 2:
        dominant_categories.append(('Tool', tool_score, tool_dominant))
    if toy_dominant >= 2:
        dominant_categories.append(('Toy', toy_score, toy_dominant))
    if trash_dominant >= 2:
        dominant_categories.append(('Trash', trash_score, trash_dominant))
    
    # 如果没有明确主导，基于综合评分判断
    if len(dominant_categories) == 0:
        if composite_score > 15:
            dominant_category = 'Tool' if tool_score > toy_score else 'Toy'
        elif composite_score < -15:
            dominant_category = 'Trash'
        else:
            dominant_category = 'Mixed'
    else:
        # 选择条件数最多的，如果相等选择评分最高的（Tool/Toy）或最低的（Trash）
        dominant_categories.sort(key=lambda x: (-x[2], x[1] if x[0] != 'Trash' else 100-x[1]))
        dominant_category = dominant_categories[0][0]
    
    # 确定次要分类
    secondary_categories = []
    if dominant_category == 'Tool':
        if toy_score >= 60 and toy_score > trash_score + 20:
            secondary_categories.append('Toy')
        if trash_score <= 40 and trash_score < toy_score - 20:
            secondary_categories.append('Trash')
    elif dominant_category == 'Toy':
        if tool_score >= 60 and tool_score > trash_score + 20:
            secondary_categories.append('Tool')
        if trash_score <= 40 and trash_score < tool_score - 20:
            secondary_categories.append('Trash')
    elif dominant_category == 'Trash':
        if tool_score >= 50:
            secondary_categories.append('Tool')
        if toy_score >= 50:
            secondary_categories.append('Toy')
    
    # 构建最终分类标签
    if secondary_categories:
        final_label = f"{dominant_category} + {' + '.join(secondary_categories)}"
    else:
        final_label = dominant_category
    
    # 计算置信度
    if dominant_category == 'Tool':
        score_diff = tool_score - max(toy_score, trash_score)
        confidence = min(50 + score_diff, 100)
    elif dominant_category == 'Toy':
        score_diff = toy_score - max(tool_score, trash_score)
        confidence = min(50 + score_diff, 100)
    else:  # Trash
        score_diff = max(tool_score, toy_score) - trash_score
        confidence = min(50 + score_diff, 100)
    
    confidence_level = 'High' if confidence > 75 else 'Medium' if confidence > 50 else 'Low'
    
    # 构建判断理由
    reasoning = {
        'primary_reason': '',
        'secondary_reason': '',
        'composite_interpretation': f"综合评分{composite_score:.1f}，{'偏向Tool/Toy' if composite_score > 0 else '偏向Trash' if composite_score < 0 else '混合分类'}",
        'litmus_test_consistency': '需要检查Litmus Test结果'
    }
    
    if dominant_category == 'Tool':
        reasoning['primary_reason'] = f"Tool评分最高（{tool_score}），{'显著' if tool_score - toy_score > 20 else ''}高于Toy评分（{toy_score}）"
        if 'Toy' in secondary_categories:
            reasoning['secondary_reason'] = f"Toy评分较高（{toy_score}），产品兼具Toy属性"
    elif dominant_category == 'Toy':
        reasoning['primary_reason'] = f"Toy评分最高（{toy_score}），{'显著' if toy_score - tool_score > 20 else ''}高于Tool评分（{tool_score}）"
        if 'Tool' in secondary_categories:
            reasoning['secondary_reason'] = f"Tool评分较高（{tool_score}），产品兼具Tool属性"
    else:  # Trash
        reasoning['primary_reason'] = f"Trash评分低（{trash_score}），显示存在设计违背或问题"
    
    return {
        'classification': final_label,
        'dominant_category': dominant_category,
        'secondary_categories': secondary_categories,
        'confidence': round(confidence, 2),
        'confidence_level': confidence_level,
        'composite_score': round(composite_score, 2),
        'scores': {
            'tool': tool_score,
            'toy': toy_score,
            'trash': trash_score
        },
        'reasoning': reasoning
    }


def generate_summary(judgment: Dict[str, Any], tool_score: float, toy_score: float, trash_score: float) -> str:
    """
    生成审计结果摘要
    
    参数:
        judgment: Final Judge的判断结果
        tool_score: Tool评分
        toy_score: Toy评分
        trash_score: Trash评分
    
    返回:
        摘要文本
    """
    classification = judgment['classification']
    dominant_category = judgment['dominant_category']
    confidence = judgment['confidence']
    composite_score = judgment['composite_score']
    
    # 判断主要特征
    if dominant_category == 'Trash':
        summary = f"产品被归类为Trash（置信度{confidence}%）。Trash评分{trash_score}/100，显示存在设计违背或问题。{judgment['reasoning']['primary_reason']}"
    elif dominant_category == 'Tool':
        if 'Toy' in judgment.get('secondary_categories', []):
            summary = f"产品被归类为Tool + Toy（置信度{confidence}%）。主要作为工具使用（{tool_score}/100），同时也具备玩具属性（{toy_score}/100）。{judgment['reasoning']['primary_reason']} {judgment['reasoning']['secondary_reason']}"
        else:
            summary = f"产品被归类为Tool（置信度{confidence}%）。主要价值在于解决实际痛点，Tool评分{tool_score}/100。{judgment['reasoning']['primary_reason']} 如果明天坏了，用户的工作流会受到明显影响。"
    elif dominant_category == 'Toy':
        if 'Tool' in judgment.get('secondary_categories', []):
            summary = f"产品被归类为Toy + Tool（置信度{confidence}%）。主要作为玩具使用（{toy_score}/100），同时也具备工具属性（{tool_score}/100）。{judgment['reasoning']['primary_reason']} {judgment['reasoning']['secondary_reason']}"
        else:
            summary = f"产品被归类为Toy（置信度{confidence}%）。主要价值在于情感价值和愉悦体验，Toy评分{toy_score}/100。{judgment['reasoning']['primary_reason']} 用户使用主要是因为带来乐趣和愉悦。"
    else:  # Mixed
        summary = f"产品被归类为混合分类（置信度{confidence}%）。Tool评分{tool_score}/100，Toy评分{toy_score}/100，Trash评分{trash_score}/100。综合评分{composite_score:.1f}，各特征均衡，无明显倾向。需要根据用户具体需求判断。"
    
    return summary


def format_auditor_report(auditor: str, report: Dict[str, Any]) -> str:
    """
    格式化单个Auditor的报告为可读文本
    
    参数:
        auditor: Auditor名称（Tool/Toy/Trash）
        report: Auditor报告
    
    返回:
        格式化的报告文本
    """
    emoji = {'Tool': '🟢', 'Toy': '🟡', 'Trash': '🔴'}.get(auditor, '')
    total_score = report.get('total_score', 0)
    dimension_scores = report.get('dimension_scores', {})
    
    lines = [
        f"\n{emoji} {auditor} Auditor: {total_score}/100",
        f"{'=' * 50}"
    ]
    
    for dim_name, dim_info in dimension_scores.items():
        score = dim_info.get('score', 0)
        weight = dim_info.get('weight', 0)
        reason = dim_info.get('reason', '无理由')
        lines.append(f"\n  {dim_name.replace('_', ' ').title()}: {score}/100 (权重{weight*100}%)")
        lines.append(f"    理由: {reason}")
    
    # 添加跨分类证据
    cross_evidence = report.get('cross_category_evidence', {})
    if cross_evidence:
        lines.append(f"\n  跨分类证据:")
        for category, evidence_list in cross_evidence.items():
            if evidence_list:
                lines.append(f"    支持{category}: {', '.join(evidence_list[:2])}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='综合三Auditor的T3评估结果')
    parser.add_argument('--input', '-i', required=True, help='三Auditor报告JSON文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径（JSON格式）')
    parser.add_argument('--pretty', action='store_true', help='美化JSON输出')
    parser.add_argument('--format-text', action='store_true', help='输出可读文本格式')
    
    args = parser.parse_args()
    
    # 读取Auditor报告
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            auditor_reports = json.load(f)
    except FileNotFoundError:
        print(f"错误: 文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"错误: JSON格式错误: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # 验证报告格式
    required_auditors = ['tool', 'toy', 'trash']
    for auditor in required_auditors:
        if auditor not in auditor_reports:
            print(f"错误: 缺少{auditor.upper()} Auditor报告", file=sys.stderr)
            sys.exit(1)
    
    # 综合结果
    print("正在综合三Auditor评估结果...", file=sys.stderr)
    result = synthesize_results(auditor_reports)
    
    # 输出结果
    if args.format_text:
        # 输出可读文本格式
        print("=" * 60)
        print("T3硬件审计报告")
        print("=" * 60)
        
        judgment = result['final_judgment']
        print(f"\n最终分类: {judgment['classification']}")
        print(f"置信度: {judgment['confidence']}% ({judgment['confidence_level']})")
        print(f"理由: {judgment['reason']}")
        
        print("\n" + "=" * 60)
        print("三Auditor评分对比")
        print("=" * 60)
        scores = result['score_comparison']
        print(f"🟢 Tool:   {scores['tool']}/100")
        print(f"🟡 Toy:    {scores['toy']}/100")
        print(f"🔴 Trash:  {scores['trash']}/100")
        
        print("\n" + "=" * 60)
        print("Auditor详细报告")
        print("=" * 60)
        for auditor in ['tool', 'toy', 'trash']:
            auditor_name = auditor.capitalize()
            report = auditor_reports[auditor]
            print(format_auditor_report(auditor_name, report))
        
        print("\n" + "=" * 60)
        print("摘要")
        print("=" * 60)
        print(result['summary'])
        
    else:
        # 输出JSON格式
        if args.pretty:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False))
    
    # 保存到文件（可选）
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.pretty:
                json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                json.dump(result, f, ensure_ascii=False)
        print(f"\n结果已保存到: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
