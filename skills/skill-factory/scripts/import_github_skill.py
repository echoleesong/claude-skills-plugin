#!/usr/bin/env python3
"""
import_github_skill.py - 从 GitHub 仓库导入完整 Skill

高效地从 GitHub 仓库下载所有文件并创建本地 Skill，支持并行下载。

用法:
    python import_github_skill.py <github_url> <output_dir> [--name <skill_name>] [--no-source]

参数:
    github_url    GitHub 仓库 URL
    output_dir    输出目录（如 ./skills）
    --name        自定义 Skill 名称（默认使用仓库名）
    --no-source   不保留源信息（移除 source_url, source_hash 等元数据）

示例:
    python import_github_skill.py https://github.com/user/skill-repo ./skills
    python import_github_skill.py https://github.com/user/skill-repo ./skills --name my-skill
    python import_github_skill.py https://github.com/user/skill-repo ./skills --no-source

特点:
    - 使用 GitHub API 获取目录结构（单次请求）
    - 并行下载所有文件（使用 ThreadPoolExecutor）
    - 自动检测默认分支（main/master）
    - 支持递归获取子目录
    - 可选移除源信息
"""

import sys
import os
import json
import re
import argparse
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from pathlib import Path


# 配置
MAX_WORKERS = 10  # 并行下载线程数
TIMEOUT = 30  # 单个请求超时时间（秒）
USER_AGENT = 'skill-factory/2.0'


def normalize_url(url: str) -> str:
    """标准化 GitHub URL"""
    clean_url = url.strip().rstrip('/')
    if clean_url.endswith('.git'):
        clean_url = clean_url[:-4]
    return clean_url


def extract_repo_parts(url: str) -> tuple[str, str]:
    """从 URL 提取 owner 和 repo 名称"""
    clean_url = normalize_url(url)
    parts = clean_url.split('/')
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return '', parts[-1] if parts else ''


def fetch_json(url: str, retry: int = 3) -> Optional[dict]:
    """获取 JSON 数据，支持重试"""
    import time

    for attempt in range(retry):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': USER_AGENT,
                    'Accept': 'application/vnd.github.v3+json'
                }
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 403:
                # API 限流，等待后重试
                if attempt < retry - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"API 限流，等待 {wait_time} 秒后重试...", file=sys.stderr)
                    time.sleep(wait_time)
                    continue
            print(f"HTTP 错误 {e.code}: {url}", file=sys.stderr)
            return None
        except Exception as e:
            if attempt < retry - 1:
                time.sleep(1)
                continue
            print(f"请求失败: {url} - {e}", file=sys.stderr)
            return None
    return None


def fetch_raw_content(url: str, retry: int = 3) -> Optional[bytes]:
    """获取原始文件内容，支持重试"""
    import time

    for attempt in range(retry):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                return response.read()
        except Exception as e:
            if attempt < retry - 1:
                time.sleep(0.5)
                continue
            print(f"下载失败: {url} - {e}", file=sys.stderr)
            return None
    return None


def detect_default_branch(owner: str, repo: str) -> str:
    """检测仓库的默认分支"""
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    data = fetch_json(api_url)
    if data and 'default_branch' in data:
        return data['default_branch']
    return 'main'  # 默认假设 main


def get_repo_contents(owner: str, repo: str, path: str = '', branch: str = 'main') -> list[dict]:
    """
    递归获取仓库目录内容

    Returns:
        list: 文件信息列表，每个元素包含 path, type, download_url
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    if branch:
        api_url += f"?ref={branch}"

    data = fetch_json(api_url)
    if not data:
        return []

    # 确保是列表
    if isinstance(data, dict):
        data = [data]

    files = []
    dirs_to_process = []

    for item in data:
        if item['type'] == 'file':
            files.append({
                'path': item['path'],
                'type': 'file',
                'download_url': item.get('download_url'),
                'size': item.get('size', 0)
            })
        elif item['type'] == 'dir':
            # 跳过 .git 和其他隐藏目录（除了 .claude）
            name = item['name']
            if name == '.git' or (name.startswith('.') and name != '.claude'):
                continue
            dirs_to_process.append(item['path'])

    # 递归处理子目录
    for dir_path in dirs_to_process:
        files.extend(get_repo_contents(owner, repo, dir_path, branch))

    return files


def clone_and_copy(github_url: str, output_path: str, branch: str = 'main') -> bool:
    """
    备选方案：使用 git clone 获取仓库内容

    当 GitHub API 限流时使用此方法
    """
    import subprocess
    import shutil
    import tempfile

    print("使用 git clone 备选方案...")

    # 创建临时目录
    temp_dir = tempfile.mkdtemp(prefix='skill_import_')

    try:
        # 浅克隆（只获取最新版本，不获取历史）
        clone_cmd = [
            'git', 'clone',
            '--depth', '1',
            '--branch', branch,
            github_url,
            temp_dir
        ]

        print(f"执行: git clone --depth 1 --branch {branch} ...")
        result = subprocess.run(
            clone_cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            # 尝试不指定分支
            clone_cmd = ['git', 'clone', '--depth', '1', github_url, temp_dir]
            shutil.rmtree(temp_dir, ignore_errors=True)
            os.makedirs(temp_dir, exist_ok=True)

            result = subprocess.run(
                clone_cmd,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                print(f"git clone 失败: {result.stderr}", file=sys.stderr)
                return False

        # 删除 .git 目录
        git_dir = os.path.join(temp_dir, '.git')
        if os.path.exists(git_dir):
            shutil.rmtree(git_dir)

        # 复制到目标目录
        if os.path.exists(output_path):
            shutil.rmtree(output_path)

        shutil.copytree(temp_dir, output_path)

        # 统计文件数
        file_count = sum(len(files) for _, _, files in os.walk(output_path))
        print(f"成功克隆 {file_count} 个文件")

        return True

    except subprocess.TimeoutExpired:
        print("git clone 超时", file=sys.stderr)
        return False
    except Exception as e:
        print(f"git clone 失败: {e}", file=sys.stderr)
        return False
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)


def download_file(file_info: dict, output_base: str) -> tuple[str, bool, str]:
    """
    下载单个文件

    Returns:
        tuple: (文件路径, 是否成功, 错误信息)
    """
    path = file_info['path']
    download_url = file_info.get('download_url')

    if not download_url:
        return path, False, "无下载链接"

    output_path = os.path.join(output_base, path)

    # 创建目录
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 下载内容
    content = fetch_raw_content(download_url)
    if content is None:
        return path, False, "下载失败"

    # 写入文件
    try:
        with open(output_path, 'wb') as f:
            f.write(content)
        return path, True, ""
    except Exception as e:
        return path, False, str(e)


def download_files_parallel(files: list[dict], output_base: str) -> tuple[int, int]:
    """
    并行下载所有文件

    Returns:
        tuple: (成功数, 失败数)
    """
    success_count = 0
    fail_count = 0

    print(f"\n开始下载 {len(files)} 个文件...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有下载任务
        future_to_file = {
            executor.submit(download_file, f, output_base): f
            for f in files
        }

        # 收集结果
        for future in as_completed(future_to_file):
            path, success, error = future.result()
            if success:
                success_count += 1
                print(f"  ✓ {path}")
            else:
                fail_count += 1
                print(f"  ✗ {path}: {error}")

    return success_count, fail_count


def remove_source_metadata(skill_md_path: str) -> bool:
    """从 SKILL.md 中移除源信息元数据"""
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 移除 source_url, source_hash, created_at, updated_at 等字段
        patterns = [
            r'^source_url:.*\n',
            r'^source_hash:.*\n',
            r'^source:.*\n',
            r'^created_at:.*\n',
            r'^updated_at:.*\n',
            r'^version:.*\n',
            r'^evolution_enabled:.*\n',
            r'^entry_point:.*\n',
            r'^# 生命周期管理字段.*\n',
            r'^# 可选字段.*\n',
            r'^metadata:.*\n',
            r'^  trigger:.*\n',
            r'^  source:.*\n',
        ]

        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)

        # 清理多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)

        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"移除源信息失败: {e}", file=sys.stderr)
        return False


def rename_skill(skill_path: str, new_name: str) -> bool:
    """重命名 Skill（修改 SKILL.md 中的 name 字段）"""
    skill_md_path = os.path.join(skill_path, 'SKILL.md')
    if not os.path.exists(skill_md_path):
        return False

    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换 name 字段
        content = re.sub(
            r'^name:\s*.*$',
            f'name: {new_name}',
            content,
            count=1,
            flags=re.MULTILINE
        )

        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"重命名失败: {e}", file=sys.stderr)
        return False


def import_github_skill(
    github_url: str,
    output_dir: str,
    skill_name: Optional[str] = None,
    remove_source: bool = False
) -> Optional[str]:
    """
    从 GitHub 导入 Skill

    Args:
        github_url: GitHub 仓库 URL
        output_dir: 输出目录
        skill_name: 自定义 Skill 名称
        remove_source: 是否移除源信息

    Returns:
        str: 创建的 Skill 路径，失败返回 None
    """
    # 1. 解析 URL
    owner, repo = extract_repo_parts(github_url)
    if not owner or not repo:
        print(f"错误: 无法解析 GitHub URL: {github_url}", file=sys.stderr)
        return None

    print(f"仓库: {owner}/{repo}")

    # 2. 检测默认分支
    print("检测默认分支...")
    branch = detect_default_branch(owner, repo)
    print(f"默认分支: {branch}")

    # 3. 确定输出路径
    final_name = skill_name or repo
    # 清理名称
    final_name = re.sub(r'[^a-z0-9-]', '-', final_name.lower())
    final_name = re.sub(r'-+', '-', final_name).strip('-')

    skill_path = os.path.join(output_dir, final_name)

    # 检查是否已存在
    if os.path.exists(skill_path):
        print(f"警告: 目录已存在，将覆盖: {skill_path}")

    # 4. 获取目录结构
    print("获取仓库目录结构...")
    files = get_repo_contents(owner, repo, '', branch)

    success = 0
    fail = 0

    if files:
        # 方案A: 使用 API + 并行下载
        print(f"发现 {len(files)} 个文件")
        success, fail = download_files_parallel(files, skill_path)
        print(f"\n下载完成: {success} 成功, {fail} 失败")
    else:
        # 方案B: 使用 git clone 备选方案
        print("API 获取失败，尝试 git clone...")
        if clone_and_copy(github_url, skill_path, branch):
            success = 1  # 标记成功
        else:
            print("错误: 无法获取仓库内容", file=sys.stderr)
            return None

    if success == 0:
        print("错误: 没有成功下载任何文件", file=sys.stderr)
        return None

    # 5. 后处理
    skill_md_path = os.path.join(skill_path, 'SKILL.md')

    # 重命名（如果指定了新名称）
    if skill_name and os.path.exists(skill_md_path):
        print(f"重命名 Skill 为: {final_name}")
        rename_skill(skill_path, final_name)

    # 移除源信息（如果指定）
    if remove_source and os.path.exists(skill_md_path):
        print("移除源信息...")
        remove_source_metadata(skill_md_path)

    return skill_path


def main():
    parser = argparse.ArgumentParser(
        description='从 GitHub 仓库导入完整 Skill',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s https://github.com/user/skill-repo ./skills
  %(prog)s https://github.com/user/skill-repo ./skills --name my-skill
  %(prog)s https://github.com/user/skill-repo ./skills --no-source
'''
    )

    parser.add_argument('github_url', help='GitHub 仓库 URL')
    parser.add_argument('output_dir', help='输出目录')
    parser.add_argument('--name', dest='skill_name', help='自定义 Skill 名称')
    parser.add_argument('--no-source', dest='remove_source', action='store_true',
                        help='不保留源信息（移除 source_url 等元数据）')

    args = parser.parse_args()

    # 验证 URL
    if not re.match(r'https?://(www\.)?github\.com/', args.github_url):
        print(f"错误: 不是有效的 GitHub URL: {args.github_url}", file=sys.stderr)
        sys.exit(1)

    # 执行导入
    skill_path = import_github_skill(
        args.github_url,
        args.output_dir,
        args.skill_name,
        args.remove_source
    )

    if skill_path:
        print(f"\n✅ Skill 导入成功: {skill_path}")
        print("\n目录结构:")
        # 显示目录结构
        for root, dirs, files in os.walk(skill_path):
            level = root.replace(skill_path, '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = '  ' * (level + 1)
            for file in files[:10]:  # 限制显示数量
                print(f"{subindent}{file}")
            if len(files) > 10:
                print(f"{subindent}... 还有 {len(files) - 10} 个文件")
    else:
        print("\n❌ Skill 导入失败", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
