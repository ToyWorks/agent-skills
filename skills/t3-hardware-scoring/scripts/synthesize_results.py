#!/usr/bin/env python3
"""
T3 audit result synthesis script
Formats three Auditor evaluation reports and computes final classification
"""

import argparse
import json
import sys
from typing import Dict, List, Any


def synthesize_results(auditor_reports: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesize three Auditor evaluation reports and compute final classification.

    Args:
        auditor_reports: Dict containing three Auditor reports:
            {"tool": {...}, "toy": {...}, "trash": {...}}

    Returns:
        Complete audit result including final classification and confidence
    """
    # Extract total scores from three Auditors
    tool_score = auditor_reports.get('tool', {}).get('total_score', 50)
    toy_score = auditor_reports.get('toy', {}).get('total_score', 50)
    trash_score = auditor_reports.get('trash', {}).get('total_score', 50)
    
    # Extract dimension scores
    tool_dimensions = auditor_reports.get('tool', {}).get('dimension_scores', {})
    toy_dimensions = auditor_reports.get('toy', {}).get('dimension_scores', {})
    trash_dimensions = auditor_reports.get('trash', {}).get('dimension_scores', {})
    
    # Final Judge logic
    judgment = determine_final_classification(tool_score, toy_score, trash_score)
    
    # Assemble full result
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
    Determine final classification from three Auditor scores.

    Logic (per T3 classification guide):
    1. Composite = max(Tool, Toy) - Trash
    2. Determine dominant category (≥2 conditions met)
    3. Determine secondary category (if any)
    4. Apply Litmus Test consistency analysis

    Args:
        tool_score: Tool total (0-100, positive)
        toy_score: Toy total (0-100, positive)
        trash_score: Trash total (0-100, positive scale)

    Returns:
        Dict with classification result and confidence
    """
    # Compute composite score
    composite_score = max(tool_score, toy_score) - trash_score
    
    # Determine dominant category
    # Tool dominant: score ≥70 and significantly higher than others
    tool_dominant = 0
    if tool_score >= 70: tool_dominant += 1
    if tool_score > toy_score + 15: tool_dominant += 1
    if tool_score > trash_score + 30: tool_dominant += 1
    
    # Toy dominant: score ≥70 and significantly higher than others
    toy_dominant = 0
    if toy_score >= 70: toy_dominant += 1
    if toy_score > tool_score + 15: toy_dominant += 1
    if toy_score > trash_score + 30: toy_dominant += 1
    
    # Trash dominant: score ≥70 (positive scale) and significantly higher than others
    trash_dominant = 0
    if trash_score >= 70: trash_dominant += 1
    if trash_score > tool_score + 15: trash_dominant += 1
    if trash_score > toy_score + 15: trash_dominant += 1
    
    # Determine dominant category (≥2 conditions met)
    dominant_categories = []
    if tool_dominant >= 2:
        dominant_categories.append(('Tool', tool_score, tool_dominant))
    if toy_dominant >= 2:
        dominant_categories.append(('Toy', toy_score, toy_dominant))
    if trash_dominant >= 2:
        dominant_categories.append(('Trash', trash_score, trash_dominant))
    
    # If no clear dominant, judge by composite score
    if len(dominant_categories) == 0:
        if composite_score > 15:
            dominant_category = 'Tool' if tool_score > toy_score else 'Toy'
        elif composite_score < -15:
            dominant_category = 'Trash'
        else:
            dominant_category = 'Mixed'
    else:
        # Pick category with most conditions; if tie, highest score (Tool/Toy) or lowest (Trash)
        dominant_categories.sort(key=lambda x: (-x[2], x[1] if x[0] != 'Trash' else 100-x[1]))
        dominant_category = dominant_categories[0][0]
    
    # Determine secondary categories
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
    
    # Build final classification label
    if secondary_categories:
        final_label = f"{dominant_category} + {' + '.join(secondary_categories)}"
    else:
        final_label = dominant_category
    
    # Compute confidence
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
    
    # Build reasoning
    reasoning = {
        'primary_reason': '',
        'secondary_reason': '',
        'composite_interpretation': f"Composite {composite_score:.1f}; {'Tool/Toy-leaning' if composite_score > 0 else 'Trash-leaning' if composite_score < 0 else 'Mixed'}",
        'litmus_test_consistency': 'Litmus Test results need verification'
    }
    
    if dominant_category == 'Tool':
        reasoning['primary_reason'] = f"Tool score highest ({tool_score}), {'significantly ' if tool_score - toy_score > 20 else ''}above Toy ({toy_score})"
        if 'Toy' in secondary_categories:
            reasoning['secondary_reason'] = f"Toy score high ({toy_score}); product has Toy attributes"
    elif dominant_category == 'Toy':
        reasoning['primary_reason'] = f"Toy score highest ({toy_score}), {'significantly ' if toy_score - tool_score > 20 else ''}above Tool ({tool_score})"
        if 'Tool' in secondary_categories:
            reasoning['secondary_reason'] = f"Tool score high ({tool_score}); product has Tool attributes"
    else:  # Trash
        reasoning['primary_reason'] = f"Trash score high ({trash_score}); design violations or problems indicated"
    
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
    Generate audit result summary.

    Args:
        judgment: Final Judge result
        tool_score: Tool score
        toy_score: Toy score
        trash_score: Trash score

    Returns:
        Summary text
    """
    classification = judgment['classification']
    dominant_category = judgment['dominant_category']
    confidence = judgment['confidence']
    composite_score = judgment['composite_score']
    
    # Determine main characteristics
    if dominant_category == 'Trash':
        summary = f"Product classified as Trash (confidence {confidence}%). Trash score {trash_score}/100 indicates design violations or problems. {judgment['reasoning']['primary_reason']}"
    elif dominant_category == 'Tool':
        if 'Toy' in judgment.get('secondary_categories', []):
            summary = f"Product classified as Tool + Toy (confidence {confidence}%). Primarily a tool ({tool_score}/100) with Toy attributes ({toy_score}/100). {judgment['reasoning']['primary_reason']} {judgment['reasoning']['secondary_reason']}"
        else:
            summary = f"Product classified as Tool (confidence {confidence}%). Main value in solving real pain points; Tool score {tool_score}/100. {judgment['reasoning']['primary_reason']} If it broke tomorrow, the user's workflow would be noticeably affected."
    elif dominant_category == 'Toy':
        if 'Tool' in judgment.get('secondary_categories', []):
            summary = f"Product classified as Toy + Tool (confidence {confidence}%). Primarily a toy ({toy_score}/100) with Tool attributes ({tool_score}/100). {judgment['reasoning']['primary_reason']} {judgment['reasoning']['secondary_reason']}"
        else:
            summary = f"Product classified as Toy (confidence {confidence}%). Main value in emotional satisfaction; Toy score {toy_score}/100. {judgment['reasoning']['primary_reason']} Users primarily use it for enjoyment."
    else:  # Mixed
        summary = f"Product classified as Mixed (confidence {confidence}%). Tool {tool_score}/100, Toy {toy_score}/100, Trash {trash_score}/100. Composite {composite_score:.1f}; traits balanced, no clear leaning. Judgment depends on user needs."
    
    return summary


def format_auditor_report(auditor: str, report: Dict[str, Any]) -> str:
    """
    Format a single Auditor report as readable text.

    Args:
        auditor: Auditor name (Tool/Toy/Trash)
        report: Auditor report

    Returns:
        Formatted report text
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
        reason = dim_info.get('reason', 'No reason')
        lines.append(f"\n  {dim_name.replace('_', ' ').title()}: {score}/100 (weight {weight*100}%)")
        lines.append(f"    Reason: {reason}")
    
    # Add cross-category evidence
    cross_evidence = report.get('cross_category_evidence', {})
    if cross_evidence:
        lines.append(f"\n  Cross-category evidence:")
        for category, evidence_list in cross_evidence.items():
            if evidence_list:
                lines.append(f"    Supports {category}: {', '.join(evidence_list[:2])}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Synthesize T3 evaluation results from three Auditors')
    parser.add_argument('--input', '-i', required=True, help='Path to three Auditor reports JSON')
    parser.add_argument('--output', '-o', help='Output file path (JSON)')
    parser.add_argument('--pretty', action='store_true', help='Pretty-print JSON output')
    parser.add_argument('--format-text', action='store_true', help='Output readable text format')
    
    args = parser.parse_args()
    
    # Read Auditor reports
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            auditor_reports = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Validate report format
    required_auditors = ['tool', 'toy', 'trash']
    for auditor in required_auditors:
        if auditor not in auditor_reports:
            print(f"Error: Missing {auditor.upper()} Auditor report", file=sys.stderr)
            sys.exit(1)
    
    # Synthesize results
    print("Synthesizing three Auditor results...", file=sys.stderr)
    result = synthesize_results(auditor_reports)
    
    # Output result
    if args.format_text:
        # Output readable text format
        print("=" * 60)
        print("T3 Hardware Audit Report")
        print("=" * 60)

        judgment = result['final_judgment']
        print(f"\nFinal classification: {judgment['classification']}")
        print(f"Confidence: {judgment['confidence']}% ({judgment['confidence_level']})")
        print(f"Reasoning: {judgment['reasoning']['primary_reason']}")

        print("\n" + "=" * 60)
        print("Three Auditor Score Comparison")
        print("=" * 60)
        scores = result['score_comparison']
        print(f"🟢 Tool:   {scores['tool']}/100")
        print(f"🟡 Toy:    {scores['toy']}/100")
        print(f"🔴 Trash:  {scores['trash']}/100")
        
        print("\n" + "=" * 60)
        print("Auditor Detailed Reports")
        print("=" * 60)
        for auditor in ['tool', 'toy', 'trash']:
            auditor_name = auditor.capitalize()
            report = auditor_reports[auditor]
            print(format_auditor_report(auditor_name, report))
        
        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print(result['summary'])
        
    else:
        # Output JSON format
        if args.pretty:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False))
    
    # Save to file (optional)
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.pretty:
                json.dump(result, f, ensure_ascii=False, indent=2)
            else:
                json.dump(result, f, ensure_ascii=False)
        print(f"\nResult saved to: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
