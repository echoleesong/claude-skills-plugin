#!/usr/bin/env python3
"""
smart_stitch.py - 智能缝合经验到 SKILL.md

读取 evolution.json 并将其内容转换为 Markdown，
自动插入或更新 SKILL.md 中的专用章节。

支持分层架构：
- 默认模式：仅读取 skill 目录下的 evolution.json
- 分层模式（--layered）：合并上游层、全局层、项目层的经验

用法:
    python smart_stitch.py <skill_dir>
    python smart_stitch.py <skill_dir> --dry-run
    python smart_stitch.py <skill_dir> --backup
    python smart_stitch.py <skill_dir> --layered --project /path/to/project

选项:
    --dry-run   仅显示将要生成的内容，不修改文件
    --backup    修改前备份原文件
    --layered   启用分层合并模式
    --project   项目路径（分层模式下使用，默认当前目录）
"""

import os
import sys
import re
import json
import datetime
import shutil
from pathlib import Path


# 章节标题（用于匹配和替换）
SECTION_TITLE = "## User-Learned Best Practices & Constraints"

# 章节开始的正则模式
SECTION_PATTERN = r'(\n+## User-Learned Best Practices & Constraints.*?)(?=\n## |\Z)'


def load_evolution(evolution_path: Path) -> dict:
    """加载 evolution.json"""
    if not evolution_path.exists():
        return {}
    try:
        return json.loads(evolution_path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, IOError):
        return {}


def load_layered_evolution(skill_name: str, project_path: str = None) -> dict:
    """
    使用分层合并器加载合并后的经验

    Args:
        skill_name: Skill 名称
        project_path: 项目路径

    Returns:
        dict: 合并后的经验数据
    """
    try:
        from layered_merge import LayeredEvolutionManager
        manager = LayeredEvolutionManager(skill_name, project_path)
        return manager.get_merged_evolution()
    except ImportError:
        print("警告: 无法导入 layered_merge 模块，回退到单层模式", file=sys.stderr)
        return {}


def generate_evolution_section(data: dict, layered: bool = False) -> str:
    """
    根据 evolution.json 生成 Markdown 章节

    Args:
        data: evolution.json 内容
        layered: 是否为分层模式

    Returns:
        str: Markdown 格式的章节内容
    """
    lines = [
        "",
        "",
        SECTION_TITLE,
        "",
    ]

    # 根据模式显示不同的提示
    if layered:
        meta = data.get("_meta", {})
        layers = meta.get("layers", {})
        active_layers = [k for k, v in layers.items() if isinstance(v, dict) and v.get("exists")]
        layers_info = ", ".join(active_layers) if active_layers else "none"
        lines.append(f"> **Auto-Generated Section**: 此章节由 skill-evolution 自动维护（分层模式: {layers_info}），请勿手动编辑。")
    else:
        lines.append("> **Auto-Generated Section**: 此章节由 skill-evolution 自动维护，请勿手动编辑。")

    lines.append("")

    # User Preferences
    if data.get("preferences"):
        lines.append("### User Preferences")
        lines.append("")
        for item in data["preferences"]:
            lines.append(f"- {item}")
        lines.append("")

    # Known Fixes & Workarounds
    if data.get("fixes"):
        lines.append("### Known Fixes & Workarounds")
        lines.append("")
        for item in data["fixes"]:
            lines.append(f"- {item}")
        lines.append("")

    # Context-Specific Notes
    if data.get("contexts"):
        lines.append("### Context-Specific Notes")
        lines.append("")
        for item in data["contexts"]:
            lines.append(f"- {item}")
        lines.append("")

    # Custom Instruction Injection
    if data.get("custom_prompts"):
        lines.append("### Custom Instruction Injection")
        lines.append("")
        lines.append(data["custom_prompts"])
        lines.append("")

    # 元信息
    if data.get("last_updated"):
        lines.append(f"*Last updated: {data['last_updated']}*")

    return "\n".join(lines)


def stitch_skill(skill_dir: str, dry_run: bool = False, backup: bool = False,
                  layered: bool = False, project_path: str = None) -> bool:
    """
    将 evolution.json 缝合到 SKILL.md

    Args:
        skill_dir: Skill 目录路径
        dry_run: 是否仅预览
        backup: 是否备份原文件
        layered: 是否启用分层合并模式
        project_path: 项目路径（分层模式下使用）

    Returns:
        bool: 是否成功
    """
    skill_path = Path(skill_dir)
    skill_md_path = skill_path / "SKILL.md"
    evolution_path = skill_path / "evolution.json"

    # 检查 SKILL.md
    if not skill_md_path.exists():
        print(f"错误: SKILL.md 不存在: {skill_md_path}", file=sys.stderr)
        return False

    # 加载数据
    if layered:
        # 分层模式：合并三层经验
        skill_name = skill_path.name
        data = load_layered_evolution(skill_name, project_path)
        if not data:
            # 回退到单层模式
            data = load_evolution(evolution_path)
    else:
        # 单层模式：仅读取本地 evolution.json
        if not evolution_path.exists():
            print(f"信息: 没有 evolution.json，跳过: {skill_path.name}")
            return True
        data = load_evolution(evolution_path)

    if not data:
        print(f"信息: evolution.json 为空，跳过: {skill_path.name}")
        return True

    # 检查是否有实际内容
    has_content = any(data.get(k) for k in ['preferences', 'fixes', 'contexts', 'custom_prompts'])
    if not has_content:
        print(f"信息: 没有可缝合的内容，跳过: {skill_path.name}")
        return True

    # 生成新章节
    evolution_section = generate_evolution_section(data, layered=layered)

    # 读取原始内容
    content = skill_md_path.read_text(encoding='utf-8')

    # 查找并替换或追加
    match = re.search(SECTION_PATTERN, content, re.DOTALL)

    if match:
        # 替换现有章节
        new_content = content[:match.start()] + evolution_section
        action = "更新"
    else:
        # 追加到末尾
        new_content = content.rstrip() + evolution_section
        action = "追加"

    if dry_run:
        print(f"[Dry Run] 将要{action}章节到: {skill_path.name}")
        print("-" * 40)
        print(evolution_section)
        print("-" * 40)
        return True

    # 备份
    if backup:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = skill_md_path.with_suffix(f'.md.bak.{timestamp}')
        shutil.copy2(skill_md_path, backup_path)
        print(f"已备份到: {backup_path}")

    # 写入
    skill_md_path.write_text(new_content, encoding='utf-8')
    print(f"✅ 已{action}经验章节: {skill_path.name}")

    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description='智能缝合经验到 SKILL.md')
    parser.add_argument('skill_dir', help='Skill 目录路径')
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不修改文件')
    parser.add_argument('--backup', '-b', action='store_true', help='修改前备份原文件')
    parser.add_argument('--layered', '-l', action='store_true', help='启用分层合并模式')
    parser.add_argument('--project', '-p', help='项目路径（分层模式下使用）', default=None)

    args = parser.parse_args()

    success = stitch_skill(
        args.skill_dir,
        dry_run=args.dry_run,
        backup=args.backup,
        layered=args.layered,
        project_path=args.project
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
