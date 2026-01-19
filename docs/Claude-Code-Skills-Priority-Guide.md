# Claude Code Skills 优先级详解

## 概述

Claude Code Skills 是一种扩展 Claude 能力的 Markdown 文件。当存在多个 Skills 时，Claude Code 采用**层级覆盖机制**来决定使用哪个 Skill。

---

## 一、Skills 存储位置与优先级

### 优先级层级表

| 优先级 | 位置类型 | 路径 | 适用范围 |
|:------:|:---------|:-----|:---------|
| **1** (最高) | Enterprise/Managed | 企业托管配置 | 组织内所有用户 |
| **2** | Personal | `~/.claude/skills/` | 个人跨所有项目 |
| **3** | Project | `.claude/skills/` | 当前项目所有成员 |
| **4** (最低) | Plugin | 插件内 `skills/` 目录 | 安装该插件的用户 |

### 官方原文

> "If two Skills have the same name, **the higher row wins: managed overrides personal, personal overrides project, and project overrides plugin.**"

---

## 二、同名 Skills 覆盖规则

当多个位置存在**同名** Skill 时，高优先级的会**完全覆盖**低优先级的（不是合并）。

### 覆盖场景示例

| 存在的 Skills | 最终生效 |
|:-------------|:---------|
| Managed + Personal + Project + Plugin | **Managed** 版本 |
| Personal + Project + Plugin | **Personal** 版本 |
| Project + Plugin | **Project** 版本 |
| 仅 Plugin | **Plugin** 版本 |

### 实际应用

```
假设有一个名为 "code-review" 的 Skill 存在于多个位置：

~/.claude/skills/code-review/SKILL.md        ← Personal (优先级 2)
.claude/skills/code-review/SKILL.md          ← Project (优先级 3)
~/.claude/plugins/.../skills/code-review/    ← Plugin (优先级 4)

结果：Personal 版本生效，其他被忽略
```

---

## 三、Skills 加载机制（三层系统）

Claude Code 采用**渐进式披露**设计，优化性能和上下文使用：

### 第一层：Discovery（发现）

```
启动时加载 → 仅 name 和 description
```

- 保持启动速度快
- Claude 获得足够上下文判断何时需要每个 Skill
- **优先级在此阶段确定**：同名 Skill 仅保留最高优先级版本

### 第二层：Activation（激活）

```
请求匹配时 → 加载完整 SKILL.md
```

- 当用户请求与 Skill 描述匹配
- Claude 询问是否使用该 Skill
- 用户确认后加载完整内容

### 第三层：Execution（执行）

```
执行时 → 按需加载支持文件和脚本
```

- Claude 遵循 Skill 指令
- 按需加载引用的文件（references/）
- 按需运行捆绑脚本（scripts/）

---

## 四、不同名 Skills 的选择机制

当多个**不同名**的 Skills 都可能适用于用户请求时：

### 选择依据

1. **描述匹配度**：Claude 根据每个 Skill 的 `description` 与用户请求的语义匹配程度选择
2. **关键词触发**：包含用户提到的关键词的 Skill 更可能被选中
3. **单一选择**：通常只选择最匹配的一个执行

### 官方建议

> "Since Claude reads these descriptions to find relevant Skills, write descriptions that include keywords users would naturally say."

### 描述编写示例

**不好的描述**（太模糊）：
```yaml
description: Helps with documents
```

**好的描述**（具体且包含触发词）：
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents.
Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

---

## 五、优先级配置最佳实践

### 1. 提升插件 Skills 优先级

由于 Plugin Skills 优先级最低，如需提升：

```bash
# 将插件 skills 软链接到 Personal 目录
mkdir -p ~/.claude/skills
ln -sf /path/to/plugin/skills/* ~/.claude/skills/
```

### 2. 项目级覆盖

在项目中覆盖特定 Skill：

```bash
# 在项目根目录创建同名 skill
mkdir -p .claude/skills/skill-name
# 创建自定义 SKILL.md
```

### 3. 避免 Skills 冲突

**问题**：两个描述太相似

```yaml
# Skill A
description: Performs data analysis

# Skill B
description: Performs data analysis
```

**解决**：使用区分性触发词

```yaml
# Skill A - 销售数据分析
description: Analyzes sales data in Excel files and CRM exports.
Use when working with sales metrics, revenue, or customer data.

# Skill B - 系统日志分析
description: Analyzes log files and system metrics.
Use when debugging performance issues or reviewing system logs.
```

---

## 六、优先级与其他配置的关系

### SKILL.md 元数据字段

| 字段 | 影响优先级 | 说明 |
|:-----|:----------|:-----|
| `name` | **是** | 同名 Skill 触发优先级覆盖机制 |
| `description` | 否 | 影响匹配度，不影响优先级 |
| `allowed-tools` | 否 | 限制工具，不影响优先级 |
| `model` | 否 | 指定模型，不影响优先级 |
| `context` | 否 | 上下文隔离，不影响优先级 |
| `user-invocable` | 否 | 菜单可见性，不影响优先级 |

### 与其他功能的区别

| 功能 | 优先级机制 |
|:-----|:----------|
| **Skills** | 四层优先级覆盖（本文档） |
| **CLAUDE.md** | 无优先级，所有层级合并加载 |
| **Slash Commands** | 用户显式调用，无自动优先级 |
| **Hooks** | 按事件触发，无覆盖机制 |

---

## 七、优先级调试

### 查看当前可用 Skills

在 Claude Code 中询问：
```
What Skills are available?
```

### 确认 Skill 来源

查看 Skill 被加载时的确认提示，会显示来源路径。

### 检查同名冲突

```bash
# 查找所有同名 skill
find ~/.claude/skills .claude/skills ~/.claude/plugins -name "SKILL.md" -exec dirname {} \; | xargs -I {} basename {}
```

---

## 八、总结

| 要点 | 说明 |
|:-----|:-----|
| **优先级顺序** | Managed > Personal > Project > Plugin |
| **覆盖规则** | 同名 Skill 高优先级完全覆盖低优先级 |
| **加载时机** | 启动时确定优先级，激活时加载内容 |
| **选择机制** | 不同名 Skill 按描述匹配度选择 |
| **提升方法** | 将 Skill 放到更高优先级的目录 |

---

**参考文档**：https://code.claude.com/docs/en/skills.md
