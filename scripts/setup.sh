#!/usr/bin/env bash
# AI Team Hub — 一键 MCP 配置脚本
# 自动检测本地 Agent 工具，写入 MCP Server 配置
#
# 用法:
#   curl -s http://<server>:7070/setup.sh | bash           # 直接执行
#   curl -s http://<server>:7070/setup.sh | bash -s -- --dry-run  # 预览
#   bash setup.sh http://192.168.1.100:7070                # 指定服务器
set -e

DRY_RUN=false
SERVER_URL="http://localhost:7070"

for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=true ;;
    *) SERVER_URL="$arg" ;;
  esac
done

MCP_URL="${SERVER_URL}/mcp"
MCP_CONFIG=$(cat <<EOF
{
  "mcpServers": {
    "ai-team-hub": {
      "type": "sse",
      "url": "${MCP_URL}"
    }
  }
}
EOF
)

TOOLS=(
  "Claude Code|$HOME/.claude/settings.json"
  "OpenCode|./opencode.json"
  "Codex|$HOME/.codex/config.json"
  "Cursor|./.cursor/mcp.json"
  "Windsurf|./.windsurf/mcp.json"
  "Continue|$HOME/.continue/config.json"
)

detected=0
configured=0
DRY_TAG=""
if $DRY_RUN; then DRY_TAG=" [预览]"; fi

echo ""
echo "  AI Team Hub — MCP 自动配置${DRY_TAG}"
echo "  服务器: ${SERVER_URL}"
echo "  MCP 地址: ${MCP_URL}"
echo ""

for entry in "${TOOLS[@]}"; do
  tool="${entry%%|*}"
  file="${entry##*|}"

  # Expand ~ and $HOME
  file="${file/#\$HOME/$HOME}"
  dir=$(dirname "$file")

  if [ -f "$file" ] || [ -d "$dir" ]; then
    detected=$((detected + 1))

    if $DRY_RUN; then
      if [ -f "$file" ]; then
        echo "  [$tool] → 更新 $file"
      else
        echo "  [$tool] → 创建 $file"
      fi
      configured=$((configured + 1))
      continue
    fi

    mkdir -p "$dir"

    if [ -f "$file" ] && [ -s "$file" ]; then
      if command -v python3 &>/dev/null; then
        python3 -c "
import json
try:
    with open('$file') as f:
        cfg = json.load(f)
except Exception:
    cfg = {}
cfg.setdefault('mcpServers', {})
cfg['mcpServers']['ai-team-hub'] = {'type': 'sse', 'url': '${MCP_URL}'}
with open('$file', 'w') as f:
    json.dump(cfg, f, indent=2)
    f.write('\n')
" 2>/dev/null && {
          echo "  [$tool] ✓ 已更新 $file"
          configured=$((configured + 1))
        } || {
          echo "  [$tool] ✗ JSON 解析失败，跳过 $file"
        }
      else
        echo "  [$tool] ✗ 需要 python3，跳过"
      fi
    else
      echo "$MCP_CONFIG" > "$file"
      echo "  [$tool] ✓ 已创建 $file"
      configured=$((configured + 1))
    fi
  fi
done

echo ""
if $DRY_RUN; then
  echo "  [预览] 将配置 $configured 个工具"
  echo "  去掉 --dry-run 即可正式执行"
else
  echo "  检测到 $detected 个工具，成功配置 $configured 个"
  echo "  重启对应工具即可使用。"
fi
echo ""
