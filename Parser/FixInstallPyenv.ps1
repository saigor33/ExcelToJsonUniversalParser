if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))
{
    Start-Process PowerShell -Verb RunAs "-NoProfile -ExecutionPolicy Bypass -Command `"cd '$pwd'; & '$PSCommandPath';`"";
    exit;
}

echo "Step 1: Start fix install pyenv"
$error.clear()
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

if (!$error) { 
	Write-Host "Fix install pyenv applied. Rerun Instal.ps1" -foreground green -nonewline
}

pause
