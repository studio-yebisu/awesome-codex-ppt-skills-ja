param([Parameter(Mandatory=$true)][string]$CaseDirectory)
$ErrorActionPreference = 'Stop'
$casePath = (Resolve-Path -LiteralPath $CaseDirectory).Path
$outputDir = Join-Path $casePath 'qa/editability'
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
$outputPath = Join-Path $outputDir 'group-moved.pptx'
Copy-Item -LiteralPath (Join-Path $casePath 'deck.pptx') -Destination $outputPath -Force
$application = $null
$deck = $null
function Read-Connections($slide) {
    @('prototype_procedure','procedure_evaluate','evaluate_revise','revise_prototype') | ForEach-Object {
        $shape = $slide.Shapes.Item('ARROW_' + $_)
        [pscustomobject]@{
            name = $shape.Name
            begin_connected = [bool]($shape.ConnectorFormat.BeginConnected -eq -1)
            end_connected = [bool]($shape.ConnectorFormat.EndConnected -eq -1)
            from = $shape.ConnectorFormat.BeginConnectedShape.Name
            to = $shape.ConnectorFormat.EndConnectedShape.Name
        }
    }
}
try {
    $application = New-Object -ComObject PowerPoint.Application
    $deck = $application.Presentations.Open($outputPath, 0, 0, 0)
    $slide = $deck.Slides.Item(8)
    $group = $slide.Shapes.Item('GROUP_procedure')
    $before = [pscustomobject]@{left=$group.Left; top=$group.Top; members=$group.GroupItems.Count}
    $connectionsBefore = @(Read-Connections $slide)
    $group.Left = $group.Left + 24
    $group.Top = $group.Top + 18
    $deck.Save()
    $deck.Close()
    $deck = $application.Presentations.Open($outputPath, -1, 0, 0)
    $slide = $deck.Slides.Item(8)
    $group = $slide.Shapes.Item('GROUP_procedure')
    $after = [pscustomobject]@{left=$group.Left; top=$group.Top; members=$group.GroupItems.Count}
    $connectionsAfter = @(Read-Connections $slide)
    if ([math]::Abs($after.left-$before.left-24) -gt 0.1 -or [math]::Abs($after.top-$before.top-18) -gt 0.1) { throw 'Saved group move was not retained.' }
    if ($after.members -ne 2) { throw 'Expected box and text in the moved group.' }
    if (@($connectionsAfter | Where-Object {-not $_.begin_connected -or -not $_.end_connected}).Count) { throw 'A connector was detached after saving.' }
    $slide.Export((Join-Path $outputDir 'slide-08.png'), 'PNG', 1600, 900)
    $deck.SaveAs((Join-Path $outputDir 'deck.pdf'), 32)
    [pscustomobject]@{
        method='Microsoft PowerPoint: move one native box-and-label group, save, close and reopen'
        source='deck.pptx'
        source_sha256=(Get-FileHash -LiteralPath (Join-Path $casePath 'deck.pptx') -Algorithm SHA256).Hash.ToLower()
        edited='qa/editability/group-moved.pptx'
        edited_sha256=(Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash.ToLower()
        group='GROUP_procedure'
        before=$before
        after=$after
        connections_before=$connectionsBefore
        connections_after=$connectionsAfter
        scope='One representative group and four real connection bindings; other editing behavior untested.'
        passed=$true
    } | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $outputDir 'group-move.json') -Encoding utf8
    Write-Output 'PowerPoint group move retained after save/reopen; four connectors remain bound.'
}
finally {
    if ($null -ne $deck) { $deck.Close(); [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($deck) }
    if ($null -ne $application) { [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($application) }
}
