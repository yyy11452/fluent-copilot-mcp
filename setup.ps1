# PowerShell 快速启动脚本
# 用于一键安装和部署 Fluent-Copilot Integration

param(
    [switch]$SkipDependencies,
    [switch]$SkipGitHub,
    [string]$RepoName = "fluent-copilot-project"
)

# 设置错误处理
$ErrorActionPreference = "Continue"

# 颜色函数
function Write-ColorOutput {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Banner {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                                                           ║" -ForegroundColor Cyan
    Write-Host "║     Fluent-Copilot Integration - Quick Setup             ║" -ForegroundColor Cyan
    Write-Host "║                                                           ║" -ForegroundColor Cyan
    Write-Host "║     ANSYS Fluent + GitHub Copilot + MCP Server           ║" -ForegroundColor Cyan
    Write-Host "║                                                           ║" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Test-Prerequisites {
    Write-ColorOutput "`n🔍 检查前置条件...`n" "Yellow"
    
    $allGood = $true
    
    # Python
    try {
        $pythonVersion = python --version 2>&1
        Write-ColorOutput "  ✅ Python: $pythonVersion" "Green"
    } catch {
        Write-ColorOutput "  ❌ Python 未安装" "Red"
        $allGood = $false
    }
    
    # Git
    try {
        $gitVersion = git --version 2>&1
        Write-ColorOutput "  ✅ Git: $gitVersion" "Green"
    } catch {
        Write-ColorOutput "  ❌ Git 未安装" "Red"
        $allGood = $false
    }
    
    # Node.js (可选)
    try {
        $nodeVersion = node --version 2>&1
        Write-ColorOutput "  ✅ Node.js: $nodeVersion" "Green"
    } catch {
        Write-ColorOutput "  ⚠️  Node.js 未安装 (可选)" "Yellow"
    }
    
    return $allGood
}

function Install-Dependencies {
    if ($SkipDependencies) {
        Write-ColorOutput "`n⏭️  跳过依赖安装`n" "Yellow"
        return $true
    }
    
    Write-ColorOutput "`n📦 安装依赖...`n" "Yellow"
    
    # Python 依赖
    Write-ColorOutput "  安装 Python 包..." "Cyan"
    try {
        python -m pip install -r requirements.txt --quiet
        Write-ColorOutput "  ✅ Python 依赖安装完成" "Green"
    } catch {
        Write-ColorOutput "  ❌ Python 依赖安装失败" "Red"
        return $false
    }
    
    # Node.js 依赖 (可选)
    if (Test-Path "package.json") {
        Write-ColorOutput "  安装 Node.js 包..." "Cyan"
        try {
            npm install --silent 2>&1 | Out-Null
            Write-ColorOutput "  ✅ Node.js 依赖安装完成" "Green"
        } catch {
            Write-ColorOutput "  ⚠️  Node.js 依赖安装失败 (可选)" "Yellow"
        }
    }
    
    return $true
}

function Setup-Environment {
    Write-ColorOutput "`n⚙️  配置环境...`n" "Yellow"
    
    if (Test-Path ".env") {
        Write-ColorOutput "  ✅ .env 文件已存在" "Green"
        return $true
    }
    
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-ColorOutput "  ✅ .env 文件已创建" "Green"
        Write-ColorOutput "`n  ⚠️  请编辑 .env 文件，填入您的配置:" "Yellow"
        Write-ColorOutput "     - GITHUB_TOKEN" "White"
        Write-ColorOutput "     - GITHUB_OWNER" "White"
        Write-ColorOutput "     - FLUENT_PATH" "White"
        
        # 询问是否立即编辑
        $edit = Read-Host "`n  是否现在编辑 .env 文件? (y/n)"
        if ($edit -eq "y") {
            notepad .env
            Write-ColorOutput "`n  等待编辑完成...按任意键继续" "Cyan"
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
        
        return $true
    } else {
        Write-ColorOutput "  ❌ .env.example 文件不存在" "Red"
        return $false
    }
}

function Initialize-GitRepo {
    Write-ColorOutput "`n🔧 初始化 Git 仓库...`n" "Yellow"
    
    if (Test-Path ".git") {
        Write-ColorOutput "  ✅ Git 仓库已存在" "Green"
        return $true
    }
    
    try {
        git init 2>&1 | Out-Null
        Write-ColorOutput "  ✅ Git 仓库初始化完成" "Green"
        
        # 创建 .gitignore (如果不存在)
        if (-not (Test-Path ".gitignore")) {
            @"
__pycache__/
*.py[cod]
*`$py.class
node_modules/
.env
*.log
temp/
workspace/
"@ | Out-File ".gitignore" -Encoding utf8
            Write-ColorOutput "  ✅ .gitignore 已创建" "Green"
        }
        
        # 初始提交
        git add . 2>&1 | Out-Null
        git commit -m "Initial commit from Fluent-Copilot" 2>&1 | Out-Null
        Write-ColorOutput "  ✅ 初始提交完成" "Green"
        
        return $true
    } catch {
        Write-ColorOutput "  ❌ Git 初始化失败: $_" "Red"
        return $false
    }
}

function Deploy-ToGitHub {
    if ($SkipGitHub) {
        Write-ColorOutput "`n⏭️  跳过 GitHub 部署`n" "Yellow"
        return $true
    }
    
    Write-ColorOutput "`n🚀 部署到 GitHub...`n" "Yellow"
    
    # 确认部署
    $deploy = Read-Host "  是否部署到 GitHub? (y/n)"
    if ($deploy -ne "y") {
        Write-ColorOutput "  ⏭️  跳过 GitHub 部署" "Yellow"
        return $true
    }
    
    # 获取仓库名称
    $repo = Read-Host "  仓库名称 [$RepoName]"
    if ([string]::IsNullOrWhiteSpace($repo)) {
        $repo = $RepoName
    }
    
    # 是否私有
    $private = Read-Host "  创建私有仓库? (y/n) [n]"
    $privateFlag = if ($private -eq "y") { "--private" } else { "" }
    
    try {
        # 创建仓库
        Write-ColorOutput "  创建 GitHub 仓库..." "Cyan"
        $createCmd = "python cli/deploy.py init --repo $repo $privateFlag"
        Invoke-Expression $createCmd
        Write-ColorOutput "  ✅ 仓库创建成功" "Green"
        
        # 推送代码
        Write-ColorOutput "  推送代码..." "Cyan"
        python cli/deploy.py push --repo $repo --message "Initial deployment"
        Write-ColorOutput "  ✅ 代码推送完成" "Green"
        
        # 显示仓库链接
        $owner = $env:GITHUB_OWNER
        $repoUrl = "https://github.com/$owner/$repo"
        
        Write-Host ""
        Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Green
        Write-Host "║          部署成功! 🎉                      ║" -ForegroundColor Green
        Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Green
        Write-Host ""
        Write-ColorOutput "  仓库链接: $repoUrl" "Cyan"
        Write-Host ""
        
        return $true
    } catch {
        Write-ColorOutput "  ❌ GitHub 部署失败: $_" "Red"
        return $false
    }
}

function Show-NextSteps {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║          下一步                            ║" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-ColorOutput "  1. 查看快速开始指南:" "White"
    Write-ColorOutput "     QUICKSTART.md" "Cyan"
    Write-Host ""
    Write-ColorOutput "  2. 生成你的第一个 UDF:" "White"
    Write-ColorOutput "     python cli/manage.py generate-udf -d 描述 -t profile -n 名称" "Cyan"
    Write-Host ""
    Write-ColorOutput "  3. 启动 MCP Server (可选):" "White"
    Write-ColorOutput "     npm run start:mcp" "Cyan"
    Write-Host ""
    Write-ColorOutput "  4. 查看配置:" "White"
    Write-ColorOutput "     python cli/manage.py config" "Cyan"
    Write-Host ""
    Write-ColorOutput "  5. 查看完整文档:" "White"
    Write-ColorOutput "     docs/" "Cyan"
    Write-Host ""
}

# ============ 主程序 ============

Write-Banner

# 步骤 1: 检查前置条件
if (-not (Test-Prerequisites)) {
    Write-ColorOutput "`n❌ 前置条件检查失败`n" "Red"
    Write-ColorOutput "请安装:" "Yellow"
    Write-ColorOutput "  - Python 3.8+: https://www.python.org/" "White"
    Write-ColorOutput "  - Git: https://git-scm.com/" "White"
    Write-ColorOutput "  - Node.js 16+ (可选): https://nodejs.org/" "White"
    Write-Host ""
    exit 1
}

# 步骤 2: 安装依赖
if (-not (Install-Dependencies)) {
    Write-ColorOutput "`n❌ 依赖安装失败`n" "Red"
    exit 1
}

# 步骤 3: 设置环境
if (-not (Setup-Environment)) {
    Write-ColorOutput "`n❌ 环境设置失败`n" "Red"
    exit 1
}

# 步骤 4: 初始化 Git
if (-not (Initialize-GitRepo)) {
    Write-ColorOutput "`n❌ Git 初始化失败`n" "Red"
    exit 1
}

# 步骤 5: 生成示例 (可选)
$generateExamples = Read-Host "`n是否生成示例代码? (y/n) [y]"
if ([string]::IsNullOrWhiteSpace($generateExamples) -or $generateExamples -eq "y") {
    Write-ColorOutput "`n📝 生成示例代码...`n" "Yellow"
    try {
        python cli/manage.py generate-examples
        Write-ColorOutput "  ✅ 示例代码生成完成" "Green"
    } catch {
        Write-ColorOutput "  ⚠️  示例代码生成失败 (可跳过)" "Yellow"
    }
}

# 步骤 6: 部署到 GitHub
Deploy-ToGitHub | Out-Null

# 显示后续步骤
Show-NextSteps

Write-ColorOutput "✅ 安装和设置完成!`n" "Green"
