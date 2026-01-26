#!/usr/bin/env python3
"""
config.py - Skill Manager 配置管理

管理 skill-manager 的配置，包括默认 Skills 目录路径。

用法:
    python config.py get              # 获取当前配置
    python config.py set <skills_dir> # 设置 Skills 目录
    python config.py detect           # 自动检测 Skills 目录
    python config.py clear            # 清除配置
"""

from __future__ import annotations

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# 配置文件路径（与此脚本同级目录的上一级）
CONFIG_FILE = Path(__file__).parent.parent / "config.json"

# 默认搜索路径（按优先级排序）
DEFAULT_SEARCH_PATHS = [
    "~/.claude/skills",
    "~/skills",
    "~/.config/claude/skills",
]


def load_config() -> dict:
    """加载配置文件"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_config(config: dict) -> bool:
    """保存配置文件"""
    try:
        config['updated_at'] = datetime.now().isoformat()
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"错误: 无法保存配置: {e}", file=sys.stderr)
        return False


def get_skills_dir() -> Optional[str]:
    """获取已配置的 Skills 目录"""
    config = load_config()
    skills_dir = config.get('skills_dir')
    if skills_dir and Path(skills_dir).expanduser().exists():
        return str(Path(skills_dir).expanduser())
    return None


def set_skills_dir(path: str) -> bool:
    """设置 Skills 目录"""
    expanded_path = Path(path).expanduser().resolve()

    if not expanded_path.exists():
        print(f"错误: 目录不存在: {expanded_path}", file=sys.stderr)
        return False

    if not expanded_path.is_dir():
        print(f"错误: 路径不是目录: {expanded_path}", file=sys.stderr)
        return False

    config = load_config()
    config['skills_dir'] = str(expanded_path)
    config['configured_at'] = datetime.now().isoformat()

    if save_config(config):
        print(f"已设置 Skills 目录: {expanded_path}")
        return True
    return False


def detect_skills_dir() -> Optional[str]:
    """自动检测 Skills 目录"""
    for search_path in DEFAULT_SEARCH_PATHS:
        expanded = Path(search_path).expanduser()
        if expanded.exists() and expanded.is_dir():
            # 验证是否包含有效的 Skills（至少有一个 SKILL.md）
            has_skills = any(
                (item / "SKILL.md").exists()
                for item in expanded.iterdir()
                if item.is_dir() and not item.name.startswith('.')
            )
            if has_skills:
                return str(expanded)
    return None


def clear_config() -> bool:
    """清除配置"""
    if CONFIG_FILE.exists():
        try:
            CONFIG_FILE.unlink()
            print("配置已清除")
            return True
        except IOError as e:
            print(f"错误: 无法删除配置文件: {e}", file=sys.stderr)
            return False
    print("配置文件不存在")
    return True


def print_config():
    """打印当前配置"""
    config = load_config()
    if config:
        print(json.dumps(config, indent=2, ensure_ascii=False))
    else:
        print("未配置")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Skill Manager 配置管理')
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # get 命令
    subparsers.add_parser('get', help='获取当前配置')

    # set 命令
    set_parser = subparsers.add_parser('set', help='设置 Skills 目录')
    set_parser.add_argument('skills_dir', help='Skills 目录路径')

    # detect 命令
    subparsers.add_parser('detect', help='自动检测 Skills 目录')

    # clear 命令
    subparsers.add_parser('clear', help='清除配置')

    args = parser.parse_args()

    if args.command == 'get':
        print_config()
    elif args.command == 'set':
        success = set_skills_dir(args.skills_dir)
        sys.exit(0 if success else 1)
    elif args.command == 'detect':
        detected = detect_skills_dir()
        if detected:
            print(f"检测到 Skills 目录: {detected}")
            # 自动保存
            set_skills_dir(detected)
        else:
            print("未检测到 Skills 目录", file=sys.stderr)
            print(f"已搜索: {', '.join(DEFAULT_SEARCH_PATHS)}", file=sys.stderr)
            sys.exit(1)
    elif args.command == 'clear':
        success = clear_config()
        sys.exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
