# Skill 生命周期管理系统开发方案

> 分支: `feat/skill-lifecycle-management`
> 创建日期: 2026-01-23
> 状态: 规划中

## 一、项目概述

### 1.1 目标

将 Khazix-Skills 的核心创新（自动化工厂、版本管理、经验进化）与当前 Skills 插件仓库结合，实现现代化的 Skills 自迭代方案。

### 1.2 设计理念

**"Skills 管理 Skills"（自举架构）**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Skill 完整生命周期                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────────┐ │
│  │ skill-factory│   │skill-manager │   │    skill-evolution       │ │
│  │              │   │              │   │                          │ │
│  │ • GitHub转换 │──→│ • 版本检查   │──→│ • 经验持久化             │ │
│  │ • 模板生成   │   │ • 批量更新   │   │ • 智能缝合               │ │
│  │ • 元数据注入 │   │ • 库存管理   │   │ • 跨版本对齐             │ │
│  └──────────────┘   └──────────────┘   └──────────────────────────┘ │
│         ↑                   ↑                      ↑                 │
│         └───────────────────┴──────────────────────┘                 │
│                    统一的扩展元数据格式                               │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.3 方案选择

**方案 A + 轻量 B（混合方案）**

| 场景 | 使用方式 |
|------|----------|
| 日常使用 | `/skill-factory`, `/skill-manager`, `/skill-evolution` → Claude 智能交互 |
| CI/CD 自动化 | `python scripts/check_updates.py` → 直接执行 |
| 批量操作 | `python scripts/batch_evolve.py` → 高效处理 |

---

## 二、扩展元数据格式规范

### 2.1 SKILL.md 扩展 Frontmatter

```yaml
---
# === 基础字段（必需）===
name: skill-name                    # 小写字母、数字、连字符（最多64字符）
description: 详细描述              # 包含"做什么"和"何时使用"（最多1024字符）

# === 扩展字段（可选，用于生命周期管理）===
source_url: https://github.com/...  # 来源仓库 URL
source_hash: abc123def456...        # 来源仓库的 commit hash
version: 1.0.0                      # 语义化版本号
created_at: 2026-01-23              # 创建日期（ISO-8601）
updated_at: 2026-01-23              # 最后更新日期
evolution_enabled: true             # 是否启用经验进化（默认 true）

# === 可选字段 ===
license: MIT                        # 许可证
entry_point: scripts/main.py        # 主入口脚本
dependencies:                       # 依赖列表
  - python>=3.8
  - pyyaml
---
```

### 2.2 evolution.json 结构

```json
{
  "preferences": [
    "用户偏好描述1",
    "用户偏好描述2"
  ],
  "fixes": [
    "已知问题修复方案1",
    "已知问题修复方案2"
  ],
  "contexts": [
    "特定使用场景1",
    "特定使用场景2"
  ],
  "custom_prompts": "自定义指令注入（可选）",
  "last_updated": "2026-01-23T10:30:00Z",
  "last_evolved_hash": "abc123..."
}
```

### 2.3 向后兼容性

- 所有扩展字段均为**可选**
- 现有 Skills 无需修改即可继续使用
- 渐进式采用：用户可选择性启用生命周期管理

---

## 三、开发阶段规划

### Phase 1: 扩展元数据格式规范

**目标**: 定义并文档化扩展的 SKILL.md 格式

**任务**:
- [ ] 创建 `references/metadata-spec.md` 规范文档
- [ ] 更新 `skill-creator/SKILL.md` 添加扩展字段说明
- [ ] 创建元数据验证脚本 `scripts/validate_metadata.py`

**产出**:
- 元数据规范文档
- 验证工具

---

### Phase 2: skill-factory（GitHub 仓库转 Skill）

**目标**: 实现从 GitHub 仓库自动生成标准化 Skill 的能力

**目录结构**:
```
skills/skill-factory/
├── SKILL.md                    # 主 Skill 文件
├── scripts/
│   ├── fetch_github_info.py    # 获取 GitHub 仓库信息
│   └── create_skill.py         # 创建 Skill 目录结构
└── references/
    └── templates.md            # 模板说明
```

**核心功能**:
1. **信息获取**: 通过 `git ls-remote` 获取 commit hash，通过 raw URL 获取 README
2. **目录生成**: 创建标准化的 Skill 目录结构
3. **元数据注入**: 自动填充扩展元数据字段

**触发方式**:
- `/skill-factory <github_url>`
- "将这个仓库打包成 Skill: <url>"
- "从 GitHub 创建 Skill"

**工作流**:
```
1. 用户提供 GitHub URL
2. fetch_github_info.py 获取仓库元数据
3. Claude 分析 README，理解工具用法
4. create_skill.py 生成目录结构
5. Claude 完善 SKILL.md 和 wrapper 脚本
6. 输出创建完成提示
```

---

### Phase 3: skill-manager（版本管理和更新）

**目标**: 实现 Skills 的版本检查、更新和库存管理

**目录结构**:
```
skills/skill-manager/
├── SKILL.md                    # 主 Skill 文件
├── scripts/
│   ├── scan_and_check.py       # 扫描并检查更新
│   ├── list_skills.py          # 列出所有 Skills
│   └── delete_skill.py         # 删除 Skill
└── references/
    └── update-workflow.md      # 更新工作流说明
```

**核心功能**:
1. **扫描审计**: 扫描 skills 目录，解析所有 SKILL.md 的 frontmatter
2. **版本检查**: 并发调用 `git ls-remote` 比较 local_hash 和 remote_hash
3. **状态报告**: 生成 JSON 格式的状态报告（outdated/current/error）
4. **更新工作流**: 引导 Agent 执行更新操作
5. **库存管理**: 列出、删除 Skills

**触发方式**:
- `/skill-manager check` - 检查更新
- `/skill-manager list` - 列出所有 Skills
- `/skill-manager delete <name>` - 删除 Skill
- "检查我的 Skills 是否有更新"

**状态报告格式**:
```json
[
  {
    "name": "yt-dlp",
    "dir": "/path/to/yt-dlp",
    "source_url": "https://github.com/yt-dlp/yt-dlp",
    "local_hash": "abc123...",
    "remote_hash": "def456...",
    "status": "outdated",
    "message": "New commits available (50 behind)"
  }
]
```

---

### Phase 4: skill-evolution（经验持久化和进化）

**目标**: 实现用户经验的持久化存储和跨版本保留

**目录结构**:
```
skills/skill-evolution/
├── SKILL.md                    # 主 Skill 文件
├── scripts/
│   ├── merge_evolution.py      # 增量合并经验数据
│   ├── smart_stitch.py         # 智能缝合到文档
│   └── align_all.py            # 全量对齐工具
└── references/
    └── evolution-format.md     # 进化数据格式说明
```

**核心功能**:
1. **复盘诊断**: 分析对话中的问题点和成功方案
2. **经验提取**: 将非结构化反馈转为结构化 JSON
3. **增量合并**: 去重合并新经验到 evolution.json
4. **智能缝合**: 将经验自动写入 SKILL.md 的专用章节
5. **跨版本对齐**: Skill 更新后重新缝合经验

**触发方式**:
- `/skill-evolution` 或 `/evolve`
- "复盘一下刚才的对话"
- "把这个经验保存到 Skill 里"
- "记录一下这个问题的解决方案"

**工作流**:
```
1. 用户触发复盘
2. Claude 分析对话，提取经验
3. 生成结构化 JSON
4. merge_evolution.py 增量合并
5. smart_stitch.py 缝合到文档
6. 下次使用时 Claude 可看到这些最佳实践
```

**缝合后的 SKILL.md 章节**:
```markdown
## User-Learned Best Practices & Constraints

> Auto-Generated Section: 由 skill-evolution 维护，请勿手动编辑

### User Preferences
- 用户偏好1
- 用户偏好2

### Known Fixes & Workarounds
- 修复方案1
- 修复方案2

### Custom Instruction Injection
自定义指令内容...
```

---

### Phase 5: 轻量级 scripts/ 脚本

**目标**: 提供独立可执行的脚本，支持 CI/CD 和高级用户

**目录结构**:
```
scripts/
├── check_updates.py            # 批量检查更新（独立可执行）
├── batch_evolve.py             # 批量进化对齐（独立可执行）
└── validate_all.py             # 批量验证元数据（独立可执行）
```

**使用场景**:
- GitHub Actions 自动检查更新
- 本地批量操作
- 离线环境使用

**示例**:
```bash
# 检查所有 Skills 的更新状态
python scripts/check_updates.py --skills-dir ./skills --output report.json

# 批量对齐所有 evolution.json
python scripts/batch_evolve.py --skills-dir ./skills

# 验证所有 Skills 的元数据
python scripts/validate_all.py --skills-dir ./skills
```

---

### Phase 6: 文档更新

**目标**: 更新项目文档，反映新功能

**任务**:
- [ ] 更新 README.md / README_CN.md
- [ ] 更新 CHANGELOG.md
- [ ] 更新 QUICKSTART.md / QUICKSTART_CN.md
- [ ] 创建 `docs/skill-lifecycle-guide.md` 用户指南

---

## 四、技术实现细节

### 4.1 轻量级版本检查

```python
import subprocess

def get_remote_hash(github_url: str) -> str:
    """通过 git ls-remote 获取远程 HEAD hash（无需 clone）"""
    result = subprocess.run(
        ['git', 'ls-remote', github_url, 'HEAD'],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.split()[0]
```

### 4.2 并发检查

```python
import concurrent.futures

def check_all_skills(skills: list, max_workers: int = 5) -> list:
    """并发检查所有 Skills 的更新状态"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_skill = {
            executor.submit(get_remote_hash, skill['source_url']): skill
            for skill in skills
            if skill.get('source_url')
        }
        results = []
        for future in concurrent.futures.as_completed(future_to_skill):
            skill = future_to_skill[future]
            try:
                remote_hash = future.result()
                skill['remote_hash'] = remote_hash
                skill['status'] = 'outdated' if remote_hash != skill.get('local_hash') else 'current'
            except Exception as e:
                skill['status'] = 'error'
                skill['message'] = str(e)
            results.append(skill)
        return results
```

### 4.3 YAML Frontmatter 解析

```python
import yaml
import re

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """解析 SKILL.md 的 YAML frontmatter"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    if match:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return frontmatter, body
    return {}, content
```

### 4.4 智能缝合

```python
import re

def stitch_evolution(skill_md_content: str, evolution_section: str) -> str:
    """将进化章节缝合到 SKILL.md"""
    section_pattern = r'## User-Learned Best Practices & Constraints.*?(?=\n## |\Z)'

    if re.search(section_pattern, skill_md_content, re.DOTALL):
        # 替换现有章节
        return re.sub(section_pattern, evolution_section, skill_md_content, flags=re.DOTALL)
    else:
        # 追加到末尾
        return skill_md_content.rstrip() + '\n\n' + evolution_section
```

---

## 五、验收标准

### 5.1 功能验收

| 功能 | 验收标准 |
|------|----------|
| skill-factory | 能从 GitHub URL 生成标准化 Skill 目录 |
| skill-manager check | 能并发检查所有 Skills 的更新状态 |
| skill-manager list | 能列出所有 Skills 及其元数据 |
| skill-manager delete | 能安全删除指定 Skill |
| skill-evolution | 能提取对话经验并持久化 |
| smart_stitch | 能将经验缝合到 SKILL.md |
| align_all | 能批量对齐所有 Skills 的经验 |

### 5.2 兼容性验收

- [ ] 现有 Skills 无需修改即可继续使用
- [ ] 扩展字段为可选，不影响基础功能
- [ ] 脚本支持 Python 3.8+

### 5.3 文档验收

- [ ] README 更新反映新功能
- [ ] CHANGELOG 记录版本变更
- [ ] 用户指南完整清晰

---

## 六、风险和缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| GitHub API 限制 | 批量检查可能触发限流 | 使用 git ls-remote 而非 API，添加延迟 |
| 网络不稳定 | 检查失败 | 添加重试机制，支持离线模式 |
| 元数据格式变更 | 兼容性问题 | 版本化元数据格式，向后兼容 |
| 经验数据冲突 | 合并错误 | 增量合并 + 去重 + 备份 |

---

## 七、时间线

| 阶段 | 任务 | 依赖 |
|------|------|------|
| Phase 1 | 元数据格式规范 | 无 |
| Phase 2 | skill-factory | Phase 1 |
| Phase 3 | skill-manager | Phase 1 |
| Phase 4 | skill-evolution | Phase 1 |
| Phase 5 | 轻量级脚本 | Phase 2-4 |
| Phase 6 | 文档更新 | Phase 2-5 |

---

## 八、参考资料

- [Khazix-Skills 项目](./Khazix-Skills-main/)
- [skill-creator 指南](../skills/skill-creator/SKILL.md)
- [Claude Code Skills 优先级指南](./Claude-Code-Skills-Priority-Guide.md)
