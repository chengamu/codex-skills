param(
    [string]$TargetPath = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

$skillRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$sourceAi = Join-Path $skillRoot "assets/scaffold/.ai"
$targetRoot = Resolve-Path $TargetPath
$targetAi = Join-Path $targetRoot ".ai"
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$copied = New-Object System.Collections.Generic.List[string]
$backedUp = New-Object System.Collections.Generic.List[string]
$skipped = New-Object System.Collections.Generic.List[string]

$protectedFiles = @(
    "MEMORY.md",
    "DECISIONS.md",
    "HANDOFF.md"
)

$protectedDirs = @(
    "requirements",
    "archive"
)

function Ensure-Dir([string]$Path) {
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Force -Path $Path | Out-Null
    }
}

function Copy-FileSafe([string]$Source, [string]$Destination, [bool]$ProtectExisting) {
    Ensure-Dir (Split-Path $Destination -Parent)
    if (Test-Path $Destination) {
        if ($ProtectExisting) {
            $skipped.Add($Destination)
            return
        }
        $backup = "$Destination.bak-$timestamp"
        Copy-Item -LiteralPath $Destination -Destination $backup -Force
        $backedUp.Add($backup)
    }
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
    $copied.Add($Destination)
}

Ensure-Dir $targetAi
foreach ($dir in @("rules", "requirements", "playbooks", "archive", "tmp", "artifacts")) {
    Ensure-Dir (Join-Path $targetAi $dir)
}

Get-ChildItem -LiteralPath $sourceAi -File | ForEach-Object {
    $protect = $protectedFiles -contains $_.Name
    Copy-FileSafe $_.FullName (Join-Path $targetAi $_.Name) $protect
}

foreach ($dir in @("rules", "playbooks", "tmp", "artifacts")) {
    Get-ChildItem -LiteralPath (Join-Path $sourceAi $dir) -File -Force | ForEach-Object {
        Copy-FileSafe $_.FullName (Join-Path (Join-Path $targetAi $dir) $_.Name) $false
    }
}

foreach ($dir in $protectedDirs) {
    $srcDir = Join-Path $sourceAi $dir
    $dstDir = Join-Path $targetAi $dir
    Get-ChildItem -LiteralPath $srcDir -File -Force | ForEach-Object {
        $dst = Join-Path $dstDir $_.Name
        if (Test-Path $dst) {
            $skipped.Add($dst)
        } else {
            Copy-Item -LiteralPath $_.FullName -Destination $dst -Force
            $copied.Add($dst)
        }
    }
}

Write-Host "amu-workflow scaffold installed."
Write-Host "Target: $targetAi"
Write-Host "Copied: $($copied.Count)"
Write-Host "Backed up: $($backedUp.Count)"
Write-Host "Skipped protected existing files: $($skipped.Count)"
if ($backedUp.Count -gt 0) {
    Write-Host "Backups:"
    $backedUp | ForEach-Object { Write-Host "  $_" }
}
if ($skipped.Count -gt 0) {
    Write-Host "Skipped:"
    $skipped | ForEach-Object { Write-Host "  $_" }
}
