#!/usr/bin/env python3
"""
T3 Audit Result Synthesis Script — v2.0
Implements correct normalization, Eagle Eye Veto, and Litmus Gate logic
per t3-classification.md specification.
"""

import argparse
import json
import sys
from typing import Dict, List, Any, Optional


# ─── Constants ───────────────────────────────────────────────────────────────

TOOL_MAX = 33
TOY_MAX  = 33
TRASH_MAX = 42


# ─── Normalization ────────────────────────────────────────────────────────────

def normalize(raw: float, max_raw: float) -> float:
    """Normalize raw score to 0-100 scale."""
    if max_raw == 0:
        return 0.0
    return round((raw / max_raw) * 100, 1)


# ─── Classification ───────────────────────────────────────────────────────────

def check_primary_conditions(norm_tool: float, norm_toy: float, norm_trash: float,
                              litmus_tool: bool, litmus_toy: bool, litmus_trash: bool) -> Dict[str, int]:
    """
    Count how many primary-classification conditions each category meets.
    Per t3-classification.md: need 2+ conditions to become Primary.
    """
    tool_count = 0
    if norm_tool >= 75:         tool_count += 1
    if norm_tool > norm_toy  + 20: tool_count += 1
    if norm_tool > norm_trash + 20: tool_count += 1
    if litmus_tool:             tool_count += 1

    toy_count = 0
    if norm_toy >= 75:          toy_count += 1
    if norm_toy > norm_tool  + 20: toy_count += 1
    if norm_toy > norm_trash + 20: toy_count += 1
    if litmus_toy:              toy_count += 1

    trash_count = 0
    if norm_trash >= 60:        trash_count += 1  # lower threshold per spec
    if norm_trash > norm_tool + 20: trash_count += 1
    if norm_trash > norm_toy  + 20: trash_count += 1
    if litmus_trash:            trash_count += 1

    return {"tool": tool_count, "toy": toy_count, "trash": trash_count}


def determine_secondary(primary: str, norm_tool: float, norm_toy: float, norm_trash: float) -> List[str]:
    """Determine secondary classification per t3-classification.md rules."""
    secondary = []
    if primary == "Tool":
        if norm_toy   >= 60: secondary.append("Toy")
        if norm_trash >= 50: secondary.append("Trash")
    elif primary == "Toy":
        if norm_tool  >= 60: secondary.append("Tool")
        if norm_trash >= 50: secondary.append("Trash")
    elif primary == "Trash":
        if norm_tool  >= 50: secondary.append("Tool")
        if norm_toy   >= 50: secondary.append("Toy")
    return secondary


def classify(norm_tool: float, norm_toy: float, norm_trash: float,
             litmus_tool: bool, litmus_toy: bool, litmus_trash: bool,
             eagle_eye_triggers: List[str]) -> Dict[str, Any]:
    """
    Full classification logic per t3-classification.md.
    Eagle Eye Veto forces Trash into label when critical issues are flagged.
    """
    composite = max(norm_tool, norm_toy) - norm_trash
    counts = check_primary_conditions(norm_tool, norm_toy, norm_trash,
                                      litmus_tool, litmus_toy, litmus_trash)

    # ── Determine Primary ──────────────────────────────────────────────────
    primary = None
    if counts["tool"] >= 2 or counts["toy"] >= 2 or counts["trash"] >= 2:
        # Pick the category with the most conditions; break ties by normalized score
        order = sorted(
            [("Tool", counts["tool"], norm_tool),
             ("Toy",  counts["toy"],  norm_toy),
             ("Trash",counts["trash"],norm_trash if counts["trash"] >= 2 else -1)],
            key=lambda x: (-x[1], -x[2])
        )
        if order[0][1] >= 2:
            primary = order[0][0]

    if primary is None:
        # Gray Zone: fall back to composite score
        if composite > 0:
            primary = "Tool" if norm_tool >= norm_toy else "Toy"
        elif composite < 0:
            primary = "Trash"
        else:
            primary = "Tool" if norm_tool >= norm_toy else "Toy"

    # ── Secondary ──────────────────────────────────────────────────────────
    secondary = determine_secondary(primary, norm_tool, norm_toy, norm_trash)

    # ── Eagle Eye Veto ─────────────────────────────────────────────────────
    eagle_eye_activated = len(eagle_eye_triggers) > 0
    if eagle_eye_activated:
        # Trash MUST appear somewhere in the label
        if primary != "Trash" and "Trash" not in secondary:
            secondary.append("Trash")

    # ── Confidence ────────────────────────────────────────────────────────
    gray_zone = (counts["tool"] < 2 and counts["toy"] < 2 and counts["trash"] < 2)
    if eagle_eye_activated:
        confidence = "Review Required"
    elif gray_zone:
        confidence = "Low"
    elif max(counts.values()) >= 3:
        confidence = "High"
    else:
        confidence = "Medium"

    # ── Build label ───────────────────────────────────────────────────────
    parts = [primary] + secondary
    label_suffix = " (Eagle Eye)" if eagle_eye_activated else (" (Gray Zone)" if gray_zone else "")
    final_label = " + ".join(parts) + label_suffix

    return {
        "primary": primary,
        "secondary": secondary,
        "final_label": final_label,
        "eagle_eye_veto_activated": eagle_eye_activated,
        "eagle_eye_triggers": eagle_eye_triggers,
        "confidence": confidence,
        "composite_score": round(composite, 1),
        "condition_counts": counts,
        "gray_zone": gray_zone,
    }


# ─── Synthesis ────────────────────────────────────────────────────────────────

def synthesize_results(auditor_reports: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesize three Auditor reports into a final T3 audit result.

    Expected input keys: "tool", "toy", "trash"
    Each report must have: total_score (raw int), litmus_gate (str "Yes"/"No")
    Trash report additionally needs: critical_issues (list[str])
    """

    # ── Extract raw scores ─────────────────────────────────────────────────
    tool_raw  = auditor_reports.get("tool",  {}).get("total_score", 0)
    toy_raw   = auditor_reports.get("toy",   {}).get("total_score", 0)
    trash_raw = auditor_reports.get("trash", {}).get("total_score", 0)

    # ── Normalize ──────────────────────────────────────────────────────────
    norm_tool  = normalize(tool_raw,  TOOL_MAX)
    norm_toy   = normalize(toy_raw,   TOY_MAX)
    norm_trash = normalize(trash_raw, TRASH_MAX)

    # ── Litmus gates (boolean) ────────────────────────────────────────────
    def parse_litmus(val: Any) -> bool:
        if isinstance(val, bool):
            return val
        return str(val).strip().lower().startswith("yes")

    litmus_tool  = parse_litmus(auditor_reports.get("tool",  {}).get("litmus_gate", "No"))
    litmus_toy   = parse_litmus(auditor_reports.get("toy",   {}).get("litmus_gate", "No"))
    litmus_trash = parse_litmus(auditor_reports.get("trash", {}).get("litmus_gate", "No"))

    # ── Eagle Eye triggers ────────────────────────────────────────────────
    eagle_eye_triggers = auditor_reports.get("trash", {}).get("critical_issues", [])
    # Accept both top-level and nested formats
    if not eagle_eye_triggers:
        extract = auditor_reports.get("trash", {}).get("extract_for_report", {})
        eagle_eye_triggers = extract.get("critical_issues", [])

    # ── Classify ──────────────────────────────────────────────────────────
    classification = classify(
        norm_tool, norm_toy, norm_trash,
        litmus_tool, litmus_toy, litmus_trash,
        eagle_eye_triggers,
    )

    # ── Score table ───────────────────────────────────────────────────────
    scores = {
        "tool_raw": tool_raw,   "tool_max": TOOL_MAX,   "tool_normalized": norm_tool,
        "toy_raw":  toy_raw,    "toy_max":  TOY_MAX,    "toy_normalized":  norm_toy,
        "trash_raw":trash_raw,  "trash_max":TRASH_MAX,  "trash_normalized":norm_trash,
        "composite": classification["composite_score"],
    }

    # ── Final verdict summary ─────────────────────────────────────────────
    verdict = _build_verdict(classification, scores, auditor_reports)

    return {
        "scores": scores,
        "litmus_gates": {
            "tool":  "Yes" if litmus_tool  else "No",
            "toy":   "Yes" if litmus_toy   else "No",
            "trash": "Yes" if litmus_trash else "No",
        },
        "classification": classification,
        "final_verdict_summary": verdict,
        "auditor_reports": auditor_reports,
    }


def _build_verdict(classification: Dict, scores: Dict, reports: Dict) -> str:
    primary = classification["primary"]
    label   = classification["final_label"]
    comp    = scores["composite"]
    eagle   = classification["eagle_eye_activated"] if "eagle_eye_activated" in classification else classification.get("eagle_eye_veto_activated", False)

    tool_report  = reports.get("tool",  {})
    toy_report   = reports.get("toy",   {})
    trash_report = reports.get("trash", {})

    tool_str  = tool_report.get("extract_for_report",  {}).get("litmus_test_reason", "")
    toy_str   = toy_report.get("extract_for_report",   {}).get("litmus_test_reason", "")
    trash_str = trash_report.get("extract_for_report", {}).get("litmus_test_reason", "")

    verdict = f"Classification: {label}. Composite score {comp:+.1f}. "

    if primary == "Tool":
        verdict += f"Product delivers quantifiable utility (Tool normalized {scores['tool_normalized']:.0f}/100). "
        if tool_str: verdict += f"{tool_str}. "
    elif primary == "Toy":
        verdict += f"Product delivers emotional/aesthetic value (Toy normalized {scores['toy_normalized']:.0f}/100). "
        if toy_str: verdict += f"{toy_str}. "
    else:
        verdict += f"Product creates more problems than it solves (Trash normalized {scores['trash_normalized']:.0f}/100). "

    if eagle:
        issues = classification.get("eagle_eye_triggers", [])
        verdict += f"⚠️ Eagle Eye Veto activated — critical issues: {'; '.join(issues[:2])}."

    return verdict.strip()


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Synthesize T3 audit results from three Auditor reports (v2.0)"
    )
    parser.add_argument("--input", "-i", required=True,
                        help="Path to JSON file containing tool/toy/trash auditor reports")
    parser.add_argument("--output", "-o", help="Output file path (JSON)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--text",   action="store_true", help="Human-readable text summary")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            auditor_reports = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {args.input}", file=sys.stderr); sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr); sys.exit(1)

    for key in ("tool", "toy", "trash"):
        if key not in auditor_reports:
            print(f"Error: missing '{key}' auditor report", file=sys.stderr); sys.exit(1)

    result = synthesize_results(auditor_reports)

    if args.text:
        s = result["scores"]
        c = result["classification"]
        print("=" * 60)
        print("T3 AUDIT SYNTHESIS  —  v2.0")
        print("=" * 60)
        print(f"\n🟢 Tool  : {s['tool_raw']:>2}/{s['tool_max']}  →  {s['tool_normalized']:.1f}/100")
        print(f"🟡 Toy   : {s['toy_raw']:>2}/{s['toy_max']}  →  {s['toy_normalized']:.1f}/100")
        print(f"🔴 Trash : {s['trash_raw']:>2}/{s['trash_max']} →  {s['trash_normalized']:.1f}/100")
        print(f"\nComposite : {s['composite']:+.1f}")
        print(f"Litmus    : Tool={result['litmus_gates']['tool']}  "
              f"Toy={result['litmus_gates']['toy']}  Trash={result['litmus_gates']['trash']}")
        print(f"\n{'─'*60}")
        print(f"Classification : {c['final_label']}")
        print(f"Confidence     : {c['confidence']}")
        if c['eagle_eye_veto_activated']:
            print(f"\n🚨 Eagle Eye Veto ACTIVE:")
            for t in c['eagle_eye_triggers']:
                print(f"   • {t}")
        print(f"\n{result['final_verdict_summary']}")
    else:
        indent = 2 if args.pretty else None
        out = json.dumps(result, ensure_ascii=False, indent=indent)
        print(out)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nSaved to: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
