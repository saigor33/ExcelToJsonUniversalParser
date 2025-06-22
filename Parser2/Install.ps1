Function InstallPythonModule {
	param (
        [string]$moduleName,
        [string]$moduleVersions
    )
   
	Write-Host "Step 7: Install python module `"$moduleName`" v.$moduleVersions"
	pip install $moduleName==$moduleVersions
	Write-Host "Python module `"$moduleName`" installed" -foreground green -nonewline
	echo `n
}

$ErrorActionPreference = "Inquire"

# Fix execute PowerShell policy
& "$PSScriptRoot/FixExecutePowerShellPolicy.ps1"

$installationSubScriptsPath = "./InstallationSubScripts/"

if(-not(Test-Path -Path $installationSubScriptsPath))
{
	mkdir $installationSubScriptsPath
}

# Install pyenv
Write-Host "Step 1: Install penv stage"
$installPyenvFilePath = $installationSubScriptsPath +"install-pyenv-win.ps1"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile $installPyenvFilePath
&$installPyenvFilePath
write-host "Istall penv finished!" -foreground green -nonewline
echo `n

# Set Envarament variables
Write-Host "Step 2: Add Envarament variables"
& "$PSScriptRoot/SetEnvaramentVariables.ps1"

# Pyenv update cache
Write-Host "Step 3: Update pyenv cache"
pyenv update
Write-Host "Pyenv cache updated" -foreground green -nonewline
echo `n

# Install Python 3.9.11
Write-Host "Step 4: Install python 3.9.11"
pyenv install 3.9.11
Write-Host "Python 3.9.11 installed" -foreground green -nonewline
echo `n

# Select python version in pyenv
Write-Host "Step 5: Select python version 3.9.11 in pyenv"
pyenv global 3.9.11
Write-Host "Python version 3.9.11 selected" -foreground green -nonewline
echo `n

# Install pip
Write-Host "Step 6: Install pip"
$installPipFilePath = $installationSubScriptsPath +"get-pip.py"
Invoke-WebRequest -UseBasicParsing -Uri  https://bootstrap.pypa.io/pip/3.7/get-pip.py -OutFile $installPipFilePath
python $installPipFilePath
Write-Host "Pip installed!" -foreground green -nonewline
echo `n

InstallPythonModule -moduleName "numpy" -moduleVersions "1.20.3"
InstallPythonModule -moduleName "pandas" -moduleVersions "1.5.2"
InstallPythonModule -moduleName "openpyxl" -moduleVersions "3.1.3"
InstallPythonModule -moduleName "prettytable" -moduleVersions "3.15.1"
InstallPythonModule -moduleName "colorama" -moduleVersions "0.4.6"
InstallPythonModule -moduleName "google-api-python-client" -moduleVersions "2.166.0"

# Test install
pyenv version

echo `n
Write-Host "Install finished" -foreground green

pause