# 快速开始指南

## 安装（3步）

### 第1步：添加市场
```bash
/plugin marketplace add echoleesong/claude-skills-plugin
```

### 第2步：安装插件
```bash
/plugin install claude-skills-plugin@echoleesong-claude-skills-plugin
```

### 第3步：开始使用
技能会在你处理相关任务时自动激活！

## 使用示例

安装后尝试这些提示词：

```
"帮我在n8n中构建一个webhook工作流"
→ 激活 n8n-workflow-patterns 技能

"编写JavaScript代码来处理API数据"
→ 激活 n8n-code-javascript 技能

"为我的项目创建一个新技能"
→ 激活 skill-creator 技能
```

## 验证安装

```bash
# 列出已安装的插件
/plugin list

# 检查市场
/plugin marketplace list
```

## 更新插件

```bash
# 更新到最新版本
/plugin update claude-skills-plugin
```

## 故障排除

### 找不到插件？
确保你已经先添加了市场：
```bash
/plugin marketplace add echoleesong/claude-skills-plugin
```

### 技能没有激活？
1. 检查插件是否启用：`/plugin list`
2. 重启 Claude Code
3. 尝试更具体的与技能相关的提示词

## 其他安装方法

### 方法1：直接从GitHub安装（推荐）
```bash
/plugin marketplace add echoleesong/claude-skills-plugin
/plugin install claude-skills-plugin@echoleesong-claude-skills-plugin
```

### 方法2：个人 Skills 目录（最高优先级）
```bash
# 克隆并运行安装脚本
git clone https://github.com/echoleesong/claude-skills-plugin.git ~/.claude/skills-repo
cd ~/.claude/skills-repo && ./install.sh

# 以后更新使用
cd ~/.claude/skills-repo && git pull && ./install.sh

# 可选：设置 git pull 后自动同步
./setup-hooks.sh
```

### 方法3：本地开发
```bash
git clone https://github.com/echoleesong/claude-skills-plugin.git
/plugin marketplace add ./claude-skills-plugin
/plugin install claude-skills-plugin
```

### 方法4：临时使用（无需安装）
```bash
git clone https://github.com/echoleesong/claude-skills-plugin.git
claude --plugin-dir ./claude-skills-plugin
```

## 需要帮助？

- 📖 [完整文档](README_CN.md)
- 🐛 [报告问题](https://github.com/echoleesong/claude-skills-plugin/issues)
- 💬 [讨论区](https://github.com/echoleesong/claude-skills-plugin/discussions)
