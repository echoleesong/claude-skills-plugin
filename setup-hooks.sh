#!/bin/bash
# Claude Skills Plugin - Git Hooks 设置脚本
# 设置 post-merge hook，使 git pull 后自动同步 skills

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_DIR="$SCRIPT_DIR/.git"
HOOKS_DIR="$GIT_DIR/hooks"

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Claude Skills Plugin - Git Hooks 设置                  ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# 检查是否是 git 仓库
if [ ! -d "$GIT_DIR" ]; then
    echo -e "${RED}错误: 当前目录不是 git 仓库${NC}"
    exit 1
fi

# 创建 hooks 目录（如果不存在）
mkdir -p "$HOOKS_DIR"

# 创建 post-merge hook
POST_MERGE="$HOOKS_DIR/post-merge"

cat > "$POST_MERGE" << 'HOOK_CONTENT'
#!/bin/bash
# Claude Skills Plugin - Post-merge hook
# 在 git pull/merge 后自动同步 skills

# 获取仓库根目录
REPO_ROOT="$(git rev-parse --show-toplevel)"
INSTALL_SCRIPT="$REPO_ROOT/install.sh"

if [ -f "$INSTALL_SCRIPT" ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║  检测到代码更新，正在自动同步 skills...                     ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    bash "$INSTALL_SCRIPT"
fi
HOOK_CONTENT

chmod +x "$POST_MERGE"

# 可选：创建 post-checkout hook（用于 git clone 后或切换分支时）
POST_CHECKOUT="$HOOKS_DIR/post-checkout"

cat > "$POST_CHECKOUT" << 'HOOK_CONTENT'
#!/bin/bash
# Claude Skills Plugin - Post-checkout hook
# 在 git checkout/clone 后自动同步 skills

# 参数: $1 = previous HEAD, $2 = new HEAD, $3 = flag (1=branch checkout, 0=file checkout)
# 只在分支切换或 clone 时运行
if [ "$3" = "1" ]; then
    REPO_ROOT="$(git rev-parse --show-toplevel)"
    INSTALL_SCRIPT="$REPO_ROOT/install.sh"

    if [ -f "$INSTALL_SCRIPT" ]; then
        echo ""
        echo "╔═══════════════════════════════════════════════════════════╗"
        echo "║  检测到分支切换，正在自动同步 skills...                     ║"
        echo "╚═══════════════════════════════════════════════════════════╝"
        echo ""
        bash "$INSTALL_SCRIPT"
    fi
fi
HOOK_CONTENT

chmod +x "$POST_CHECKOUT"

echo -e "${GREEN}✓ Git hooks 设置完成！${NC}"
echo ""
echo -e "已创建以下 hooks:"
echo -e "  ${BLUE}post-merge${NC}    - git pull/merge 后自动同步 skills"
echo -e "  ${BLUE}post-checkout${NC} - 切换分支后自动同步 skills"
echo ""
echo -e "${YELLOW}注意: Git hooks 不会被 git 追踪，其他用户需要单独运行此脚本${NC}"
echo -e "${YELLOW}或者首次 clone 后运行一次 ./install.sh${NC}"
echo ""
