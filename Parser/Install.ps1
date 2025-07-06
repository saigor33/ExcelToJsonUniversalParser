Function LogStep {
	param (
		[int]$stepNumber,
		[string]$message
	)
	
	Write-Host "Step ${stepNumber}: ${message}" -foreground green
}

Function InstallPythonModule {
	param (
		[int]$stepNumber,
		[string]$moduleName,
		[string]$moduleVersions
	)
	
	LogStep -stepNumber $stepNumber -message "Install python module `"${moduleName}`" v.${moduleVersions}"
	pip install $moduleName==$moduleVersions
	Write-Host "Python module `"$moduleName`" installed" -foreground green -nonewline
	echo `n
}

$ErrorActionPreference = "Inquire"

# Fix execute PowerShell policy
& "$PSScriptRoot/FixExecutePowerShellPolicy.ps1"

$stepNumber = 1;
$installationSubScriptsPath = "./InstallationSubScripts/"

if(-not(Test-Path -Path $installationSubScriptsPath))
{
	mkdir $installationSubScriptsPath
}

# Install pyenv
LogStep -stepNumber $stepNumber -message "Install penv"
$installPyenvFilePath = $installationSubScriptsPath +"install-pyenv-win.ps1"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile $installPyenvFilePath
&$installPyenvFilePath
write-host "Istall penv finished!" -foreground green -nonewline
echo `n

$stepNumber++;

# Set Envarament variables
LogStep -stepNumber $stepNumber -message "Add Envarament variables"
& "$PSScriptRoot/SetEnvaramentVariables.ps1"

$stepNumber++;

# Pyenv update cache
LogStep -stepNumber $stepNumber -message "Update pyenv cache"
pyenv update
Write-Host "Pyenv cache updated" -foreground green -nonewline
echo `n

$stepNumber++;

# Install Python 3.9.11
LogStep -stepNumber $stepNumber -message "Install python 3.9.11"
pyenv install 3.9.11
Write-Host "Python 3.9.11 installed" -foreground green -nonewline
echo `n

$stepNumber++;

# Select python version in pyenv
LogStep -stepNumber $stepNumber -message "Select python version 3.9.11 in pyenv"
pyenv global 3.9.11
Write-Host "Python version 3.9.11 selected" -foreground green -nonewline
echo `n

$stepNumber++;

# Install pip
LogStep -stepNumber $stepNumber -message "Install pip"
$installPipFilePath = $installationSubScriptsPath +"get-pip.py"
Invoke-WebRequest -UseBasicParsing -Uri  https://bootstrap.pypa.io/pip/3.7/get-pip.py -OutFile $installPipFilePath
python $installPipFilePath
Write-Host "Pip installed!" -foreground green -nonewline
echo `n

$stepNumber++;

$pythonModuleVersionsByModuleName = @{
	"numpy"="1.20.3";
	"pandas"="1.5.2";
	"openpyxl"="3.1.3"
	"prettytable"="3.15.1"
	"colorama"="0.4.6"
	"google-api-python-client"="2.166.0"
}

foreach ($kv in $pythonModuleVersionsByModuleName.GetEnumerator()) {
	$moduleNmae=$kv.Name;
	$modulVersion=$kv.Value
	InstallPythonModule -stepNumber $stepNumber -moduleName $moduleNmae -moduleVersions $modulVersion
	$stepNumber++;
}

# Test install
pyenv version

echo `n
Write-Host "Install finished" -foreground green

pause