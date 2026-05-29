# switch-agents.ps1
# Usage: ./switch-agents.ps1 -Mode ghcp
#        ./switch-agents.ps1 -Mode byok

param(
    [ValidateSet("ghcp", "byok")]
    [string]$Mode = "ghcp"
)

$LinkPath = "$env:APPDATA\Code - Insiders\User\prompts"  # adjust to your actual symlink path
$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir = Join-Path $RepoDir "agents-$Mode"

if (-not (Test-Path $TargetDir)) {
    Write-Error "Target folder not found: $TargetDir"
    exit 1
}

# Remove existing symlink or folder
if (Test-Path $LinkPath) {
    Remove-Item $LinkPath -Force
}

# Create new symlink (requires Developer Mode enabled or elevated prompt)
New-Item -ItemType SymbolicLink -Path $LinkPath -Target $TargetDir | Out-Null

Write-Host "Switched to $Mode agents -> $TargetDir" -ForegroundColor Green
