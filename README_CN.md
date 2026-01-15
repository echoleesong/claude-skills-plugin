# Claude Skills 插件

[English](README.md) | [简体中文](README_CN.md) | [快速开始](QUICKSTART_CN.md)

一个全面且可扩展的 Claude Code 插件，为各种开发任务和工作流提供专家级技能支持。目前主要专注于 n8n 工作流开发、自动化和集成，未来计划扩展到其他领域。

> **🚀 推荐安装**：直接克隆到 `~/.claude/skills/` 以获得**最高优先级**

## 📦 包含内容

本插件目前包含 9 个专业技能，主要专注于 n8n 工作流开发：

### n8n 开发技能（7 个技能）

1. **n8n-workflow-patterns** - 经过验证的 n8n 工作流架构模式
   - 5 种核心模式：Webhook 处理、HTTP API 集成、数据库操作、AI 代理工作流、定时任务
   - 模式选择指南和工作流创建检查清单
   - 真实案例和最佳实践

2. **n8n-code-javascript** - JavaScript 代码节点专家指导
   - 数据访问模式（$input.all()、$input.first()、$input.item）
   - 内置函数（$helpers、DateTime、$jmespath）
   - 常见模式和错误预防

3. **n8n-code-python** - Python 代码节点开发
   - Python 特定模式和最佳实践
   - 数据处理和转换
   - Python 库集成

4. **n8n-expression-syntax** - 掌握 n8n 表达式语言
   - 表达式语法和数据引用
   - 内置函数和方法
   - 常见模式和故障排除

5. **n8n-node-configuration** - 正确配置节点
   - 节点特定配置模式
   - 操作依赖和要求
   - 身份验证和凭据设置

6. **n8n-validation-expert** - 部署前验证工作流
   - 工作流结构验证
   - 节点配置验证
   - 错误检测和自动修复建议

7. **n8n-mcp-tools-expert** - 有效使用 n8n MCP 工具
   - 搜索节点和模板
   - 通过 API 创建和更新工作流
   - 验证节点操作

### 通用开发技能（2 个技能）

8. **skill-creator** - 创建有效的 Claude Code 技能指南
   - 技能设计原则和最佳实践
   - 渐进式披露模式
   - 捆绑资源（脚本、参考文档、资产）

9. **更多技能即将推出** - 本插件设计为可扩展的
   - 未来技能可能涵盖：API 开发、测试、DevOps、数据处理等
   - 欢迎社区贡献

## 🎯 插件理念

本插件设计为**通用技能仓库**，可以容纳任何领域的技能：

- **当前**：主要是 n8n 工作流开发技能（7 个技能）
- **未来**：将扩展到其他开发领域
- **可扩展**：遵循 skill-creator 指南，易于添加新技能
- **社区驱动**：开放接受社区贡献

## 🚀 安装方法

### 理解 Skills 优先级

Claude Code Skills 按不同优先级加载（从高到低）：

| 优先级 | 级别 | 位置 | 作用范围 |
|:------:|:-----|:-----|:---------|
| **1** (最高) | Enterprise | 企业托管配置 | 组织内所有用户 |
| **2** | Personal | `~/.claude/skills/` | 你的所有项目 |
| **3** | Project | `.claude/skills/` | 当前项目 |
| **4** (最低) | Plugin | 插件 `skills/` 目录 | 安装该插件的用户 |

**我们推荐方法 1**，因为它能让你的 Skills 获得最高的非企业级优先级。

---

### ⭐ 方法 1：个人 Skills 目录（推荐）

直接安装到个人 skills 文件夹，获得**最高优先级**：

#### macOS / Linux

```bash
# 克隆到个人 skills 仓库目录
git clone https://github.com/echoleesong/claude-skills-plugin.git ~/.claude/skills-repo

# 将所有 skills 链接到个人目录
mkdir -p ~/.claude/skills && \
ln -sf ~/.claude/skills-repo/skills/* ~/.claude/skills/
```

#### Windows (PowerShell)

```powershell
# 克隆到个人 skills 仓库目录
git clone https://github.com/echoleesong/claude-skills-plugin.git "$env:USERPROFILE\.claude\skills-repo"

# 创建个人 skills 目录并链接
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"
Get-ChildItem "$env:USERPROFILE\.claude\skills-repo\skills" -Directory | ForEach-Object {
    New-Item -ItemType SymbolicLink -Force -Path "$env:USERPROFILE\.claude\skills\$($_.Name)" -Target $_.FullName
}
```

#### 更新 Skills

```bash
# macOS / Linux
cd ~/.claude/skills-repo && git pull

# Windows (PowerShell)
cd "$env:USERPROFILE\.claude\skills-repo"; git pull
```

✅ **优势**：最高优先级（Personal 级别），优先于所有插件，使用 `git pull` 轻松更新。

---

### 方法 2：插件市场（标准方式）

通过 Claude Code 插件市场安装：

```bash
# 添加市场
/plugin marketplace add echoleesong/claude-skills-plugin

# 安装插件
/plugin install claude-skills-plugin@echoleesong-claude-skills-plugin
```

⚠️ **注意**：插件 Skills 优先级**最低**。如需更高优先级，请使用方法 1 或在安装后升级：

<details>
<summary>📌 将插件升级为 Personal 优先级</summary>

```bash
# macOS / Linux：将插件 skills 链接到个人目录
mkdir -p ~/.claude/skills && \
ln -sf ~/.claude/plugins/cache/claude-skills-plugin-marketplace/claude-skills-plugin/*/skills/* ~/.claude/skills/
```

```powershell
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"
$pluginPath = Get-ChildItem "$env:USERPROFILE\.claude\plugins\cache\claude-skills-plugin-marketplace\claude-skills-plugin\*\skills" | Select-Object -First 1
Get-ChildItem $pluginPath -Directory | ForEach-Object {
    New-Item -ItemType SymbolicLink -Force -Path "$env:USERPROFILE\.claude\skills\$($_.Name)" -Target $_.FullName
}
```

</details>

---

### 方法 3：项目级安装

仅为特定项目安装：

```bash
# 在项目目录中
git clone https://github.com/echoleesong/claude-skills-plugin.git .claude/skills-repo

# 将 skills 链接到项目目录
mkdir -p .claude/skills && \
ln -sf .claude/skills-repo/skills/* .claude/skills/
```

✅ **适用场景**：仅在特定项目中需要这些 skills 时使用。

---

### 验证安装

重启 Claude Code 并询问："What Skills are available?"

你应该能看到本插件的 Skills。如果使用方法 1，它们将拥有 Personal 级别优先级。

## 📖 使用说明

安装后，技能会在检测到相关任务时自动激活。

### 当前技能激活方式

**n8n 开发：**
- **构建工作流**：激活 `n8n-workflow-patterns`
- **编写 JavaScript 代码**：激活 `n8n-code-javascript`
- **编写 Python 代码**：激活 `n8n-code-python`
- **使用表达式**：激活 `n8n-expression-syntax`
- **配置节点**：激活 `n8n-node-configuration`
- **验证工作流**：激活 `n8n-validation-expert`
- **使用 MCP 工具**：激活 `n8n-mcp-tools-expert`

**通用开发：**
- **创建技能**：激活 `skill-creator`

### 示例提示词

**n8n 开发：**
```
"帮我构建一个处理表单提交的 webhook 工作流"
→ 激活：n8n-workflow-patterns、n8n-node-configuration

"编写 JavaScript 代码来聚合多个 API 响应的数据"
→ 激活：n8n-code-javascript

"在部署前验证我的工作流"
→ 激活：n8n-validation-expert
```

**通用开发：**
```
"创建一个用于 PDF 处理的新技能"
→ 激活：skill-creator

"帮我设计一个用于 API 测试的技能"
→ 激活：skill-creator
```

## 🎯 技能详细说明

### n8n 开发技能

#### n8n-workflow-patterns
来自真实 n8n 工作流的经过验证的架构模式。用于构建新工作流、设计工作流结构、选择工作流模式、规划工作流架构，或询问 webhook 处理、HTTP API 集成、数据库操作、AI 代理工作流或定时任务。

### n8n-code-javascript
在 n8n 代码节点中编写 JavaScript 代码。用于在 n8n 中编写 JavaScript、使用 $input/$json/$node 语法、使用 $helpers 发起 HTTP 请求、使用 DateTime 处理日期、排查代码节点错误，或在代码节点模式之间选择。

### n8n-code-python
在 n8n 代码节点中编写 Python 代码。用于在 n8n 中编写 Python、使用项目访问模式、使用 pandas/numpy、发起 HTTP 请求、处理数据转换，或排查 Python 代码节点错误。

### n8n-expression-syntax
掌握 n8n 的表达式语言进行数据转换和操作。用于在 n8n 节点中编写表达式、访问前置节点的数据、使用内置函数、格式化日期/字符串，或排查表达式错误。

### n8n-node-configuration
使用正确的操作和参数配置 n8n 节点。用于配置特定节点操作、理解节点要求、设置身份验证，或排查节点配置错误。

### n8n-validation-expert
在部署前验证 n8n 工作流和节点配置。用于验证工作流结构、检查节点配置、检测错误，或获取常见问题的自动修复建议。

#### n8n-mcp-tools-expert
使用 n8n MCP（模型上下文协议）工具的专家指导。用于搜索节点、获取节点文档、通过 API 创建工作流、验证操作，或以编程方式使用 n8n。

### 通用开发技能

#### skill-creator
创建有效的 Claude Code 技能指南。用于创建新技能、更新现有技能、设计技能结构、编写技能文档，或学习技能最佳实践。

## 📁 插件结构

```
claude-skills-plugin/
├── .claude-plugin/
│   ├── plugin.json          # 插件元数据
│   └── marketplace.json     # 市场配置
├── skills/
│   ├── n8n-workflow-patterns/
│   ├── n8n-code-javascript/
│   ├── n8n-code-python/
│   ├── n8n-expression-syntax/
│   ├── n8n-node-configuration/
│   ├── n8n-validation-expert/
│   ├── n8n-mcp-tools-expert/
│   └── skill-creator/
├── LICENSE
├── README.md
├── README_CN.md
└── CHANGELOG.md
```

## 🤝 贡献

欢迎贡献！本插件设计为社区驱动的技能仓库。

### 如何贡献

1. **添加新技能**：使用 `skill-creator` 技能来设计和实现新技能
2. **改进现有技能**：提交 PR 来增强当前技能
3. **报告问题**：帮助我们识别错误或需要改进的地方
4. **建议新技能领域**：提出有价值的新技能领域

### 我们感兴趣的技能领域

- API 开发和测试
- DevOps 和 CI/CD
- 数据处理和分析
- 前端/后端框架
- 测试框架
- 文档生成
- 更多领域！

请随时提交问题或拉取请求。

## 📄 许可证

MIT 许可证 - 详见 LICENSE 文件

## 🔗 相关链接

- **仓库地址**：https://github.com/echoleesong/claude-skills-plugin
- **问题反馈**：https://github.com/echoleesong/claude-skills-plugin/issues
- **n8n 文档**：https://docs.n8n.io

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史和更新。

## 🙏 致谢

- n8n 技能基于真实的工作流开发经验和 n8n 社区的最佳实践构建
- skill-creator 受 Claude Code 官方技能开发指南启发
- 感谢所有贡献者和 Claude Code 社区

---

**用 ❤️ 为 Claude Code 社区打造**
