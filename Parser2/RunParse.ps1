# Set Envarament variables
& "$PSScriptRoot/SetEnvaramentVariables.ps1"

$json_config_file_path = (Get-Location).Path + "\Example\Config.json"
Write-Host "config_file_path=" $json_config_file_path
echo `n

cd .\PythonScripts
python .\main.py --config_path $json_config_file_path --print_stacktrace false

cd ..

pause