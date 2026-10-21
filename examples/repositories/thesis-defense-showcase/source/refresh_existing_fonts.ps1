$ErrorActionPreference='Stop'
$fontSources=Resolve-Path (Join-Path $PSScriptRoot '../fonts')
$installedRoot=Join-Path $env:LOCALAPPDATA 'Microsoft/Windows/Fonts'
Add-Type -TypeDefinition @"
using System;using System.Runtime.InteropServices;
public class ExistingYebisuFontRefresh {
[DllImport("gdi32.dll",CharSet=CharSet.Unicode)]public static extern int AddFontResourceEx(string path,uint flags,IntPtr reserved);
[DllImport("user32.dll",CharSet=CharSet.Unicode)]public static extern IntPtr SendMessageTimeout(IntPtr hwnd,uint msg,IntPtr w,IntPtr l,uint flags,uint timeout,out IntPtr result);
}
"@
foreach($font in Get-ChildItem -LiteralPath $fontSources -Filter '*.ttf' -File){
 $installed=Join-Path $installedRoot ('Yebisu-OSS-'+$font.Name)
 if(-not(Test-Path -LiteralPath $installed)){throw ('Install the included original OSS font manually first: '+$font.Name)}
 if((Get-FileHash -LiteralPath $installed).Hash -ne (Get-FileHash -LiteralPath $font.FullName).Hash){throw ('Different installed font retained: '+$font.Name)}
 [ExistingYebisuFontRefresh]::AddFontResourceEx($installed,0,[IntPtr]::Zero)|Out-Null
}
$result=[IntPtr]::Zero
[ExistingYebisuFontRefresh]::SendMessageTimeout([IntPtr]0xffff,0x001d,[IntPtr]::Zero,[IntPtr]::Zero,2,1000,[ref]$result)|Out-Null
Write-Output 'Existing hash-matching fonts re-notified; no files or registry values changed.'
