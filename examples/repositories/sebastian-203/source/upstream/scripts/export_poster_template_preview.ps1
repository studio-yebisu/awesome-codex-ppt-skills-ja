$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$posterDir = Join-Path $repoRoot 'assets\posters'
$pptFile = Get-ChildItem -LiteralPath $posterDir -File -Filter '*.pptx' |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($null -eq $pptFile) {
    throw "No PPTX found in $posterDir"
}

$pptPath = $pptFile.FullName
$outDir = Join-Path $posterDir 'poster_template_preview_slides'

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$ppt = $null
$pres = $null

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $ppt.Visible = -1
    $pres = $ppt.Presentations.Open($pptPath, $false, $true, $false)
    $pres.Export($outDir, 'PNG', 2200, 1238)
    Get-ChildItem -LiteralPath $outDir -Filter '*.PNG' | Sort-Object Name | Select-Object Name, Length
}
finally {
    if ($pres -ne $null) {
        $pres.Close()
    }
    if ($ppt -ne $null) {
        $ppt.Quit()
    }
}
