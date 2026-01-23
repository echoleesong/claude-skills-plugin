#!/usr/bin/env python3
"""
batch_evolve.py - 批量对齐所有 Skills 的经验

独立可执行脚本，用于 CI/CD 或命令行批量对齐 evolution.json。

用法:
    python scripts/batch_evolve.py [options]

示例:
    # 对齐默认 skills 目录
    python scripts/batch_evolve.py

    # 指定目录
    python scripts/batch_evolve.py --skills-dir ./skills

    # 预览模式
    python scripts/batch_evolve.py --dry-run

    # 备份原文件
    python scripts/batch_evolve.py --backup
"""

import os
import sys
import re
import json
import argparse
import datetime
import shutil
from pathlib import Path
from typing import List, Dict, Tuple

# 默认 Skills 目录
DEFAULT_SKILLS_DIR = Path(__file__).parent.parent / "skills"

# 章节标题
SECTION_TITLE = "## User-Learned Best Practices & Constraints"
SECTION_PATTERN = r'(\n+## User-Learned Best Practices & Constraints.*?)(?=\n## |\Z)'


def find_skills_with_evolution(skills_dir: Path) -> List[Path]:
    """查找包含 evolution.json 的 Skills"""
    result = []
    if not skills_dir.exists():
        return result

    for item in sorted(skills_dir.iterdir()):
        if not item.is_dir() or item.name.startswith('.'):
            continue
        if (item / "evolution.json").exists() and (item / "SKILL.md").exists():
            result.append(item)

    return result


def generate_section(data: dict) -> str:
    """生成经验章节 Markdown"""
    lines = ["", "", SECTION_TITLE, "",
             "> **Auto-Generated Section**: 此章节由 skill-evolution 自动维护。", ""]

    if data.get("preferences"):
        lines.extend(["### User Preferences", ""])
        lines.extend(f"- {item}" for item in data["preferences"])
        lines.append("")

    if data.get("fixes"):
        lines.extend(["### Known Fixes & Workarounds", ""])
        lines.extend(f"- {item}" for item in data["fixes"])
        lines.append("")

    if data.get("contexts"):
        lines.extend(["### Context-Specific Notes", ""])
        lines.extend(f"- {item}" for item in data["contexts"])
        lines.append("")

    if data.get("custom_prompts"):
        lines.extend(["### Custom Instruction Injection", "", data["custom_prompts"], ""])

    if data.get("last_updated"):
        lines.append(f"*Last updated: {data['last_updated']}*")

    return "\n".join(lines)


def stitch_skill(skill_dir: Path, dry_run: bool = False, backup: bool = False) -> Tuple[bool, str]:
    """缝合单个 Skill"""
    skill_md = skill_dir / "SKILL.md"
    evolution_json = skill_dir / "evolution.json"

    try:
        data = json.loads(evolution_json.read_text(encoding='utf-8'))
    except Exception as e:
        return False, f"无法读取 evolution.json: {e}"

    if not any(data.get(k) for k in ['preferences', 'fixes', 'contexts', 'custom_prompts']):
        return True, "无内容，跳过"

    section = generate_section(data)
    content = skill_md.read_text(encoding='utf-8')

    match = re.search(SECTION_PATTERN, content, re.DOTALL)
    if match:
        new_content = content[:match.start()] + section
        action = "更新"
    else:
        new_content = content.rstrip() + section
        action = "追加"

    if dry_run:
        return True, f"[Dry Run] 将{action}章节"

    if backup:
        ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        shutil.copy2(skill_md, skill_md.with_suffix(f'.md.bak.{ts}'))

    skill_md.write_text(new_content, encoding='utf-8')
    return True, f"已{action}章节"


def batch_evolve(skills_dir: Path, dry_run: bool = False, backup: bool = False) -> Dict:
    """批量对齐"""
    skills = find_skills_with_evolution(skills_dir)

    if not skills:
        print("没有找到包含 evolution.json 的 Skills")
        return {"total": 0, "success": 0, "failed": 0}

    print(f"找到 {len(skills)} 个需要对齐的 Skills")
    if dry_run:
        print("[Dry Run 模式]")
    print("-" * 40)

    stats = {"total": len(skills), "success": 0, "failed": 0}
    failed = []

    for skill_dir in skills:
        name = skill_dir.name
        success, msg = stitch_skill(skill_dir, dry_run=dry_run, backup=backup)

        if success:
            stats["success"] += 1
            print(f"✅ {name}: {msg}")
        else:
            stats["failed"] += 1
            failed.append((name, msg))
            print(f"❌ {name}: {msg}")

    print("-" * 40)
    print(f"完成: {stats['success']}/{stats['total']} 成功")

    if failed:
        print("\n失败:")
        for name, msg in failed:
            print(f"  - {name}: {msg}")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='批量对齐所有 Skills 的经验',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--skills-dir', '-d',
        type=Path,
        default=DEFAULT_SKILLS_DIR,
        help=f'Skills 目录 (默认: {DEFAULT_SKILLS_DIR})'
    )
    parser.add_argument('--dry-run', action='store_true', help='预览模式')
    parser.add_argument('--backup', '-b', action='store_true', help='备份原文件')

    args = parser.parse_args()

    stats = batch_evolve(args.skills_dir, dry_run=args.dry_run, backup=args.backup)
    sys.exit(1 if stats["failed"] > 0 else 0)


if __name__ == "__main__":
    main()
