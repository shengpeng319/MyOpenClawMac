#!/bin/bash
# Initialize memory structure

MEMORY_DIR="$HOME/.openclaw/skills/memory-manager/memory"

mkdir -p "$MEMORY_DIR"/{episodic,semantic,procedural,snapshots}
mkdir -p "$MEMORY_DIR"/legacy

echo "✅ Memory structure initialized at $MEMORY_DIR"
echo ""
echo "Created directories:"
echo "  - episodic/    # Daily event logs"
echo "  - semantic/    # Knowledge base"
echo "  - procedural/  # How-to guides"
echo "  - snapshots/   # Compression backups"
echo "  - legacy/      # Migrated files"
