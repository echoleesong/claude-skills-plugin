#!/usr/bin/env python3
"""
validate_all.py - 批量验证 Skills 元数据

独立可执行脚本，用于 CI/CD 或命令行批量验证 SKILL.md 格式。

用法:
    python scripts/validate_all.py [options]

示例:
    # 验证默认 skills 目录
    python scripts/validate_all.py

    # 指定目录
    python scripts/validate_all.py --skills-dir ./skills

    # 输出 JSON 格式
    python scripts/validate_all.py --json

    # 严格模式（检查扩展字段）
    python scripts/validate_all.py --strict
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# 默认 Skills 目录
DEFAULT_SKILLS_DIR = Path(__file__).parent.parent / "skills"


def parse_frontmatter(content: str) -> Tuple[Optional[dict], str]:
    """解析 YAML frontmatter，返回 (frontmatter, body)"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None, content

    yaml_content = match.group(1)
    body = match.group(2)
    result = {}

    current_key = None
    current_list = None

    for line in yaml_content.split('\n'):
        stripped = line.strip()

        if not stripped or stripped.startswith('#'):
            continue

        # 检查是否是列表项
        if stripped.startswith('- ') and current_key:
            if current_list is None:
                current_list = []
            current_list.append(stripped[2:].strip())
            result[current_key] = current_list
            continue

        if ':' in stripped:
            # 保存之前的列表
            current_list = None

            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()

            current_key = key

            if value:
                # 移除引号
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]

                # 布尔值
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False

                result[key] = value
            else:
                # 可能是列表的开始
                current_list = []

    return result, body


def validate_name(name: str) -> List[str]:
    """验证 name 字段"""
    errors = []

    if not name:
        errors.append("name 字段缺失")
        return errors

    if not isinstance(name, str):
        errors.append("name 必须是字符串")
        return errors

    if len(name) > 64:
        errors.append(f"name 超过 64 字符 (当前: {len(name)})")

    if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$', name):
        errors.append("name 格式无效 (应为小写字母、数字、连字符)")

    return errors


def validate_description(description: str) -> List[str]:
    """验证 description 字段"""
    errors = []

    if not description:
        errors.append("description 字段缺失")
        return errors

    if not isinstance(description, str):
        errors.append("description 必须是字符串")
        return errors

    if len(description) < 10:
        errors.append(f"description 过短 (最少 10 字符，当前: {len(description)})")

    if len(description) > 1024:
        errors.append(f"description 超过 1024 字符 (当前: {len(description)})")

    return errors


def validate_source_url(url: str) -> List[str]:
    """验证 source_url 字段"""
    errors = []

    if not url:
        return errors  # 可选字段

    if not isinstance(url, str):
        errors.append("source_url 必须是字符串")
        return errors

    if not re.match(r'^https?://', url):
        errors.append("source_url 必须是有效的 URL")

    return errors


def validate_source_hash(hash_val: str) -> List[str]:
    """验证 source_hash 字段"""
    errors = []

    if not hash_val:
        return errors  # 可选字段

    if not isinstance(hash_val, str):
        errors.append("source_hash 必须是字符串")
        return errors

    if not re.match(r'^[a-f0-9]{40}$', hash_val):
        errors.append("source_hash 应为 40 字符的十六进制字符串")

    return errors


def validate_version(version: str) -> List[str]:
    """验证 version 字段"""
    errors = []

    if not version:
        return errors  # 可选字段

    if not isinstance(version, str):
        errors.append("version 必须是字符串")
        return errors

    # 支持语义化版本或日期版本
    if not re.match(r'^\d+\.\d+\.\d+$|^\d{4}\.\d{2}\.\d{2}$', version):
        errors.append("version 格式无效 (应为 X.Y.Z 或 YYYY.MM.DD)")

    return errors


def validate_skill(skill_dir: Path, strict: bool = False) -> Dict:
    """验证单个 Skill"""
    result = {
        "name": skill_dir.name,
        "dir": str(skill_dir),
        "valid": True,
        "errors": [],
        "warnings": [],
    }

    skill_md = skill_dir / "SKILL.md"

    # 检查 SKILL.md 存在
    if not skill_md.exists():
        result["valid"] = False
        result["errors"].append("SKILL.md 文件不存在")
        return result

    # 读取内容
    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"无法读取文件: {e}")
        return result

    # 解析 frontmatter
    frontmatter, body = parse_frontmatter(content)

    if frontmatter is None:
        result["valid"] = False
        result["errors"].append("无效的 YAML frontmatter 格式")
        return result

    # 验证必需字段
    result["errors"].extend(validate_name(frontmatter.get('name', '')))
    result["errors"].extend(validate_description(frontmatter.get('description', '')))

    # 验证可选字段
    source_url = frontmatter.get('source_url') or frontmatter.get('github_url', '')
    source_hash = frontmatter.get('source_hash') or frontmatter.get('github_hash', '')

    result["errors"].extend(validate_source_url(source_url))
    result["errors"].extend(validate_source_hash(source_hash))
    result["errors"].extend(validate_version(frontmatter.get('version', '')))

    # 严格模式检查
    if strict:
        if not source_url:
            result["warnings"].append("缺少 source_url (无法进行版本管理)")
        if not frontmatter.get('version'):
            result["warnings"].append("缺少 version 字段")
        if not frontmatter.get('created_at'):
            result["warnings"].append("缺少 created_at 字段")

    # 检查 body 内容
    if len(body.strip()) < 50:
        result["warnings"].append("SKILL.md body 内容过少")

    # 设置最终状态
    if result["errors"]:
        result["valid"] = False

    return result


def validate_all(skills_dir: Path, strict: bool = False) -> List[Dict]:
    """验证所有 Skills"""
    results = []

    if not skills_dir.exists():
        return results

    for item in sorted(skills_dir.iterdir()):
        if not item.is_dir() or item.name.startswith('.'):
            continue

        result = validate_skill(item, strict=strict)
        results.append(result)

    return results


def format_table(results: List[Dict]) -> str:
    """格式化表格输出"""
    lines = [
        f"{'Name':<25} | {'Status':<8} | {'Errors':<5} | {'Warnings':<8}",
        "-" * 55
    ]

    for r in sorted(results, key=lambda x: (x['valid'], x['name'])):
        name = r['name'][:24]
        status = "✅ OK" if r['valid'] else "❌ FAIL"
        errors = len(r['errors'])
        warnings = len(r['warnings'])
        lines.append(f"{name:<25} | {status:<8} | {errors:<5} | {warnings:<8}")

    # 统计
    total = len(results)
    valid = sum(1 for r in results if r['valid'])
    invalid = total - valid

    lines.append("-" * 55)
    lines.append(f"Total: {total} | Valid: {valid} | Invalid: {invalid}")

    return '\n'.join(lines)


def format_detail(results: List[Dict]) -> str:
    """格式化详细输出"""
    lines = []

    invalid = [r for r in results if not r['valid']]
    with_warnings = [r for r in results if r['valid'] and r['warnings']]

    if invalid:
        lines.append("=" * 50)
        lines.append("INVALID SKILLS")
        lines.append("=" * 50)

        for r in invalid:
            lines.append(f"\n{r['name']}:")
            for err in r['errors']:
                lines.append(f"  ❌ {err}")
            for warn in r['warnings']:
                lines.append(f"  ⚠️ {warn}")

    if with_warnings:
        lines.append("\n" + "=" * 50)
        lines.append("WARNINGS")
        lines.append("=" * 50)

        for r in with_warnings:
            lines.append(f"\n{r['name']}:")
            for warn in r['warnings']:
                lines.append(f"  ⚠️ {warn}")

    # 统计
    total = len(results)
    valid = sum(1 for r in results if r['valid'])

    lines.append("\n" + "=" * 50)
    lines.append(f"Summary: {valid}/{total} valid")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='批量验证 Skills 元数据',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--skills-dir', '-d',
        type=Path,
        default=DEFAULT_SKILLS_DIR,
        help=f'Skills 目录 (默认: {DEFAULT_SKILLS_DIR})'
    )
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--detail', action='store_true', help='显示详细错误信息')
    parser.add_argument('--strict', '-s', action='store_true', help='严格模式')
    parser.add_argument('--output', '-o', type=Path, help='输出到文件')

    args = parser.parse_args()

    # 验证
    results = validate_all(args.skills_dir, strict=args.strict)

    if not results:
        print(f"未找到 Skills: {args.skills_dir}", file=sys.stderr)
        sys.exit(1)

    # 格式化
    if args.json:
        output = json.dumps(results, indent=2, ensure_ascii=False)
    elif args.detail:
        output = format_detail(results)
    else:
        output = format_table(results)

    # 输出
    if args.output:
        args.output.write_text(output, encoding='utf-8')
        print(f"已保存到: {args.output}")
    else:
        print(output)

    # 退出码
    invalid_count = sum(1 for r in results if not r['valid'])
    sys.exit(1 if invalid_count > 0 else 0)


if __name__ == "__main__":
    main()
