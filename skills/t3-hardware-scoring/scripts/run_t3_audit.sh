#!/usr/bin/env bash
set -euo pipefail

# Minimal runner (manual use). Keeps prompts short by using file paths.
# Usage:
#   scripts/run_t3_audit.sh "https://example.com/product" "product-slug"

URL="${1:-}"
SLUG="${2:-case}"
DATE="$(date +%F)"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OUT_DIR="./tmp/reports/t3-${DATE}-${SLUG}"

mkdir -p "$OUT_DIR"

echo "[1] Crawl"
python3 "$SKILL_DIR/scripts/crawl_product_info.py" --url "$URL" --pretty > "$OUT_DIR/01-level0-extracts.md" || true

echo "[2] Brand blinding step is manual (per SKILL.md)."
echo "Write to: $OUT_DIR/02-brand-blinded.md"

echo "[3] Run auditors via OpenClaw sessions_spawn (recommended)."
echo "Pass only file paths: $OUT_DIR/02-brand-blinded.md"

echo "[4] If needed, run Eagle Eye validator."

echo "[5] Synthesize"
# Expects auditor_reports.json (tool/toy/trash)
if [[ -f "$OUT_DIR/auditor_reports.json" ]]; then
  python3 "$SKILL_DIR/scripts/synthesize_results.py" --input "$OUT_DIR/auditor_reports.json" --output "$OUT_DIR/05-synthesis.json" --text
else
  echo "Missing $OUT_DIR/auditor_reports.json"
fi
