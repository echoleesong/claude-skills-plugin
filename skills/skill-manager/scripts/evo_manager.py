#!/usr/bin/env python3
"""
evo_manager.py - 经验层管理命令

为 skill-manager 提供经验层管理功能：
- evo-status: 查看经验分布状态
- promote: 将项目经验提升到全局层
- pull: 从全局层拉取经验到项目层
- sync: 同步所有 skills 的经验状态

用法:
    python evo_manager.py evo-status <skill_name> [--project <path>]
    python evo_manager.py promote <skill_name> [--project <path>] [--fields f1,f2]
    python evo_manager.py pull <skill_name> [--project <path>]
    python evo_manager.py sync [--skills-dir <path>] [--project <path>]
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional, List

# 添加 skill-evolution 的 scripts 目录到路径
SCRIPT_DIR = Path(__file__).parent
EVOLUTION_SCRIPTS = SCRIPT_DIR.parent.parent / "skill-evolution" / "scripts"
if EVOLUTION_SCRIPTS.exists():
    sys.path.insert(0, str(EVOLUTION_SCRIPTS))


def get_skills_dir() -> Path:
    """获取 skills 目录"""
    # 优先从环境变量获取
    if os.environ.get("SKILLS_DIR"):
        return Path(os.environ["SKILLS_DIR"])

    # 默认路径
    home = Path.home()
    default_paths = [
        home / ".claude" / "skills-repo" / "skills",
        home / ".claude" / "skills",
    ]

    for path in default_paths:
        if path.exists():
            return path

    return default_paths[0]


def list_all_skills(skills_dir: Path) -> List[str]:
    """列出所有 skills"""
    skills = []
    if skills_dir.exists():
        for item in skills_dir.iterdir():
            if item.is_dir() and (item / "SKILL.md").exists():
                skills.append(item.name)
    return sorted(skills)


def cmd_evo_status(skill_name: str, project_path: Optional[str] = None) -> dict:
    """查看经验分布状态"""
    try:
        from layered_merge import LayeredEvolutionManager
        manager = LayeredEvolutionManager(skill_name, project_path)
        return manager.get_status()
    except ImportError as e:
        return {"status": "error", "message": f"无法导入 layered_merge: {e}"}


def cmd_promote(skill_name: str, project_path: Optional[str] = None,
                fields: Optional[List[str]] = None) -> dict:
    """将项目经验提升到全局层"""
    try:
        from layered_merge import LayeredEvolutionManager
        manager = LayeredEvolutionManager(skill_name, project_path)
        return manager.promote_to_global(fields)
    except ImportError as e:
        return {"status": "error", "message": f"无法导入 layered_merge: {e}"}


def cmd_pull(skill_name: str, project_path: Optional[str] = None) -> dict:
    """从全局层拉取经验到项目层"""
    try:
        from layered_merge import LayeredEvolutionManager
        manager = LayeredEvolutionManager(skill_name, project_path)
        return manager.pull_from_global()
    except ImportError as e:
        return {"status": "error", "message": f"无法导入 layered_merge: {e}"}


def cmd_sync(skills_dir: Optional[str] = None, project_path: Optional[str] = None) -> dict:
    """同步所有 skills 的经验状态"""
    try:
        from layered_merge import LayeredEvolutionManager
    except ImportError as e:
        return {"status": "error", "message": f"无法导入 layered_merge: {e}"}

    skills_path = Path(skills_dir) if skills_dir else get_skills_dir()
    skills = list_all_skills(skills_path)

    if not skills:
        return {
            "status": "error",
            "message": f"在 {skills_path} 中没有找到任何 skills"
        }

    results = {
        "status": "success",
        "skills_dir": str(skills_path),
        "project_path": project_path or str(Path.cwd()),
        "total_skills": len(skills),
        "summary": {
            "has_upstream": 0,
            "has_global": 0,
            "has_project": 0,
            "no_evolution": 0
        },
        "skills": []
    }

    for skill_name in skills:
        manager = LayeredEvolutionManager(skill_name, project_path)
        status = manager.get_status()

        layers = status.get("layers", {})
        has_upstream = layers.get("upstream", {}).get("exists", False)
        has_global = layers.get("global", {}).get("exists", False)
        has_project = layers.get("project", {}).get("exists", False)

        if has_upstream:
            results["summary"]["has_upstream"] += 1
        if has_global:
            results["summary"]["has_global"] += 1
        if has_project:
            results["summary"]["has_project"] += 1
        if not (has_upstream or has_global or has_project):
            results["summary"]["no_evolution"] += 1

        results["skills"].append({
            "name": skill_name,
            "upstream": has_upstream,
            "global": has_global,
            "project": has_project,
            "merged_total": status.get("merged_total", 0)
        })

    return results


def format_status_output(status: dict) -> str:
    """格式化状态输出"""
    lines = []
    lines.append(f"Skill: {status.get('skill_name')}")
    lines.append(f"Project: {status.get('project_path')}")
    lines.append("")
    lines.append("Layers:")

    for layer_name in ["upstream", "global", "project"]:
        layer = status.get("layers", {}).get(layer_name, {})
        exists = "✓" if layer.get("exists") else "✗"
        path = layer.get("path", "N/A")

        lines.append(f"  [{exists}] {layer_name.capitalize()}")
        lines.append(f"      Path: {path}")

        if layer.get("exists") and layer.get("counts"):
            counts = layer["counts"]
            lines.append(f"      Items: {counts.get('total', 0)} total")
            lines.append(f"        - preferences: {counts.get('preferences', 0)}")
            lines.append(f"        - fixes: {counts.get('fixes', 0)}")
            lines.append(f"        - contexts: {counts.get('contexts', 0)}")
            if counts.get("has_custom_prompts"):
                lines.append(f"        - custom_prompts: yes")

    lines.append("")
    lines.append(f"Merged Total: {status.get('merged_total', 0)} items")

    return "\n".join(lines)


def format_sync_output(result: dict) -> str:
    """格式化同步输出"""
    lines = []
    lines.append("=" * 60)
    lines.append("Skills Evolution Status Summary")
    lines.append("=" * 60)
    lines.append(f"Skills Directory: {result.get('skills_dir')}")
    lines.append(f"Project Path: {result.get('project_path')}")
    lines.append(f"Total Skills: {result.get('total_skills')}")
    lines.append("")

    summary = result.get("summary", {})
    lines.append("Summary:")
    lines.append(f"  - Has upstream evolution: {summary.get('has_upstream', 0)}")
    lines.append(f"  - Has global evolution: {summary.get('has_global', 0)}")
    lines.append(f"  - Has project evolution: {summary.get('has_project', 0)}")
    lines.append(f"  - No evolution data: {summary.get('no_evolution', 0)}")
    lines.append("")

    lines.append("Skills Detail:")
    lines.append("-" * 60)
    lines.append(f"{'Name':<30} {'Up':>4} {'Glb':>4} {'Prj':>4} {'Total':>6}")
    lines.append("-" * 60)

    for skill in result.get("skills", []):
        up = "✓" if skill.get("upstream") else "-"
        glb = "✓" if skill.get("global") else "-"
        prj = "✓" if skill.get("project") else "-"
        total = skill.get("merged_total", 0)
        lines.append(f"{skill['name']:<30} {up:>4} {glb:>4} {prj:>4} {total:>6}")

    lines.append("-" * 60)

    return "\n".join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='经验层管理命令',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # evo-status 命令
    status_parser = subparsers.add_parser('evo-status', help='查看经验分布状态')
    status_parser.add_argument('skill_name', help='Skill 名称')
    status_parser.add_argument('--project', '-p', help='项目路径', default=None)
    status_parser.add_argument('--json', '-j', action='store_true', help='JSON 输出')

    # promote 命令
    promote_parser = subparsers.add_parser('promote', help='将项目经验提升到全局层')
    promote_parser.add_argument('skill_name', help='Skill 名称')
    promote_parser.add_argument('--project', '-p', help='项目路径', default=None)
    promote_parser.add_argument('--fields', '-f', help='要提升的字段（逗号分隔）', default=None)
    promote_parser.add_argument('--json', '-j', action='store_true', help='JSON 输出')

    # pull 命令
    pull_parser = subparsers.add_parser('pull', help='从全局层拉取经验到项目层')
    pull_parser.add_argument('skill_name', help='Skill 名称')
    pull_parser.add_argument('--project', '-p', help='项目路径', default=None)
    pull_parser.add_argument('--json', '-j', action='store_true', help='JSON 输出')

    # sync 命令
    sync_parser = subparsers.add_parser('sync', help='同步所有 skills 的经验状态')
    sync_parser.add_argument('--skills-dir', '-s', help='Skills 目录', default=None)
    sync_parser.add_argument('--project', '-p', help='项目路径', default=None)
    sync_parser.add_argument('--json', '-j', action='store_true', help='JSON 输出')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 执行命令
    if args.command == 'evo-status':
        result = cmd_evo_status(args.skill_name, args.project)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_status_output(result))

    elif args.command == 'promote':
        fields = args.fields.split(',') if args.fields else None
        result = cmd_promote(args.skill_name, args.project, fields)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if result.get("status") == "success":
                items = result.get("items", [])
                if items:
                    print(f"✅ 已提升 {len(items)} 条经验到全局层")
                    for item in items:
                        print(f"   - [{item.get('field')}] {item.get('item', item.get('action', ''))}")
                else:
                    print(result.get("message", "没有新的经验需要提升"))
            else:
                print(f"❌ 错误: {result.get('message')}")

    elif args.command == 'pull':
        result = cmd_pull(args.skill_name, args.project)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if result.get("status") == "success":
                items = result.get("items", [])
                if items:
                    print(f"✅ 已拉取 {len(items)} 条经验到项目层")
                    for item in items:
                        print(f"   - [{item.get('field')}] {item.get('item', item.get('action', ''))}")
                else:
                    print(result.get("message", "没有新的经验需要拉取"))
            else:
                print(f"❌ 错误: {result.get('message')}")

    elif args.command == 'sync':
        result = cmd_sync(args.skills_dir, args.project)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if result.get("status") == "success":
                print(format_sync_output(result))
            else:
                print(f"❌ 错误: {result.get('message')}")

    # 设置退出码
    if isinstance(result, dict) and result.get("status") == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()
