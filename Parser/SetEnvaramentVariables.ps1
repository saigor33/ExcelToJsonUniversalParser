# Set Evarament variables
$pevn_bin_path = $env:USERPROFILE +'\.pyenv\pyenv-win\bin;'
$pevn_shims_path = $env:USERPROFILE +'\.pyenv\pyenv-win\shims;'
Write-Host "Step 2: Add Envarament variables"
Write-Host "1.`"$pevn_bin_path`""
Write-Host "2.`"$pevn_shims_path`""
$env:Path = $pevn_bin_path + $env:Path 
$env:Path = $pevn_shims_path + $env:Path 

write-host "Envarament variables added" -foreground green -nonewline
echo `n