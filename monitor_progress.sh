#!/bin/bash
# Spider生成进度监控脚本

echo "=========================================="
echo "Spider生成进度监控"
echo "=========================================="
echo ""

# 检查进度文件
PROGRESS_FILE="./generated_spiders_batch1/batch_progress.json"

if [ ! -f "$PROGRESS_FILE" ]; then
    echo "⚠️  进度文件不存在，生成可能还未开始或已完成"
    echo "文件路径: $PROGRESS_FILE"
    exit 1
fi

# 统计进度
TOTAL=$(jq '. | length' "$PROGRESS_FILE")
SUCCESS=$(jq '[.[] | select(.success == true)] | length' "$PROGRESS_FILE")
FAILED=$(jq '[.[] | select(.success == false)] | length' "$PROGRESS_FILE")

echo "📊 总体进度"
echo "-------------------------------------------"
echo "总数: $TOTAL"
echo "成功: $SUCCESS ✓"
echo "失败: $FAILED ✗"
echo "成功率: $(echo "scale=1; $SUCCESS * 100 / $TOTAL" | bc)%"
echo ""

# 显示最近5个
echo "📝 最近处理的平台"
echo "-------------------------------------------"
jq -r '.[-5:] | .[] | "\(.platform_name): \(if .success then "✓" else "✗" end)"' "$PROGRESS_FILE"
echo ""

# 显示失败的
FAILED_COUNT=$(jq '[.[] | select(.success == false)] | length' "$PROGRESS_FILE")
if [ "$FAILED_COUNT" -gt 0 ]; then
    echo "❌ 失败的平台"
    echo "-------------------------------------------"
    jq -r '.[] | select(.success == false) | "\(.platform_name): \(.errors[0])"' "$PROGRESS_FILE"
    echo ""
fi

# 检查日志
LOG_FILE="/tmp/batch1_optimized.log"
if [ -f "$LOG_FILE" ]; then
    echo "📄 最新日志 (最后10行)"
    echo "-------------------------------------------"
    tail -10 "$LOG_FILE"
fi

echo ""
echo "=========================================="
echo "提示: 运行 'bash monitor_progress.sh' 查看最新进度"
echo "=========================================="
