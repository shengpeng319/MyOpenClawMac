#!/bin/bash
# Organize memories into proper structure

MEMORY_DIR="$HOME/.openclaw/skills/memory-manager/memory"

if [ ! -d "$MEMORY_DIR" ]; then
  echo "⚠️ Memory not initialized"
  exit 1
fi

echo "📦 Organizing memories..."

# Find flat memory files
flat_files=$(find "$MEMORY_DIR" -maxdepth 1 -name "*.md" -type f 2>/dev/null)

if [ -z "$flat_files" ]; then
  echo "✅ No flat files to organize"
else
  echo "📁 Moving legacy files to $MEMORY_DIR/legacy/"
  for file in $flat_files; do
    mv "$file" "$MEMORY_DIR/legacy/" 2>/dev/null
  done
fi

# Ensure directories exist
mkdir -p "$MEMORY_DIR"/{episodic,semantic,procedural}

echo "✅ Organization complete"
echo "  Legacy files: $MEMORY_DIR/legacy/"
echo ""
echo "To search memories:"
echo "  ~/.openclaw/skills/memory-manager/search.sh all \"keyword\""
