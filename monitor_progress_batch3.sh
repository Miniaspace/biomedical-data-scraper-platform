#!/bin/bash
# Spider生成进度监控脚本 - 第3批

echo "=========================================="
echo "Spider生成进度监控 - 第3批 (最后一批)"
echo "=========================================="
echo ""

# 检查进度文件
PROGRESS_FILE="./generated_spiders_batch3/batch_progress.json"

if [ ! -f "$PROGRESS_FILE" ]; then
    echo "⚠️  进度文件不存在，生成可能还未开始"
    exit 1
fi

# 统计进度
TOTAL=$(jq '. | length' "$PROGRESS_FILE")
SUCCESS=$(jq '[.[] | select(.success == true)] | length' "$PROGRESS_FILE")
FAILED=$(jq '[.[] | select(.success == false)] | length' "$PROGRESS_FILE")

echo "📊 第3批进度 (51-75号平台)"
echo "-------------------------------------------"
echo "总数: $TOTAL / 25"
echo "成功: $SUCCESS ✓"
echo "失败: $FAILED ✗"
if [ "$TOTAL" -gt 0 ]; then
    echo "成功率: $(echo "scale=1; $SUCCESS * 100 / $TOTAL" | bc)%"
fi
echo ""

# 显示最近5个
echo "📝 最近处理的平台"
echo "-------------------------------------------"
jq -r '.[-5:] | .[] | "\(.platform_name): \(if .success then "✓" else "✗" end)"' "$PROGRESS_FILE"
echo ""

# 检查日志
LOG_FILE="/tmp/batch3_optimized.log"
if [ -f "$LOG_FILE" ]; then
    echo "📄 最新日志 (最后5行)"
    echo "-------------------------------------------"
    tail -5 "$LOG_FILE"
fi
