#!/bin/bash
# Search memories by type

MEMORY_DIR="$HOME/.openclaw/skills/memory-manager/memory"
type="${1:-all}"
query="${2:-}"

if [ -z "$query" ]; then
  echo "Usage: $0 <type> <query>"
  echo "  Types: episodic, semantic, procedural, all"
  exit 1
fi

case "$type" in
  episodic)
    echo "🔍 Searching episodic memory for: $query"
    find "$MEMORY_DIR/episodic" -name "*.md" -exec grep -l "$query" {} \; 2>/dev/null | head -10
    ;;
  semantic)
    echo "🔍 Searching semantic memory for: $query"
    find "$MEMORY_DIR/semantic" -name "*.md" -exec grep -l "$query" {} \; 2>/dev/null | head -10
    ;;
  procedural)
    echo "🔍 Searching procedural memory for: $query"
    find "$MEMORY_DIR/procedural" -name "*.md" -exec grep -l "$query" {} \; 2>/dev/null | head -10
    ;;
  all)
    echo "🔍 Searching all memories for: $query"
    find "$MEMORY_DIR" -name "*.md" -exec grep -l "$query" {} \; 2>/dev/null | head -20
    ;;
  *)
    echo "Unknown type: $type"
    echo "Valid types: episodic, semantic, procedural, all"
    ;;
esac
