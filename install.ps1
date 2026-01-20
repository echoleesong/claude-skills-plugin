# Claude Skills Plugin - Windows 自动安装脚本
# 自动创建 skills 目录的软链接到 ~/.claude/skills/
# 需要管理员权限运行（创建软链接需要）

param(
    [switch]$SetupHook
)

# 设置错误处理
$ErrorActionPreference = "Stop"

# 获取脚本所在目录
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsSource = Join-Path $ScriptDir "skills"
$ClaudeDir = Join-Path $env:USERPROFILE ".claude"
$SkillsTarget = Join-Path $ClaudeDir "skills"

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║     Claude Skills Plugin - 自动安装脚本 (Windows)          ║" -ForegroundColor Blue
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# 检查是否以管理员身份运行
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "警告: 建议以管理员身份运行此脚本以创建软链接" -ForegroundColor Yellow
    Write-Host "如果创建软链接失败，请右键点击 PowerShell 并选择'以管理员身份运行'" -ForegroundColor Yellow
    Write-Host ""
}

# 检查 skills 源目录
if (-not (Test-Path $SkillsSource)) {
    Write-Host "错误: skills 目录不存在于 $SkillsSource" -ForegroundColor Red
    exit 1
}

# 创建 ~/.claude 目录
if (-not (Test-Path $ClaudeDir)) {
    Write-Host "创建 Claude 配置目录: $ClaudeDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $ClaudeDir | Out-Null
}

# 创建 ~/.claude/skills 目录
if (-not (Test-Path $SkillsTarget)) {
    Write-Host "创建 skills 目录: $SkillsTarget" -ForegroundColor Yellow
    New-Item -ItemType Directory -Force -Path $SkillsTarget | Out-Null
}

# 统计信息
$Created = 0
$Updated = 0
$Skipped = 0

Write-Host "正在链接 skills..." -ForegroundColor Blue
Write-Host ""

# 遍历 skills 目录
Get-ChildItem -Path $SkillsSource -Directory | ForEach-Object {
    $skillName = $_.Name
    $skillPath = $_.FullName
    $linkPath = Join-Path $SkillsTarget $skillName
    
    if (Test-Path $linkPath) {
        $item = Get-Item $linkPath -Force
        if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            # 是软链接
            $currentTarget = (Get-Item $linkPath).Target
            if ($currentTarget -eq $skillPath) {
                Write-Host "  ✓ $skillName (已是最新)" -ForegroundColor Green
                $script:Skipped++
            } else {
                # 更新软链接
                Remove-Item $linkPath -Force
                New-Item -ItemType SymbolicLink -Path $linkPath -Target $skillPath -Force | Out-Null
                Write-Host "  ↻ $skillName (已更新)" -ForegroundColor Yellow
                $script:Updated++
            }
        } else {
            # 存在但不是软链接
            Write-Host "  ! $skillName (已存在，跳过，请手动处理)" -ForegroundColor Yellow
            $script:Skipped++
        }
    } else {
        # 创建新的软链接
        try {
            New-Item -ItemType SymbolicLink -Path $linkPath -Target $skillPath -Force | Out-Null
            Write-Host "  + $skillName (已创建)" -ForegroundColor Green
            $script:Created++
        } catch {
            Write-Host "  ✗ $skillName (创建失败: $_)" -ForegroundColor Red
            Write-Host "    请尝试以管理员身份运行此脚本" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Blue
Write-Host "安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "  新创建: $Created" -ForegroundColor Green
Write-Host "  已更新: $Updated" -ForegroundColor Yellow
Write-Host "  已跳过: $Skipped" -ForegroundColor Blue
Write-Host ""
Write-Host "Skills 已链接到: $SkillsTarget" -ForegroundColor Blue
Write-Host ""
Write-Host "提示: 请重启 Claude Code 以使更改生效" -ForegroundColor Yellow
Write-Host ""

# 设置 Git hook（可选）
if ($SetupHook) {
    $HookDir = Join-Path $ScriptDir ".git\hooks"
    if (Test-Path $HookDir) {
        $HookFile = Join-Path $HookDir "post-merge"
        $HookContent = @'
#!/bin/bash
# Auto-run install script after git pull
echo "检测到代码更新，正在同步 skills..."
powershell.exe -ExecutionPolicy Bypass -File "$(dirname "$0")/../../install.ps1"
'@
        Set-Content -Path $HookFile -Value $HookContent -Encoding UTF8
        Write-Host "Git hook 已设置！以后 git pull 会自动同步 skills。" -ForegroundColor Green
    } else {
        Write-Host "无法设置 Git hook：.git/hooks 目录不存在" -ForegroundColor Red
    }
}
