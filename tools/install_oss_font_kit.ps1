param([string]$FontRoot = (Join-Path $PSScriptRoot '../downloads/fonts'))
$ErrorActionPreference = 'Stop'
$resolvedFontRoot = (Resolve-Path -LiteralPath $FontRoot).Path
$userFontDirectory = Join-Path $env:LOCALAPPDATA 'Microsoft/Windows/Fonts'
New-Item -ItemType Directory -Path $userFontDirectory -Force | Out-Null
$registryPath = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts'
New-Item -Path $registryPath -Force | Out-Null
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public class YebisuFontRegistration {
 [DllImport("gdi32.dll", CharSet=CharSet.Unicode)] public static extern int AddFontResourceEx(string name, uint flags, IntPtr reserved);
 [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern IntPtr SendMessageTimeout(IntPtr hwnd, uint msg, IntPtr wparam, IntPtr lparam, uint flags, uint timeout, out IntPtr result);
}
'@
$count = 0
foreach ($font in Get-ChildItem -LiteralPath $resolvedFontRoot -Filter '*.ttf' -Recurse -File) {
    $targetName = 'Yebisu-OSS-' + $font.Name
    $destination = Join-Path $userFontDirectory $targetName
    if (Test-Path -LiteralPath $destination) {
        if ((Get-FileHash -LiteralPath $destination).Hash -ne (Get-FileHash -LiteralPath $font.FullName).Hash) {
            throw "Existing font differs; retained: $destination"
        }
    } else { Copy-Item -LiteralPath $font.FullName -Destination $destination }
    New-ItemProperty -Path $registryPath -Name ($targetName + ' (TrueType)') -Value $destination -PropertyType String -Force | Out-Null
    [YebisuFontRegistration]::AddFontResourceEx($destination, 0, [IntPtr]::Zero) | Out-Null
    $count++
}
$broadcastResult = [IntPtr]::Zero
[YebisuFontRegistration]::SendMessageTimeout([IntPtr]0xffff, 0x001d, [IntPtr]::Zero, [IntPtr]::Zero, 2, 1000, [ref]$broadcastResult) | Out-Null
Write-Output "Registered $count original OSS font files for this Windows user."
