# Skill 元数据规范 v1.0

本文档定义了 SKILL.md 文件的扩展元数据格式，用于支持 Skill 生命周期管理。

## 1. Frontmatter 字段定义

### 1.1 基础字段（必需）

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `name` | string | ✅ | Skill 名称，小写字母、数字、连字符，最多 64 字符 |
| `description` | string | ✅ | 详细描述，包含"做什么"和"何时使用"，最多 1024 字符 |

### 1.2 扩展字段（可选，用于生命周期管理）

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `source_url` | string | ❌ | 来源仓库 URL（GitHub/GitLab 等） |
| `source_hash` | string | ❌ | 来源仓库的 commit hash（40 字符） |
| `version` | string | ❌ | 语义化版本号（如 `1.0.0`） |
| `created_at` | string | ❌ | 创建日期（ISO-8601 格式，如 `2026-01-23`） |
| `updated_at` | string | ❌ | 最后更新日期（ISO-8601 格式） |
| `evolution_enabled` | boolean | ❌ | 是否启用经验进化（默认 `true`） |

### 1.3 其他可选字段

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| `license` | string | ❌ | 许可证（如 `MIT`） |
| `entry_point` | string | ❌ | 主入口脚本路径（如 `scripts/main.py`） |
| `dependencies` | array | ❌ | 依赖列表（如 `["python>=3.8", "pyyaml"]`） |
| `allowed-tools` | string | ❌ | 限制可用工具（如 `Read, Grep, Glob`） |
| `model` | string | ❌ | 指定模型（如 `claude-opus-4-5`） |

## 2. 完整示例

### 2.1 基础 Skill（仅必需字段）

```yaml
---
name: my-skill
description: 这是一个示例 Skill。当用户需要执行某个特定任务时使用此 Skill。
---

# My Skill

Skill 内容...
```

### 2.2 带生命周期管理的 Skill

```yaml
---
name: yt-dlp-wrapper
description: YouTube 视频下载工具封装。当用户需要下载 YouTube 视频、提取音频、或获取视频信息时使用此 Skill。

# 生命周期管理字段
source_url: https://github.com/yt-dlp/yt-dlp
source_hash: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
version: 2024.01.15
created_at: 2026-01-23
updated_at: 2026-01-23
evolution_enabled: true

# 其他可选字段
license: Unlicense
entry_point: scripts/wrapper.py
dependencies:
  - yt-dlp>=2024.01.01
  - ffmpeg
---

# yt-dlp Wrapper

Skill 内容...
```

### 2.3 禁用经验进化的 Skill

```yaml
---
name: static-skill
description: 一个不需要经验进化的静态 Skill。
evolution_enabled: false
---

# Static Skill

此 Skill 不会记录用户经验。
```

## 3. 字段验证规则

### 3.1 name 字段

- **格式**: `^[a-z0-9][a-z0-9-]*[a-z0-9]$` 或单字符 `^[a-z0-9]$`
- **长度**: 1-64 字符
- **示例**: `my-skill`, `n8n-code-javascript`, `pdf`

### 3.2 description 字段

- **长度**: 10-1024 字符
- **内容要求**:
  - 必须描述 Skill 的功能（"做什么"）
  - 必须描述触发条件（"何时使用"）
- **示例**: "Markdown 转 PowerPoint 工具。当用户需要将 MD 文件转换为 PPTX、创建演示文稿、或生成幻灯片时使用。"

### 3.3 source_url 字段

- **格式**: 有效的 URL，支持 `https://` 协议
- **支持平台**: GitHub, GitLab, Bitbucket 等
- **示例**: `https://github.com/owner/repo`

### 3.4 source_hash 字段

- **格式**: 40 字符的十六进制字符串（Git commit hash）
- **示例**: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0`

### 3.5 version 字段

- **格式**: 语义化版本号 `MAJOR.MINOR.PATCH` 或日期版本 `YYYY.MM.DD`
- **示例**: `1.0.0`, `2024.01.15`

### 3.6 日期字段（created_at, updated_at）

- **格式**: ISO-8601 日期格式
- **示例**: `2026-01-23`, `2026-01-23T10:30:00Z`

## 4. evolution.json 格式

当 `evolution_enabled: true`（默认）时，Skill 目录下可能存在 `evolution.json` 文件，用于存储用户经验。

### 4.1 结构定义

```json
{
  "preferences": ["string"],
  "fixes": ["string"],
  "contexts": ["string"],
  "custom_prompts": "string",
  "last_updated": "ISO-8601 datetime",
  "last_evolved_hash": "string"
}
```

### 4.2 字段说明

| 字段 | 类型 | 描述 |
|------|------|------|
| `preferences` | array[string] | 用户偏好列表 |
| `fixes` | array[string] | 已知问题修复方案列表 |
| `contexts` | array[string] | 特定使用场景列表 |
| `custom_prompts` | string | 自定义指令注入（可选） |
| `last_updated` | string | 最后更新时间（ISO-8601） |
| `last_evolved_hash` | string | 最后进化时的 source_hash |

### 4.3 示例

```json
{
  "preferences": [
    "用户希望下载时默认静音",
    "优先使用 mp4 格式"
  ],
  "fixes": [
    "Windows 下 ffmpeg 路径需要转义",
    "某些视频需要添加 --cookies 参数"
  ],
  "contexts": [
    "批量下载播放列表时使用 --yes-playlist",
    "下载直播时需要等待直播结束"
  ],
  "custom_prompts": "在执行下载前，总是先打印预估文件大小和下载时间",
  "last_updated": "2026-01-23T10:30:00Z",
  "last_evolved_hash": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
}
```

## 5. 缝合后的 SKILL.md 章节

当 `smart_stitch.py` 执行后，会在 SKILL.md 末尾生成或更新以下章节：

```markdown
## User-Learned Best Practices & Constraints

> Auto-Generated Section: 由 skill-evolution 维护，请勿手动编辑

### User Preferences
- 用户偏好1
- 用户偏好2

### Known Fixes & Workarounds
- 修复方案1
- 修复方案2

### Context-Specific Notes
- 场景说明1
- 场景说明2

### Custom Instruction Injection
自定义指令内容...
```

## 6. 向后兼容性

### 6.1 兼容性保证

- 所有扩展字段均为**可选**
- 现有 Skills 无需修改即可继续使用
- 不包含扩展字段的 Skills 将被视为"静态 Skill"，不参与生命周期管理

### 6.2 版本迁移

如需为现有 Skill 启用生命周期管理，只需添加扩展字段：

```yaml
---
name: existing-skill
description: 现有 Skill 描述

# 新增以下字段即可启用生命周期管理
version: 1.0.0
created_at: 2026-01-23
evolution_enabled: true
---
```

## 7. 验证工具

使用 `scripts/validate_metadata.py` 验证 SKILL.md 的元数据：

```bash
python scripts/validate_metadata.py path/to/skill/SKILL.md
```

输出示例：

```
✅ name: valid
✅ description: valid
✅ source_url: valid
✅ source_hash: valid
⚠️ version: missing (optional)
⚠️ created_at: missing (optional)
```
