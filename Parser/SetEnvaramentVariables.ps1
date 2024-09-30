# Set Evarament variables
$pyenv_bin_path = $env:USERPROFILE +'\.pyenv\pyenv-win\bin;'
$pyenv_shims_path = $env:USERPROFILE +'\.pyenv\pyenv-win\shims;'
Write-Host "Add Envarament variables process"
Write-Host "1.`"$pyenv_bin_path`""
Write-Host "2.`"$pyenv_shims_path`""
$env:Path = $pyenv_bin_path + $env:Path 
$env:Path = $pyenv_shims_path + $env:Path 

write-host "Envarament variables added" -foreground green -nonewline
echo `n