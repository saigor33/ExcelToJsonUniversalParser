$ErrorActionPreference = "Inquire"
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

# Install numpy
Write-Host "Step 7: Install python module `"numpy`" v.1.20.3"
pip install numpy==1.20.3
Write-Host "Python module `"numpy`" installed" -foreground green -nonewline

# Setup pandas
Write-Host "Step 8: Install python module `"pandas`" v.1.5.2"
pip install pandas==1.5.2
Write-Host "Python module `"pandas`" installed" -foreground green -nonewline
echo `n

# Setup openpyxl
Write-Host "Step 9: Install python module `"openpyxl`" v.3.1.3"
pip install openpyxl==3.1.3
Write-Host "Python module `"openpyxl`" installed" -foreground green -nonewline
echo `n

# Setup PrettyTable
Write-Host "Step 9: Install python module `"PrettyTable`" v.3.15.1"
pip install prettytable==3.15.1
Write-Host "Python module `"PrettyTable`" installed" -foreground green -nonewline
echo `n

# Setup PrettyTable
Write-Host "Step 9: Install python module `"colorama`" v.0.4.6"
pip install colorama==0.4.6
Write-Host "Python module `"colorama`" installed" -foreground green -nonewline
echo `n

Write-Host "Step 9: Install python module `"google-api-python-client`" v. 2.166.0"
pip install google-api-python-client==2.166.0
Write-Host "Python module `" google-api-python-client`" installed" -foreground green -nonewline
echo `n

Write-Host "Step 9: Install python module `"google-auth-oauthlib`" v. 1.2.1"
pip install google-auth-oauthlib==1.2.1
Write-Host "Python module `"google-auth-oauthlib`" installed" -foreground green -nonewline
echo `n

# Test install
pyenv version

echo `n
Write-Host "Install finished" -foreground green

pause