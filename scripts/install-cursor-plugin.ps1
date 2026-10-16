# Install this repo as a Cursor local plugin (~/.cursor/plugins/local/the-developer).
# After install: Developer: Reload Window, then open Customize and confirm "The Developer".

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$PluginName = "the-developer"
$DestRoot = Join-Path $env:USERPROFILE ".cursor\plugins\local\$PluginName"
$PreserveSkill = "ui-case-studies"

Write-Host "Installing Cursor plugin '$PluginName' from:"
Write-Host "  $RepoRoot"
Write-Host "Into:"
Write-Host "  $DestRoot"

$Backup = $null
$PreservePath = Join-Path $DestRoot "skills\$PreserveSkill"
if (Test-Path $PreservePath) {
  $Backup = Join-Path $env:TEMP "the-developer-plugin-preserve-$PreserveSkill"
  if (Test-Path $Backup) { Remove-Item $Backup -Recurse -Force }
  Copy-Item $PreservePath $Backup -Recurse -Force
  Write-Host "Preserved existing skill: $PreserveSkill"
}

New-Item -ItemType Directory -Force -Path $DestRoot | Out-Null

$CopyMap = @(
  @{ Src = ".cursor-plugin"; Dst = ".cursor-plugin" },
  @{ Src = ".cursor\rules"; Dst = ".cursor\rules" },
  @{ Src = ".cursor\agents"; Dst = ".cursor\agents" },
  @{ Src = ".cursor\commands"; Dst = ".cursor\commands" },
  @{ Src = "agents"; Dst = "agents" },
  @{ Src = "skills"; Dst = "skills" }
)

foreach ($item in $CopyMap) {
  $src = Join-Path $RepoRoot $item.Src
  $dst = Join-Path $DestRoot $item.Dst
  if (-not (Test-Path $src)) {
    Write-Warning "Skip missing: $($item.Src)"
    continue
  }
  if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
  New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
  Copy-Item $src $dst -Recurse -Force
  Write-Host "Copied $($item.Src)"
}

if ($Backup -and (Test-Path $Backup)) {
  $restore = Join-Path $DestRoot "skills\$PreserveSkill"
  if (-not (Test-Path $restore)) {
    Copy-Item $Backup $restore -Recurse -Force
    Write-Host "Restored preserved skill: $PreserveSkill"
  }
  Remove-Item $Backup -Recurse -Force
}

$manifest = Join-Path $DestRoot ".cursor-plugin\plugin.json"
if (-not (Test-Path $manifest)) {
  throw "Install failed: missing $manifest"
}

Write-Host ""
Write-Host "Done. Reload Cursor (Developer: Reload Window), then open Customize to verify the plugin."
Write-Host "Commands: /understand  /spec  /plan"
