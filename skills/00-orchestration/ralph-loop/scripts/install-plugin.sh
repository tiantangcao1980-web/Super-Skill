#!/usr/bin/env bash
# Install / uninstall the embedded ralph-loop plugin into ~/.claude/plugins/.
#
# This is a *separate* mechanism from `code-skills install` (which only
# installs the Markdown skill). The plugin includes a Stop hook + slash
# commands that actually run the Ralph loop in a Claude Code session.
#
# Usage:
#   ralph-loop/scripts/install-plugin.sh install [--symlink|--copy]
#   ralph-loop/scripts/install-plugin.sh uninstall
#   ralph-loop/scripts/install-plugin.sh status
#
# The plugin sits at:
#   ~/.claude/plugins/code-skills/ralph-loop/
# (separate namespace from the official "claude-plugins-official" marketplace
# so we never overwrite the user's existing official install.)

set -euo pipefail

PLUGIN_NAMESPACE="code-skills"
PLUGIN_NAME="ralph-loop"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/plugin"
DST_BASE="$HOME/.claude/plugins/$PLUGIN_NAMESPACE"
DST="$DST_BASE/$PLUGIN_NAME"

cmd="${1:-status}"
mode="${2:---symlink}"

ensure_src() {
  if [[ ! -f "$SRC/.claude-plugin/plugin.json" ]]; then
    echo "error: plugin source missing at $SRC" >&2
    exit 1
  fi
}

case "$cmd" in
  install)
    ensure_src
    mkdir -p "$DST_BASE"
    if [[ -e "$DST" || -L "$DST" ]]; then
      echo "info: plugin already installed at $DST"
      echo "      run 'uninstall' first to replace it"
      exit 0
    fi
    if [[ "$mode" == "--copy" ]]; then
      cp -R "$SRC" "$DST"
      echo "[OK] copied to $DST"
    else
      ln -s "$SRC" "$DST"
      echo "[OK] symlinked to $DST"
    fi
    echo ""
    echo "next steps:"
    echo "  1. open a NEW Claude Code session in any project"
    echo "  2. run /ralph-loop \"your task\" --completion-promise 'DONE' --max-iterations 20"
    echo "  3. inspect state with: head -10 .claude/ralph-loop.local.md"
    ;;
  uninstall)
    if [[ ! -e "$DST" && ! -L "$DST" ]]; then
      echo "info: not installed at $DST"
      exit 0
    fi
    if [[ -L "$DST" ]]; then
      rm "$DST"
      echo "[OK] symlink removed: $DST"
    else
      rm -rf "$DST"
      echo "[OK] directory removed: $DST"
    fi
    ;;
  status)
    if [[ -L "$DST" ]]; then
      target="$(readlink "$DST")"
      echo "installed (symlink) -> $target"
    elif [[ -d "$DST" ]]; then
      echo "installed (copy) at $DST"
    else
      echo "not installed"
    fi
    if command -v jq >/dev/null 2>&1; then :; else
      echo "warn: 'jq' not found; the Stop hook needs it. install: brew install jq"
    fi
    ;;
  *)
    echo "usage: $0 {install [--symlink|--copy] | uninstall | status}" >&2
    exit 2
    ;;
esac
