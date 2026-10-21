param(
    [Parameter(Mandatory=$true)][string]$PresentationPath,
    [Parameter(Mandatory=$true)][string]$OutputDirectory
)
$ErrorActionPreference = 'Stop'
$pptPath = (Resolve-Path -LiteralPath $PresentationPath).Path
$renderDir = [System.IO.Path]::GetFullPath($OutputDirectory)
New-Item -ItemType Directory -Path $renderDir -Force | Out-Null
$existingPowerPoint = @(Get-Process -Name POWERPNT -ErrorAction SilentlyContinue)
$powerPoint = $null
$openedDeck = $null
try {
    $powerPoint = New-Object -ComObject PowerPoint.Application
    # ReadOnly, Untitled, WithWindow: automate this document without a visible window.
    $openedDeck = $powerPoint.Presentations.Open($pptPath, -1, 0, 0)
    $slides = @()
    foreach ($slide in $openedDeck.Slides) {
        $imagePath = Join-Path $renderDir ('slide-{0:d2}.png' -f $slide.SlideIndex)
        $slide.Export($imagePath, 'PNG', 1600, 900)
        $texts = @()
        foreach ($shape in $slide.Shapes) {
            if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
                $texts += [pscustomobject]@{
                    text = $shape.TextFrame.TextRange.Text
                    font = $shape.TextFrame.TextRange.Font.Name
                    left = $shape.Left
                    top = $shape.Top
                    width = $shape.Width
                    height = $shape.Height
                }
            }
        }
        $slides += [pscustomobject]@{
            page = $slide.SlideIndex
            image = [System.IO.Path]::GetFileName($imagePath)
            shape_count = $slide.Shapes.Count
            text_shapes = $texts
        }
    }
    $pdfPath = Join-Path $renderDir 'deck.pdf'
    $openedDeck.SaveAs($pdfPath, 32)
    $report = [pscustomobject]@{
        application = 'Microsoft PowerPoint'
        version = $powerPoint.Version
        source = $pptPath
        source_sha256 = (Get-FileHash -LiteralPath $pptPath -Algorithm SHA256).Hash.ToLower()
        slide_count = $openedDeck.Slides.Count
        width_pt = $openedDeck.PageSetup.SlideWidth
        height_pt = $openedDeck.PageSetup.SlideHeight
        slides = $slides
        pdf = 'deck.pdf'
        checked_at = [DateTime]::UtcNow.ToString('o')
    }
    $report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $renderDir 'powerpoint-render.json') -Encoding utf8
    Write-Output ('PowerPoint {0}: {1} slides exported to PNG and PDF' -f $powerPoint.Version, $openedDeck.Slides.Count)
}
finally {
    if ($null -ne $openedDeck) {
        $openedDeck.Close()
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($openedDeck)
    }
    if ($null -ne $powerPoint) {
        # Close only the document opened by this script; leave the user's app running.
        [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($powerPoint)
    }
}
