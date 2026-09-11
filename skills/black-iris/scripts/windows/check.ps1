# black-iris self-lint, PowerShell edition. Same checks as universal/check.py.
# Run: pwsh scripts/windows/check.ps1   (Windows PowerShell 5.1 also works)
$ErrorActionPreference = 'Stop'
$skill = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$root  = Resolve-Path (Join-Path $skill '..\..')
Set-Location $skill
$fail = $false
function Hit($m)  { Write-Output "FAIL: $m"; $script:fail = $true }
function Want($label, $expected, $actual) { if ($expected -ne $actual) { Hit "${label}: expected $expected, found $actual" } }
function Count($pattern, $text) { ([regex]::Matches($text, $pattern, 'Multiline')).Count }
function Section($text, $start, $end) {
  $m = [regex]::Match($text, "(?ms)^" + [regex]::Escape($start) + ".*?(?=^" + [regex]::Escape($end) + ")")
  if ($m.Success) { $m.Value } else { '' }
}

# Cut list 1, 9, 10 applied to our own prose and scripts. Regex escapes, so
# this file never contains the characters it bans.
Get-ChildItem -Recurse -Path $skill,(Join-Path $root 'hooks') -Include *.md,*.py,*.sh,*.ps1,*.json | ForEach-Object {
  $rel = $_.FullName.Substring($root.Path.Length + 1); $i = 0
  foreach ($line in Get-Content $_.FullName -Encoding UTF8) {
    $i++
    if ($line -match '[^\x00-\x7F]') { Hit "${rel}:${i}: non-ASCII byte (Cut list 1 and 9)" }
    if ($line -match '^Co-[Aa]uthored-[Bb]y:')  { Hit "${rel}:${i}: AI trailer (Cut list 10)" }
  }
}

$s = Get-Content SKILL.md -Raw -Encoding UTF8
Want 'shape rules'     10 (Count '^\d+\. \*\*' (Section $s '## Shape' '## Build'))
Want 'build rules'      5 (Count '^\d+\. \*\*' (Section $s '## Build' '## Cut list'))
Want 'cut list items'  10 (Count '^\d+\. '     (Section $s '## Cut list' 'Full catalog'))
$ids = [regex]::Matches((Get-Content references/deslop.md -Raw -Encoding UTF8), '(?m)^### (\d+)\. ') | ForEach-Object { [int]$_.Groups[1].Value }
if (($ids -join ',') -ne (($ids | Sort-Object -Unique) -join ',')) { Hit 'deslop pattern ids must be unique and ascending' }
$ideate = Get-Content references/ideate.md -Raw -Encoding UTF8
Want 'ideate frames'   15 (Count '^\| \*\*' (Section $ideate '## Frames' '## Output'))

# The router's cost is bytes, not lines. A line budget bought compression that
# cost clarity; the length cap stops a long line from gaming the byte budget.
$bytes = [System.Text.Encoding]::UTF8.GetByteCount($s)
if ($bytes -gt 16000) { Hit "SKILL.md is $bytes bytes, over the 16000 budget (about 4k tokens)" }
$i = 0
foreach ($line in ($s -split "\r?\n")) {
  $i++
  if ($line.Length -gt 100 -and -not $line.StartsWith('|') -and -not $line.StartsWith('   ')) {
    Hit "SKILL.md:${i}: prose line is $($line.Length) chars, over 100"
  }
}
$m = [regex]::Match($s, '(?ms)^description: >\r?\n(.*?)^license:')
$desc = if ($m.Success) { ($m.Groups[1].Value -split '\s+' | Where-Object { $_ }) -join ' ' } else { '' }
if (-not $desc) { Hit 'description block not found' }
if ($desc.Length -gt 1024) { Hit "description is $($desc.Length) chars, over the 1024 cap" }

$named  = [regex]::Matches($s, '`references/([a-z-]+\.md)`') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
$onDisk = Get-ChildItem references -Filter *.md | ForEach-Object Name
foreach ($f in $named)  { if ($f -notin $onDisk) { Hit "SKILL.md points at missing references/$f" } }
foreach ($f in $onDisk) { if ($f -notin $named)  { Hit "references/$f exists but SKILL.md never points at it" } }

$hooks = Join-Path $root 'hooks\hooks.json'
if (Test-Path $hooks) { try { Get-Content $hooks -Raw | ConvertFrom-Json | Out-Null } catch { Hit "hooks.json is not valid JSON: $_" } }

if (-not $fail) { Write-Output 'clean'; exit 0 } else { exit 1 }
