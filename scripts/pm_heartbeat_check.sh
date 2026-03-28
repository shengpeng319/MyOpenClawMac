#!/bin/bash
# PM 心跳检查脚本
# 检查所有 Task Agent 的心跳状态，卡住超过5分钟的任务会报警

ACTIVE_DIR="$HOME/.openclaw/workspace/active_tasks"
TIMEOUT=300  # 5分钟
CURRENT_TIME=$(date +%s)

echo "=== PM 心跳检查 [$(date '+%Y-%m-%d %H:%M:%S')] ==="

found_stale=false
for heartbeat in "$ACTIVE_DIR"/*.json; do
  [ -f "$heartbeat" ] || continue
  
  TASK_ID=$(basename "$heartbeat" .json)
  LAST_BEAT=$(jq -r '.last_beat' "$heartbeat" 2>/dev/null)
  DESC=$(jq -r '.desc' "$heartbeat" 2>/dev/null)
  STATUS=$(jq -r '.status' "$heartbeat" 2>/dev/null)
  
  # 检查 jq 是否成功
  if [ $? -ne 0 ] || [ "$LAST_BEAT" = "null" ]; then
    echo "⚠️  $TASK_ID: 心跳文件格式错误"
    continue
  fi
  
  ELAPSED=$((CURRENT_TIME - LAST_BEAT))
  
  if [ $ELAPSED -gt $TIMEOUT ]; then
    echo "⚠️  任务 [$TASK_ID] \"$DESC\" 已卡住超过5分钟 (${ELAPSED}秒未更新)"
    found_stale=true
  else
    echo "✅  $TASK_ID \"$DESC\" - 正常 (${ELAPSED}秒前更新)"
  fi
done

if [ "$found_stale" = false ]; then
  echo "所有任务运行正常，无卡住任务"
fi

echo "=== 检查完成 ==="
