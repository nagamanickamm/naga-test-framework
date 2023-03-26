if (!$Env:path.Contains("Python")) {
    [Environment]::SetEnvironmentVariable("PATH", $Env:PATH + ";C:\Python310;C:\Python310\Scripts;", [EnvironmentVariableTarget]::Machine)
    $Env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") 
    Write-Output $Env:PATH
}

# Expand-Archive -Path tools\plugins.zip -DestinationPath C:\Users\ta_igs_neonbuild\AppData\Roaming\gauge -Force

# pip install --find-links=.\dist --no-index neon-test-framework --force
python -m venv ./env
.\env\Scripts\activate

pip uninstall -y neon-test-framework

tools\gauge.exe uninstall python
tools\gauge.exe install python --file tools\gauge-python-0.3.17.zip

pip install -r .\neon\requirements.txt --no-index --find-links .\dependencies --upgrade

Set-Variable -Name "FLASK_APP" -Value "Demo"
Set-Variable -Name "FLASK_ENV" -Value "development"

Start-Process flask -ArgumentList "--app", "neon\test\test_support\demo_api.py", "run", "--port", "5000" -Verb Open
Start-Process python -ArgumentList "-u", "neon\test\test_support\websockets_demo.py" -Verb Open

tools\gauge.exe run .\neon\test\functional_tests\demo\test_suite\features\specs\unit --env="azure"

deactivate