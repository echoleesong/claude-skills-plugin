#!/usr/bin/env python3
"""
check_updates.py - 批量检查 Skills 更新状态

独立可执行脚本，用于 CI/CD 或命令行批量检查。

用法:
    python scripts/check_updates.py [options]

示例:
    # 检查默认 skills 目录
    python scripts/check_updates.py

    # 指定目录并输出 JSON
    python scripts/check_updates.py --skills-dir ./skills --json

    # 只显示需要更新的
    python scripts/check_updates.py --outdated-only

    # 输出到文件（CI/CD 用）
    python scripts/check_updates.py --json --output report.json
"""

import os
import sys
import re
import json
import subprocess
import concurrent.futures
import argparse
from pathlib import Path
from typing import Optional, List, Dict

# 默认 Skills 目录（相对于脚本位置）
DEFAULT_SKILLS_DIR = Path(__file__).parent.parent / "skills"


def parse_frontmatter(content: str) -> dict:
    """简单解析 YAML frontmatter"""
    pattern = r'^---\s*\n(.*?)\n---'
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}

    result = {}
    for line in match.group(1).split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip().strip('"\'')
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            result[key] = value
    return result


def get_remote_hash(url: str, timeout: int = 15) -> Optional[str]:
    """获取远程 HEAD hash"""
    try:
        result = subprocess.run(
            ['git', 'ls-remote', url, 'HEAD'],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.split()[0]
    except Exception:
        pass
    return None


def scan_skills(skills_dir: Path) -> List[Dict]:
    """扫描 Skills 目录"""
    skills = []

    if not skills_dir.exists():
        return skills

    for item in sorted(skills_dir.iterdir()):
        if not item.is_dir() or item.name.startswith('.'):
            continue

        skill_md = item / "SKILL.md"
        if not skill_md.exists():
            continue

        try:
            content = skill_md.read_text(encoding='utf-8')
            fm = parse_frontmatter(content)

            source_url = fm.get('source_url') or fm.get('github_url', '')
            local_hash = fm.get('source_hash') or fm.get('github_hash', '')

            skills.append({
                "name": fm.get('name', item.name),
                "dir": str(item),
                "version": fm.get('version', ''),
                "source_url": source_url,
                "local_hash": local_hash,
            })
        except Exception:
            pass

    return skills


def check_updates(skills: List[Dict], max_workers: int = 5) -> List[Dict]:
    """并发检查更新"""
    results = []
    managed = [s for s in skills if s.get('source_url')]
    unmanaged = [s for s in skills if not s.get('source_url')]

    for s in unmanaged:
        s['status'] = 'unmanaged'
        s['remote_hash'] = ''
        results.append(s)

    if managed:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {
                executor.submit(get_remote_hash, s['source_url']): s
                for s in managed
            }
            for future in concurrent.futures.as_completed(future_map):
                skill = future_map[future]
                remote = future.result()
                skill['remote_hash'] = remote or ''

                if not remote:
                    skill['status'] = 'error'
                elif not skill['local_hash']:
                    skill['status'] = 'unknown'
                elif remote != skill['local_hash']:
                    skill['status'] = 'outdated'
                else:
                    skill['status'] = 'current'

                results.append(skill)

    return results


def format_table(results: List[Dict]) -> str:
    """格式化表格"""
    lines = [
        f"{'Name':<25} | {'Status':<10} | {'Version':<10} | {'Source URL':<40}",
        "-" * 90
    ]
    for r in sorted(results, key=lambda x: (x['status'] != 'outdated', x['name'])):
        name = r['name'][:24]
        status = r['status'][:9]
        version = (r.get('version') or 'N/A')[:9]
        url = (r.get('source_url') or 'N/A')[:39]
        lines.append(f"{name:<25} | {status:<10} | {version:<10} | {url:<40}")
    return '\n'.join(lines)


def format_summary(results: List[Dict]) -> str:
    """格式化摘要"""
    total = len(results)
    outdated = [r for r in results if r['status'] == 'outdated']
    current = [r for r in results if r['status'] == 'current']
    unmanaged = [r for r in results if r['status'] == 'unmanaged']
    errors = [r for r in results if r['status'] == 'error']

    lines = [
        "Skills Update Check Report",
        "=" * 40,
        f"Total: {total}",
        f"  Current: {len(current)}",
        f"  Outdated: {len(outdated)}",
        f"  Unmanaged: {len(unmanaged)}",
        f"  Errors: {len(errors)}",
    ]

    if outdated:
        lines.append("")
        lines.append("Outdated Skills:")
        for r in outdated:
            lines.append(f"  - {r['name']}")
            lines.append(f"    Local:  {r['local_hash'][:12]}...")
            lines.append(f"    Remote: {r['remote_hash'][:12]}...")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='批量检查 Skills 更新状态',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python check_updates.py                        # 检查默认目录
  python check_updates.py --skills-dir ./skills  # 指定目录
  python check_updates.py --json --output r.json # 输出到文件
  python check_updates.py --outdated-only        # 只显示需更新的
        """
    )
    parser.add_argument(
        '--skills-dir', '-d',
        type=Path,
        default=DEFAULT_SKILLS_DIR,
        help=f'Skills 目录 (默认: {DEFAULT_SKILLS_DIR})'
    )
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--summary', '-s', action='store_true', help='输出摘要格式')
    parser.add_argument('--outdated-only', action='store_true', help='只显示需要更新的')
    parser.add_argument('--output', '-o', type=Path, help='输出到文件')
    parser.add_argument('--workers', '-w', type=int, default=5, help='并发数 (默认: 5)')

    args = parser.parse_args()

    # 扫描
    skills = scan_skills(args.skills_dir)
    if not skills:
        print(f"未找到 Skills: {args.skills_dir}", file=sys.stderr)
        sys.exit(1)

    # 检查
    results = check_updates(skills, max_workers=args.workers)

    # 过滤
    if args.outdated_only:
        results = [r for r in results if r['status'] == 'outdated']

    # 格式化输出
    if args.json:
        output = json.dumps(results, indent=2, ensure_ascii=False)
    elif args.summary:
        output = format_summary(results)
    else:
        output = format_table(results)

    # 输出
    if args.output:
        args.output.write_text(output, encoding='utf-8')
        print(f"已保存到: {args.output}")
    else:
        print(output)

    # 退出码：有 outdated 则返回 1（便于 CI/CD 判断）
    outdated_count = sum(1 for r in results if r['status'] == 'outdated')
    sys.exit(1 if outdated_count > 0 else 0)


if __name__ == "__main__":
    main()
