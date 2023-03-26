if (!$Env:path.Contains("Python")) {
    [Environment]::SetEnvironmentVariable("PATH", $Env:PATH + ";C:\Python310;C:\Python310\Scripts;", [EnvironmentVariableTarget]::Machine)
    $Env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") 
    Write-Output $Env:PATH
}

New-Item .\build\ -Name "lib" -ItemType "directory" -Force
Get-ChildItem -Path .\build\lib | Remove-Item -Recurse -Confirm:$false -Force


New-Item -ItemType Directory -Force -Path .\dist
python .\build\setup.py bdist_wheel