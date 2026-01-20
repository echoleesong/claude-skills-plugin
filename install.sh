#!/bin/bash
# Claude Skills Plugin - 自动安装脚本
# 自动创建 skills 目录的软链接到 ~/.claude/skills/

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SOURCE="$SCRIPT_DIR/skills"
CLAUDE_DIR="$HOME/.claude"
SKILLS_TARGET="$CLAUDE_DIR/skills"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Claude Skills Plugin - 自动安装脚本                    ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 检查 skills 源目录是否存在
if [ ! -d "$SKILLS_SOURCE" ]; then
    echo -e "${RED}错误: skills 目录不存在于 $SKILLS_SOURCE${NC}"
    exit 1
fi

# 创建 ~/.claude 目录（如果不存在）
if [ ! -d "$CLAUDE_DIR" ]; then
    echo -e "${YELLOW}创建 Claude 配置目录: $CLAUDE_DIR${NC}"
    mkdir -p "$CLAUDE_DIR"
fi

# 创建 ~/.claude/skills 目录（如果不存在）
if [ ! -d "$SKILLS_TARGET" ]; then
    echo -e "${YELLOW}创建 skills 目录: $SKILLS_TARGET${NC}"
    mkdir -p "$SKILLS_TARGET"
fi

# 统计信息
CREATED=0
UPDATED=0
SKIPPED=0

echo -e "${BLUE}正在链接 skills...${NC}"
echo ""

# 遍历 skills 目录中的每个子目录
for skill_dir in "$SKILLS_SOURCE"/*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        link_target="$SKILLS_TARGET/$skill_name"
        
        # 检查是否已存在
        if [ -L "$link_target" ]; then
            # 是软链接，检查是否指向正确位置
            current_target=$(readlink "$link_target" 2>/dev/null || echo "")
            if [ "$current_target" = "${skill_dir%/}" ] || [ "$current_target" = "$skill_dir" ]; then
                echo -e "  ${GREEN}✓${NC} $skill_name (已是最新)"
                ((SKIPPED++))
            else
                # 更新软链接
                rm "$link_target"
                ln -sf "${skill_dir%/}" "$link_target"
                echo -e "  ${YELLOW}↻${NC} $skill_name (已更新)"
                ((UPDATED++))
            fi
        elif [ -e "$link_target" ]; then
            # 存在但不是软链接（可能是普通目录）
            echo -e "  ${YELLOW}!${NC} $skill_name (已存在，跳过，请手动处理)"
            ((SKIPPED++))
        else
            # 创建新的软链接
            ln -sf "${skill_dir%/}" "$link_target"
            echo -e "  ${GREEN}+${NC} $skill_name (已创建)"
            ((CREATED++))
        fi
    fi
done

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}安装完成！${NC}"
echo ""
echo -e "  新创建: ${GREEN}$CREATED${NC}"
echo -e "  已更新: ${YELLOW}$UPDATED${NC}"
echo -e "  已跳过: ${BLUE}$SKIPPED${NC}"
echo ""
echo -e "${BLUE}Skills 已链接到: $SKILLS_TARGET${NC}"
echo ""
echo -e "${YELLOW}提示: 请重启 Claude Code 以使更改生效${NC}"
echo ""

# 可选：设置 git hook
if [ "$1" = "--setup-hook" ]; then
    HOOK_DIR="$SCRIPT_DIR/.git/hooks"
    if [ -d "$HOOK_DIR" ]; then
        HOOK_FILE="$HOOK_DIR/post-merge"
        cat > "$HOOK_FILE" << 'EOF'
#!/bin/bash
# Auto-run install script after git pull
echo "检测到代码更新，正在同步 skills..."
"$(dirname "$0")/../../install.sh"
EOF
        chmod +x "$HOOK_FILE"
        echo -e "${GREEN}Git hook 已设置！以后 git pull 会自动同步 skills。${NC}"
    else
        echo -e "${RED}无法设置 Git hook：.git/hooks 目录不存在${NC}"
    fi
fi
