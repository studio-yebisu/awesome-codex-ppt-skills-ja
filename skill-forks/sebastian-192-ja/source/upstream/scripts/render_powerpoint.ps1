param(
    [Parameter(Mandatory = $true)][string]$Deck,
    [Parameter(Mandatory = $true)][string]$OutputDir,
    [Parameter(Mandatory = $true)][int]$Width,
    [Parameter(Mandatory = $true)][int]$Height,
    [string]$SlideNumbers = '',
    [string]$ProcessMarker = '',
    [switch]$MeasureText
)

$ErrorActionPreference = 'Stop'
$app = $null
$presentation = $null
$owned = $false
$existing = @(Get-Process POWERPNT -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id)
function Measure-Frame($shape, $page, $cell, $frame, $unsupported) {
    $identity = @{page_number=[int]$page; element_id=($shape.Name -split ' \| ',2)[0]}
    if ($cell) { $identity.cell = $cell }
    if ($unsupported -or $shape.Rotation -ne 0) {
        return ($identity + @{status='unverified'; reason='Rotated/grouped text requires visual review'})
    }
    if (-not $frame.HasText) { return $null }
    $range = $frame.TextRange
    return ($identity + @{status='measured';
        content_width_pt=[double]$range.BoundWidth; content_height_pt=[double]$range.BoundHeight;
        available_width_pt=[double]($shape.Width-$frame.MarginLeft-$frame.MarginRight);
        available_height_pt=[double]($shape.Height-$frame.MarginTop-$frame.MarginBottom);
        bounds=@([double]$range.BoundLeft,[double]$range.BoundTop,[double]$range.BoundWidth,[double]$range.BoundHeight)})
}
function Measure-Shapes($shapes, $page, $unsupported=$false) {
    $records = @()
    foreach ($shape in $shapes) {
        if ($shape.Type -eq 6) { $records += @(Measure-Shapes $shape.GroupItems $page $true); continue }
        if ($shape.HasTable) {
            for ($row=1; $row -le $shape.Table.Rows.Count; $row++) {
                for ($col=1; $col -le $shape.Table.Columns.Count; $col++) {
                    $cellShape = $shape.Table.Cell($row,$col).Shape
                    $item = Measure-Frame $cellShape $page @($row,$col) $cellShape.TextFrame2 $unsupported
                    if ($item) { $item.element_id=($shape.Name -split ' \| ',2)[0]; $records += $item }
                }
            }
            $records += @{page_number=[int]$page; element_id=($shape.Name -split ' \| ',2)[0];
                status='table_bounds'; bounds=@([double]$shape.Left,[double]$shape.Top,[double]$shape.Width,[double]$shape.Height)}
        } elseif ($shape.HasTextFrame) {
            $item = Measure-Frame $shape $page $null $shape.TextFrame2 $unsupported
            if ($item) { $records += $item }
        }
    }
    return $records
}
try {
    $app = New-Object -ComObject PowerPoint.Application
    # COM may return an existing interactive instance. Never quit or kill it.
    Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class SlideMuseWindow { [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hwnd, out uint pid); }'
    [uint32]$applicationProcessId = 0
    [void][SlideMuseWindow]::GetWindowThreadProcessId([IntPtr]$app.HWND,[ref]$applicationProcessId)
    $applicationProcess = Get-Process -Id $applicationProcessId -ErrorAction Stop
    $owned = $applicationProcess.ProcessName -eq 'POWERPNT' -and $existing -notcontains $applicationProcessId
    if ($ProcessMarker) {
        @{Owned=$owned; ProcessId=[int]$applicationProcessId; StartTicks=$applicationProcess.StartTime.ToUniversalTime().Ticks.ToString()} |
            ConvertTo-Json | Set-Content -LiteralPath $ProcessMarker -Encoding UTF8
    }
    $presentation = $app.Presentations.Open($Deck, $true, $false, $false)
    $selected = if ($SlideNumbers) { @($SlideNumbers.Split(',') | ForEach-Object { [int]$_ }) } else { @(1..$presentation.Slides.Count) }
    if (($selected | Select-Object -Unique).Count -ne $selected.Count) { throw 'Duplicate slide indices' }
    foreach ($index in $selected) {
        if ($index -lt 1 -or $index -gt $presentation.Slides.Count) { throw 'Slide index outside deck' }
        $target = Join-Path $OutputDir ('{0:D3}.png' -f $index)
        $presentation.Slides.Item($index).Export($target, 'PNG', $Width, $Height)
        if ($MeasureText) {
            $records = @(Measure-Shapes $presentation.Slides.Item($index).Shapes $index)
            $measurement = @{version='1.0'; page_number=[int]$index; items=$records;
                slide_width_pt=[double]$presentation.PageSetup.SlideWidth; slide_height_pt=[double]$presentation.PageSetup.SlideHeight}
            $measurement | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $OutputDir ('{0:D3}.layout.json' -f $index)) -Encoding UTF8
        }
    }
}
finally {
    if ($null -ne $presentation) {
        $presentation.Close()
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($presentation)
    }
    if ($null -ne $app) {
        if ($owned) { $app.Quit() }
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
    }
}
