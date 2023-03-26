if(!$Env:path.Contains("Python")){
    [Environment]::SetEnvironmentVariable("PATH", $Env:PATH + ";C:\Python310;C:\Python310\Scripts;C:\Program Files\Gauge\bin", [EnvironmentVariableTarget]::Machine)
    $Env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") 
    Write-Output $Env:PATH
}

Write-Output $Env:PATH
python -m pip3 install -r $(System.DefaultWorkingDirectory)\neon\requirement.txt