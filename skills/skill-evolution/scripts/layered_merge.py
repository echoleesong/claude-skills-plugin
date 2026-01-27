#!/usr/bin/env python3
"""
layered_merge.py - 分层经验合并器

支持三层架构：上游层 → 全局层 → 项目层

三层架构说明:
- 上游层 (Upstream): skills-repo 原始仓库的经验，来自社区/原作者
- 全局层 (Global): ~/.claude/evolutions/<skill>/evolution.json，个人通用经验
- 项目层 (Project): <project>/.claude/evolutions/<skill>.json，项目特定经验

用法:
    python layered_merge.py status <skill_name> [--project <path>]
    python layered_merge.py merge <skill_name> [--project <path>]
    python layered_merge.py promote <skill_name> [--project <path>] [--fields f1,f2]
    python layered_merge.py pull <skill_name> [--project <path>]
    python layered_merge.py save <skill_name> <layer> '<json>' [--project <path>]
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class LayeredEvolutionManager:
    """分层经验管理器"""

    def __init__(self, skill_name: str, project_path: Optional[str] = None):
        self.skill_name = skill_name
        self.project_path = Path(project_path).resolve() if project_path else Path.cwd()

        # 路径配置
        self.home = Path.home()
        self.claude_dir = self.home / ".claude"

        # 加载配置
        self.config = self._load_config()

        # 解析路径
        self.skills_repo = Path(os.path.expanduser(
            self.config.get("skills_repo_path", "~/.claude/skills-repo")
        )) / "skills"

        self.global_evolutions = Path(os.path.expanduser(
            self.config.get("global_evolutions_path", "~/.claude/evolutions")
        ))

        self.project_evolutions_dir = self.config.get("project_evolutions_dir", ".claude/evolutions")
        self.project_evolutions = self.project_path / self.project_evolutions_dir

    def _load_config(self) -> dict:
        """加载全局配置"""
        config_path = self.claude_dir / "evolutions" / "config.json"
        if config_path.exists():
            try:
                return json.loads(config_path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, IOError):
                pass
        return {}

    def _load_json(self, path: Path) -> dict:
        """安全加载 JSON 文件"""
        if path.exists():
            try:
                return json.loads(path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_json(self, path: Path, data: dict) -> bool:
        """保存 JSON 文件"""
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            return True
        except IOError as e:
            print(f"错误: 无法写入文件 {path}: {e}", file=sys.stderr)
            return False

    def _dedupe_list(self, items: list) -> list:
        """列表去重（保持顺序）"""
        seen = set()
        result = []
        for item in items:
            normalized = item.strip() if isinstance(item, str) else str(item)
            if normalized not in seen:
                seen.add(normalized)
                result.append(item)
        return result

    # ==================== 路径获取 ====================

    def get_upstream_path(self) -> Path:
        """获取上游层 evolution.json 路径"""
        return self.skills_repo / self.skill_name / "evolution.json"

    def get_global_path(self) -> Path:
        """获取全局层 evolution.json 路径"""
        return self.global_evolutions / self.skill_name / "evolution.json"

    def get_project_path(self) -> Path:
        """获取项目层 evolution.json 路径"""
        return self.project_evolutions / f"{self.skill_name}.json"

    # ==================== 数据获取 ====================

    def get_upstream_evolution(self) -> dict:
        """获取上游层经验（来自 skills-repo）"""
        return self._load_json(self.get_upstream_path())

    def get_global_evolution(self) -> dict:
        """获取全局层经验"""
        return self._load_json(self.get_global_path())

    def get_project_evolution(self) -> dict:
        """获取项目层经验"""
        return self._load_json(self.get_project_path())

    # ==================== 核心功能 ====================

    def get_merged_evolution(self) -> dict:
        """
        合并三层经验，返回最终结果

        合并策略:
        - preferences, fixes, contexts: 追加去重
        - custom_prompts: 项目层 > 全局层 > 上游层（覆盖）
        """
        upstream = self.get_upstream_evolution()
        global_evo = self.get_global_evolution()
        project = self.get_project_evolution()

        merged = {
            "preferences": [],
            "fixes": [],
            "contexts": [],
            "custom_prompts": "",
            "_meta": {
                "merged_at": datetime.now().isoformat(),
                "skill_name": self.skill_name,
                "project_path": str(self.project_path),
                "layers": {
                    "upstream": {
                        "exists": bool(upstream),
                        "path": str(self.get_upstream_path())
                    },
                    "global": {
                        "exists": bool(global_evo),
                        "path": str(self.get_global_path())
                    },
                    "project": {
                        "exists": bool(project),
                        "path": str(self.get_project_path())
                    }
                }
            }
        }

        # 按优先级合并列表字段（去重）
        for field in ["preferences", "fixes", "contexts"]:
            items = []
            # 按优先级顺序：上游 → 全局 → 项目
            for layer in [upstream, global_evo, project]:
                items.extend(layer.get(field, []))
            merged[field] = self._dedupe_list(items)

        # custom_prompts: 项目层覆盖
        merged["custom_prompts"] = (
            project.get("custom_prompts") or
            global_evo.get("custom_prompts") or
            upstream.get("custom_prompts") or
            ""
        )

        return merged

    def save_to_layer(self, layer: str, data: dict) -> dict:
        """
        保存经验到指定层

        Args:
            layer: "global" 或 "project"
            data: 要保存的数据

        Returns:
            dict: 操作结果
        """
        if layer == "global":
            path = self.get_global_path()
        elif layer == "project":
            path = self.get_project_path()
        elif layer == "upstream":
            return {
                "status": "error",
                "message": "不能直接写入上游层，请通过 PR 提交到原仓库"
            }
        else:
            return {
                "status": "error",
                "message": f"无效的层级: {layer}，请使用 'global' 或 'project'"
            }

        # 加载现有数据并合并
        existing = self._load_json(path)

        # 合并列表字段
        for field in ["preferences", "fixes", "contexts"]:
            if field in data:
                existing_items = existing.get(field, [])
                new_items = data[field] if isinstance(data[field], list) else [data[field]]
                existing[field] = self._dedupe_list(existing_items + new_items)

        # 覆盖 custom_prompts
        if "custom_prompts" in data and data["custom_prompts"]:
            existing["custom_prompts"] = data["custom_prompts"]

        # 更新时间戳
        existing["last_updated"] = datetime.now().isoformat()

        if self._save_json(path, existing):
            return {
                "status": "success",
                "layer": layer,
                "path": str(path),
                "data": existing
            }
        else:
            return {
                "status": "error",
                "message": f"无法保存到 {path}"
            }

    def promote_to_global(self, fields: Optional[List[str]] = None) -> dict:
        """
        将项目层经验提升到全局层

        Args:
            fields: 要提升的字段列表，默认全部

        Returns:
            dict: 操作结果
        """
        project = self.get_project_evolution()
        global_evo = self.get_global_evolution()

        if not project:
            return {
                "status": "error",
                "message": f"项目层没有 {self.skill_name} 的经验数据",
                "path": str(self.get_project_path())
            }

        fields = fields or ["preferences", "fixes", "contexts", "custom_prompts"]
        promoted = {
            "status": "success",
            "items": [],
            "from_layer": "project",
            "to_layer": "global"
        }

        for field in fields:
            if field == "custom_prompts":
                if project.get("custom_prompts") and not global_evo.get("custom_prompts"):
                    global_evo["custom_prompts"] = project["custom_prompts"]
                    promoted["items"].append({
                        "field": "custom_prompts",
                        "action": "set"
                    })
            else:
                project_items = project.get(field, [])
                global_items = global_evo.get(field, [])

                for item in project_items:
                    normalized = item.strip() if isinstance(item, str) else str(item)
                    global_normalized = [
                        x.strip() if isinstance(x, str) else str(x)
                        for x in global_items
                    ]
                    if normalized not in global_normalized:
                        global_items.append(item)
                        promoted["items"].append({
                            "field": field,
                            "item": item
                        })

                global_evo[field] = global_items

        if promoted["items"]:
            global_evo["last_updated"] = datetime.now().isoformat()
            if self._save_json(self.get_global_path(), global_evo):
                promoted["path"] = str(self.get_global_path())
                promoted["total_promoted"] = len(promoted["items"])
            else:
                return {
                    "status": "error",
                    "message": "无法保存到全局层"
                }
        else:
            promoted["message"] = "没有新的经验需要提升（可能已存在于全局层）"

        return promoted

    def pull_from_global(self) -> dict:
        """
        从全局层拉取经验到项目层

        Returns:
            dict: 操作结果
        """
        global_evo = self.get_global_evolution()
        project = self.get_project_evolution()

        if not global_evo:
            return {
                "status": "error",
                "message": f"全局层没有 {self.skill_name} 的经验数据",
                "path": str(self.get_global_path())
            }

        pulled = {
            "status": "success",
            "items": [],
            "from_layer": "global",
            "to_layer": "project"
        }

        # 合并列表字段
        for field in ["preferences", "fixes", "contexts"]:
            global_items = global_evo.get(field, [])
            project_items = project.get(field, [])

            for item in global_items:
                normalized = item.strip() if isinstance(item, str) else str(item)
                project_normalized = [
                    x.strip() if isinstance(x, str) else str(x)
                    for x in project_items
                ]
                if normalized not in project_normalized:
                    project_items.append(item)
                    pulled["items"].append({
                        "field": field,
                        "item": item
                    })

            project[field] = project_items

        # custom_prompts: 仅当项目层为空时拉取
        if not project.get("custom_prompts") and global_evo.get("custom_prompts"):
            project["custom_prompts"] = global_evo["custom_prompts"]
            pulled["items"].append({
                "field": "custom_prompts",
                "action": "set"
            })

        if pulled["items"]:
            project["last_updated"] = datetime.now().isoformat()
            project["pulled_from_global_at"] = datetime.now().isoformat()
            if self._save_json(self.get_project_path(), project):
                pulled["path"] = str(self.get_project_path())
                pulled["total_pulled"] = len(pulled["items"])
            else:
                return {
                    "status": "error",
                    "message": "无法保存到项目层"
                }
        else:
            pulled["message"] = "没有新的经验需要拉取（可能已存在于项目层）"

        return pulled

    def get_status(self) -> dict:
        """
        获取经验分布状态

        Returns:
            dict: 状态信息
        """
        upstream = self.get_upstream_evolution()
        global_evo = self.get_global_evolution()
        project = self.get_project_evolution()

        def count_items(data: dict) -> dict:
            return {
                "preferences": len(data.get("preferences", [])),
                "fixes": len(data.get("fixes", [])),
                "contexts": len(data.get("contexts", [])),
                "has_custom_prompts": bool(data.get("custom_prompts")),
                "total": sum(len(data.get(k, [])) for k in ["preferences", "fixes", "contexts"])
            }

        return {
            "skill_name": self.skill_name,
            "project_path": str(self.project_path),
            "layers": {
                "upstream": {
                    "exists": bool(upstream),
                    "path": str(self.get_upstream_path()),
                    "counts": count_items(upstream) if upstream else None,
                    "last_updated": upstream.get("last_updated")
                },
                "global": {
                    "exists": bool(global_evo),
                    "path": str(self.get_global_path()),
                    "counts": count_items(global_evo) if global_evo else None,
                    "last_updated": global_evo.get("last_updated")
                },
                "project": {
                    "exists": bool(project),
                    "path": str(self.get_project_path()),
                    "counts": count_items(project) if project else None,
                    "last_updated": project.get("last_updated")
                }
            },
            "merged_total": sum(
                len(self.get_merged_evolution().get(k, []))
                for k in ["preferences", "fixes", "contexts"]
            )
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='分层经验管理器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 查看经验状态
  python layered_merge.py status n8n-code-javascript

  # 合并三层经验
  python layered_merge.py merge n8n-code-javascript

  # 将项目经验提升到全局
  python layered_merge.py promote n8n-code-javascript

  # 从全局拉取经验到项目
  python layered_merge.py pull n8n-code-javascript

  # 保存经验到指定层
  python layered_merge.py save n8n-code-javascript global '{"preferences": ["偏好1"]}'
        """
    )

    parser.add_argument(
        'action',
        choices=['status', 'merge', 'promote', 'pull', 'save'],
        help='操作类型'
    )
    parser.add_argument(
        'skill_name',
        help='Skill 名称'
    )
    parser.add_argument(
        'extra_args',
        nargs='*',
        help='额外参数（save 命令需要 layer 和 json_data）'
    )
    parser.add_argument(
        '--project', '-p',
        help='项目路径（默认当前目录）',
        default=None
    )
    parser.add_argument(
        '--fields', '-f',
        help='要操作的字段（逗号分隔）',
        default=None
    )
    parser.add_argument(
        '--json', '-j',
        action='store_true',
        help='JSON 格式输出'
    )

    args = parser.parse_args()

    manager = LayeredEvolutionManager(args.skill_name, args.project)

    if args.action == 'status':
        result = manager.get_status()

    elif args.action == 'merge':
        result = manager.get_merged_evolution()

    elif args.action == 'promote':
        fields = args.fields.split(',') if args.fields else None
        result = manager.promote_to_global(fields)

    elif args.action == 'pull':
        result = manager.pull_from_global()

    elif args.action == 'save':
        if len(args.extra_args) < 2:
            print("错误: save 命令需要 layer 和 json_data 参数", file=sys.stderr)
            print("用法: python layered_merge.py save <skill_name> <layer> '<json_data>'", file=sys.stderr)
            sys.exit(1)

        layer = args.extra_args[0]
        json_str = args.extra_args[1]

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"错误: 无法解析 JSON: {e}", file=sys.stderr)
            sys.exit(1)

        result = manager.save_to_layer(layer, data)

    # 输出结果
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 根据结果设置退出码
    if isinstance(result, dict) and result.get("status") == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()
