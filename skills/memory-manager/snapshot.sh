#!/bin/bash
# Save memory snapshot before compression

MEMORY_DIR="$HOME/.openclaw/skills/memory-manager/memory"
SNAPSHOT_DIR="$MEMORY_DIR/snapshots"
timestamp=$(date +%Y%m%d_%H%M%S)

mkdir -p "$SNAPSHOT_DIR"

# Create compressed snapshot
tar -czf "$SNAPSHOT_DIR/snapshot_${timestamp}.tar.gz" -C "$MEMORY_DIR" episodic semantic procedural 2>/dev/null

if [ -f "$SNAPSHOT_DIR/snapshot_${timestamp}.tar.gz" ]; then
  echo "✅ Snapshot saved: $SNAPSHOT_DIR/snapshot_${timestamp}.tar.gz"
  ls -lh "$SNAPSHOT_DIR/" | tail -5
else
  echo "❌ Failed to create snapshot"
fi
