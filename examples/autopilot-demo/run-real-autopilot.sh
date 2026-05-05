#!/usr/bin/env bash
# Run autopilot end-to-end against the real Anthropic API.
#
# Usage:
#   export ANTHROPIC_API_KEY=sk-ant-...
#   ./run-real-autopilot.sh "Build a Python TODO list CLI with tests"
#
# Or pass --offline to fall back to the deterministic stub (no key needed).

set -euo pipefail

PROMPT="${1:-Build a Python add(a,b) function with one bare test_add()}"
PROVIDER="anthropic"
PROJECT_DIR="${PROJECT_DIR:-./build}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

if [[ "${PROMPT}" == "--offline" || -z "${ANTHROPIC_API_KEY:-}" ]]; then
  PROVIDER="stub"
  if [[ "${PROMPT}" == "--offline" ]]; then
    PROMPT="${2:-Build a Python add(a,b) function with one bare test_add()}"
  else
    echo "[demo] ANTHROPIC_API_KEY not set; falling back to stub provider." >&2
  fi
fi

mkdir -p "${PROJECT_DIR}"
echo "[demo] provider=${PROVIDER} project=${PROJECT_DIR}" >&2
echo "[demo] prompt=${PROMPT}" >&2

"${ROOT}/bin/super-skill" autopilot \
  --provider "${PROVIDER}" \
  --project "${PROJECT_DIR}" \
  --prompt "${PROMPT}" \
  --max-ralph-rounds 10

# Print a one-liner summary that points the user to artifacts.
RUN_DIR="$(ls -td "${PROJECT_DIR}/.super-skill/autopilot/"*/ | head -1)"
echo
echo "[demo] artifacts:"
ls -1 "${RUN_DIR}" | sed 's/^/  - /'
echo
echo "[demo] inspect run journal:"
echo "  cat \"${RUN_DIR}run.json\""
