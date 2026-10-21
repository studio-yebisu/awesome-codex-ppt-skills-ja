param([Parameter(Mandatory=$true)][string]$PresentationPath,[Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
$source=(Resolve-Path -LiteralPath $PresentationPath).Path
$destination=[IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $destination -Force | Out-Null
$application=$null
$presentation=$null
try {
    $application=New-Object -ComObject PowerPoint.Application
    $presentation=$application.Presentations.Open($source,-1,0,0)
    $presentation.SaveAs((Join-Path $destination 'deck.pdf'),32)
    [pscustomobject]@{application='Microsoft PowerPoint16';slide_count=$presentation.Slides.Count;source_pptx_sha256=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLower();read_only=$true;export='deck.pdf';source_modified=$false} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $destination 'powerpoint-render.json') -Encoding utf8
} finally {
    if ($null -ne $presentation) {$presentation.Close();[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($presentation)}
    if ($null -ne $application) {[void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($application)}
}
