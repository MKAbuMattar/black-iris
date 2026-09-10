# Install black-iris as a personal skill on Windows.
#   pwsh scripts/windows/install.ps1               link into ~\.claude\skills
#   pwsh scripts/windows/install.ps1 -AlwaysOn     also set the SessionStart re-inject flag
#   pwsh scripts/windows/install.ps1 -Uninstall    remove link and flag
# A symlink needs Developer Mode or admin; without it this falls back to a
# directory junction, which needs neither.
param([switch]$AlwaysOn, [switch]$Uninstall)
$ErrorActionPreference = 'Stop'
$skill = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$dest  = Join-Path $HOME ".claude\skills\$(Split-Path $skill -Leaf)"
$flag  = Join-Path $HOME '.BLACK_IRIS_AGENTS\always-on'
function Remove-Dest {
  if (-not (Test-Path $dest)) { return }
  $item = Get-Item $dest
  if ($item.LinkType) { $item.Delete() } else { Remove-Item $dest -Recurse -Force }
}
if ($Uninstall) {
  Remove-Dest
  if (Test-Path $flag) { Remove-Item $flag }
  Write-Output "removed $dest and always-on flag"; exit 0
}
New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
Remove-Dest
try   { New-Item -ItemType SymbolicLink -Path $dest -Target $skill | Out-Null; Write-Output "linked $dest -> $skill" }
catch { New-Item -ItemType Junction     -Path $dest -Target $skill | Out-Null; Write-Output "junction $dest -> $skill (symlink needs Developer Mode)" }
if ($AlwaysOn) { New-Item -ItemType File -Force $flag | Out-Null; Write-Output "always-on flag set: $flag" }
Write-Output 'Start a new session; skills and hooks load at session start.'
