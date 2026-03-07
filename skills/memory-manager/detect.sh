#!/bin/bash
# Detect compression risk

MEMORY_DIR="$HOME/.openclaw/skills/memory-manager/memory"

if [ ! -d "$MEMORY_DIR" ]; then
  echo "⚠️ Memory not initialized. Run: ~/.openclaw/skills/memory-manager/init.sh"
  exit 1
fi

# Count files and estimate size
total_files=$(find "$MEMORY_DIR" -type f \( -name "*.md" -o -name "*.txt" \) 2>/dev/null | wc -l)
total_size=$(du -sm "$MEMORY_DIR" 2>/dev/null | cut -f1)

# Estimate context usage (rough heuristic: ~500 tokens per KB)
estimated_tokens=$((total_size * 500))

# Thresholds (approximate)
warning_threshold=70000  # ~70%
critical_threshold=85000 # ~85%

if [ "$estimated_tokens" -lt "$warning_threshold" ]; then
  echo "✅ Safe ($estimated_tokens tokens, $total_files files)"
  echo "  Context usage: $((estimated_tokens * 100 / 128000))%"
elif [ "$estimated_tokens" -lt "$critical_threshold" ]; then
  echo "⚠️ WARNING ($estimated_tokens tokens, $total_files files)"
  echo "  Context usage: $((estimated_tokens * 100 / 128000))%"
  echo "  Run: ~/.openclaw/skills/memory-manager/organize.sh"
else
  echo "🚨 CRITICAL ($estimated_tokens tokens, $total_files files)"
  echo "  Context usage: $((estimated_tokens * 100 / 128000))%"
  echo "  Run: ~/.openclaw/skills/memory-manager/snapshot.sh NOW"
fi
