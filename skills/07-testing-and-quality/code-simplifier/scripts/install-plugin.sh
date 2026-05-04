#!/usr/bin/env bash
# Install / uninstall the embedded code-simplifier plugin into ~/.claude/plugins/.
#
# This plugin ships an Anthropic-authored agent definition. After install, you
# can call it from Claude Code via the standard Agent tool with
# subagent_type: "code-simplifier", or use the skill directly.
#
# Usage:
#   code-simplifier/scripts/install-plugin.sh install [--symlink|--copy]
#   code-simplifier/scripts/install-plugin.sh uninstall
#   code-simplifier/scripts/install-plugin.sh status

set -euo pipefail

PLUGIN_NAMESPACE="code-skills"
PLUGIN_NAME="code-simplifier"
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
    echo "  1. restart Claude Code session"
    echo "  2. invoke via Agent tool with subagent_type=\"code-simplifier\""
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
      echo "installed (symlink) -> $(readlink "$DST")"
    elif [[ -d "$DST" ]]; then
      echo "installed (copy) at $DST"
    else
      echo "not installed"
    fi
    ;;
  *)
    echo "usage: $0 {install [--symlink|--copy] | uninstall | status}" >&2
    exit 2
    ;;
esac
