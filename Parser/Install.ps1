$ErrorActionPreference = "Inquire"
$installationSubScriptsPath = "./InstallationSubScripts/"

if(-not(Test-Path -Path $installationSubScriptsPath))
{
	mkdir $installationSubScriptsPath
}

# Install pyenv
echo "Step 1: Install penv stage"
$installPyenvFilePath = $installationSubScriptsPath +"install-pyenv-win.ps1"
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile $installPyenvFilePath
&$installPyenvFilePath
write-host "Istall penv finished!" -foreground green -nonewline
echo `n

# Set Envarament variables
Write-Host "Step 2: Add Envarament variables"
& "$PSScriptRoot/SetEnvaramentVariables.ps1"

# Install Python 3.7.4
Write-Host "Step 3: Install python 3.7.4"
pyenv install 3.7.4
Write-Host "Python 3.7.4 installed" -foreground green -nonewline
echo `n

# Select python version in pyenv
Write-Host "Step 4: Select python version 3.7.4 in pyenv"
pyenv global 3.7.4
Write-Host "Python version 3.7.4 selected" -foreground green -nonewline
echo `n

# Install pip
Write-Host "Step 5: Install pip"
$installPipFilePath = $installationSubScriptsPath +"get-pip.py"
Invoke-WebRequest -UseBasicParsing -Uri  https://bootstrap.pypa.io/pip/3.7/get-pip.py -OutFile $installPipFilePath
python $installPipFilePath
Write-Host "Pip installed!" -foreground green -nonewline
echo `n

# Setup pandas
Write-Host "Step 6: Install python module `"pandas`" v.1.3.5"
pip install pandas==1.3.5
Write-Host "Python module `"pandas`" installed" -foreground green -nonewline
echo `n

# Setup openpyxl
Write-Host "Step 7: Install python module `"openpyxl`" v.3.1.3"
pip install openpyxl==3.1.3
Write-Host "Python module `"openpyxl`" installed" -foreground green -nonewline
echo `n

# Test install
pyenv version

echo `n
Write-Host "Install finished" -foreground green

pause