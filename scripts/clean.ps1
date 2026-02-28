#!/usr/bin/env pwsh
# 清理项目中的临时文件和缓存

Write-Host "🧹 开始清理项目..." -ForegroundColor Cyan

$itemsToRemove = @(
    ".pytest_cache",
    "htmlcov",
    ".coverage",
    ".history",
    "*.pyc",
    ".tox",
    ".nox",
    "dist",
    "build",
    "*.egg-info"
)

foreach ($item in $itemsToRemove) {
    if (Test-Path $item) {
        Remove-Item -Recurse -Force $item -ErrorAction SilentlyContinue
        Write-Host "  ✓ 删除: $item" -ForegroundColor Green
    }
}

# 清理所有 __pycache__ 目录
$pycacheDirs = Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue
foreach ($dir in $pycacheDirs) {
    Remove-Item -Recurse -Force $dir.FullName -ErrorAction SilentlyContinue
    Write-Host "  ✓ 删除: $($dir.FullName)" -ForegroundColor Green
}

# 清理所有 .pyc 文件
$pycFiles = Get-ChildItem -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue
foreach ($file in $pycFiles) {
    Remove-Item -Force $file.FullName -ErrorAction SilentlyContinue
    Write-Host "  ✓ 删除: $($file.FullName)" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ 清理完成！" -ForegroundColor Green
Write-Host ""
Write-Host "提示: 运行 'pytest tests/ --cov=src/fluent_integration' 可重新生成测试报告" -ForegroundColor Yellow
