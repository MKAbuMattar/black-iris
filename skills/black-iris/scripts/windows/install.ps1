# Install black-iris as personal skills on Windows: black-iris itself plus one
# black-iris-<mode> folder per mode, which read their reference from
# ..\black-iris\ and so must sit beside it.
#   pwsh scripts/windows/install.ps1               link into ~\.claude\skills
#   pwsh scripts/windows/install.ps1 -AlwaysOn     also set the SessionStart re-inject flag
#   pwsh scripts/windows/install.ps1 -Uninstall    remove links and flag
# A symlink needs Developer Mode or admin; without it this falls back to a
# directory junction, which needs neither.
param([switch]$AlwaysOn, [switch]$Uninstall)
$ErrorActionPreference = 'Stop'
$skill = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$root  = Split-Path $skill -Parent
# Honor HOME when set (CI, MSYS, a custom profile); fall back to the PowerShell profile dir.
$homeDir = if ($env:HOME) { $env:HOME } else { $HOME }
$dir   = Join-Path $homeDir '.claude\skills'
$flag  = Join-Path $homeDir '.BLACK_IRIS_AGENTS\always-on'
$sources = @($skill) + @(Get-ChildItem -Path $root -Directory -Filter 'black-iris-*' |
  Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } | Sort-Object Name | ForEach-Object { $_.FullName })
function Remove-Dest($dest) {
  if (-not (Test-Path $dest)) { return }
  $item = Get-Item $dest
  if ($item.LinkType) { $item.Delete() } else { Remove-Item $dest -Recurse -Force }
}
if ($Uninstall) {
  foreach ($s in $sources) { Remove-Dest (Join-Path $dir (Split-Path $s -Leaf)) }
  if (Test-Path $flag) { Remove-Item $flag }
  Write-Output "removed $($sources.Count) skill folders and always-on flag"; exit 0
}
New-Item -ItemType Directory -Force $dir | Out-Null
foreach ($s in $sources) {
  $dest = Join-Path $dir (Split-Path $s -Leaf)
  Remove-Dest $dest
  try   { New-Item -ItemType SymbolicLink -Path $dest -Target $s | Out-Null; Write-Output "linked $dest -> $s" }
  catch { New-Item -ItemType Junction     -Path $dest -Target $s | Out-Null; Write-Output "junction $dest -> $s (symlink needs Developer Mode)" }
}
if ($AlwaysOn) { New-Item -ItemType File -Force $flag | Out-Null; Write-Output "always-on flag set: $flag" }
Write-Output 'Start a new session; skills and hooks load at session start.'
