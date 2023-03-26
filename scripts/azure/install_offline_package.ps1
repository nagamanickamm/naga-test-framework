Write-Output $Env:PATH

Write-Output "Update"

if(!$Env:path.Contains("Python")){
    [Environment]::SetEnvironmentVariable("PATH", $Env:PATH + ";C:\Python310;C:\Python310\Scripts;C:\Program Files\Gauge\bin", [EnvironmentVariableTarget]::Machine)
    $Env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") 
    Write-Output $Env:PATH
}

pip install -r .\neon\requirements.txt --no-index --find-links .\dependencies

$env:HTTPS_PROXY="http://10.44.33.10:8080"

python -m playwright install