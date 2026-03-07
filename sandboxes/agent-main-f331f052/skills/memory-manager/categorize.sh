#!/bin/bash
# Categorize memories manually

MEMORY_DIR="$HOME/.openclaw/skills/memory-manager/memory"
type="$1"
content="$2"

if [ -z "$type" ] || [ -z "$content" ]; then
  echo "Usage: $0 <episodic|semantic|procedural> \"content\""
  exit 1
fi

mkdir -p "$MEMORY_DIR/$type"

case "$type" in
  episodic)
    filename="episodic/$(date +%Y-%m-%d).md"
    ;;
  semantic)
    filename="semantic/$(date +%Y%m%d_%H%M%S).md"
    ;;
  procedural)
    filename="procedural/$(date +%Y%m%d_%H%M%S).md"
    ;;
  *)
    echo "Invalid type: $type"
    exit 1
    ;;
esac

echo "$content" >> "$MEMORY_DIR/$filename"
echo "✅ Saved to $filename"
