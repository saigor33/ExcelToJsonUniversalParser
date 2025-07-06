echo "Start fix execute PowerShell policy"
$error.clear()
Set-ExecutionPolicy Unrestricted -Scope Process

if (!$error) { 
	Write-Host "Fix execute PowerShell policy succeced" -foreground green
}
else {
	Write-Host "Fix execute PowerShell policy failed" -foreground red
}