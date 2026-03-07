#!/bin/bash
# Show memory statistics

MEMORY_DIR="$HOME/.openclaw/skills/memory-manager/memory"

if [ ! -d "$MEMORY_DIR" ]; then
  echo "⚠️ Memory not initialized. Run: ~/.openclaw/skills/memory-manager/init.sh"
  exit 1
fi

echo "📊 Memory Statistics"
echo "=================="

# Episodic
epi_count=$(find "$MEMORY_DIR/episodic" -name "*.md" 2>/dev/null | wc -l)
epi_size=$(du -sm "$MEMORY_DIR/episodic" 2>/dev/null | cut -f1)
echo "Episodic: $epi_count entries, ${epi_size}KB"

# Semantic
sem_count=$(find "$MEMORY_DIR/semantic" -name "*.md" 2>/dev/null | wc -l)
sem_size=$(du -sm "$MEMORY_DIR/semantic" 2>/dev/null | cut -f1)
echo "Semantic: $sem_count topics, ${sem_size}KB"

# Procedural
proc_count=$(find "$MEMORY_DIR/procedural" -name "*.md" 2>/dev/null | wc -l)
proc_size=$(du -sm "$MEMORY_DIR/procedural" 2>/dev/null | cut -f1)
echo "Procedural: $proc_count workflows, ${proc_size}KB"

# Snapshots
snap_count=$(find "$MEMORY_DIR/snapshots" -name "*.tar.gz" 2>/dev/null | wc -l)
echo "Snapshots: $snap_count"

# Total
total_size=$(du -sm "$MEMORY_DIR" 2>/dev/null | cut -f1)
total_files=$(find "$MEMORY_DIR" -name "*.md" 2>/dev/null | wc -l)
echo ""
echo "Total: $total_files files, ${total_size}KB"
