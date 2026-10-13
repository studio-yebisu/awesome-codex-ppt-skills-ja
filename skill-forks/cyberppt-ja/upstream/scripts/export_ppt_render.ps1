param(
  [Parameter(Mandatory=$true)][string]$Pptx,
  [Parameter(Mandatory=$true)][string]$OutDir
)

$ErrorActionPreference = "Stop"
$pptxPath = (Resolve-Path -LiteralPath $Pptx).Path
$outputDir = New-Item -ItemType Directory -Force -Path $OutDir
$powerPoint = New-Object -ComObject PowerPoint.Application
try {
  $presentation = $powerPoint.Presentations.Open($pptxPath, $true, $false, $false)
  try {
    $presentation.Export($outputDir.FullName, "PNG")
  } finally {
    $presentation.Close()
  }
} finally {
  $powerPoint.Quit()
}

Get-ChildItem -LiteralPath $outputDir.FullName -Filter "*.PNG" | Select-Object FullName,Length
