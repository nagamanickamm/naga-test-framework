Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

if(!$Env:path.Contains("chocolatey")){
    [System.Environment]::SetEnvironmentVariable('ChocolateyToolsLocation','C:\tools',[System.EnvironmentVariableTarget]::Machine)
    [System.Environment]::SetEnvironmentVariable('ChocolateyInstall','C:\ProgramData\chocolatey',[System.EnvironmentVariableTarget]::Machine)
    [Environment]::SetEnvironmentVariable("PATH", $Env:PATH + ";C:\ProgramData\chocolatey\bin;C:\Python310;C:\Python310\Scripts;C:\Program Files\Gauge\bin", [EnvironmentVariableTarget]::Machine)
    $Env:ChocolateyToolsLocation = [System.Environment]::GetEnvironmentVariable("ChocolateyToolsLocation","Machine") 
    $Env:ChocolateyInstall = [System.Environment]::GetEnvironmentVariable("ChocolateyInstall","Machine") 
    
    $Env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") 
    Write-Output $Env:ChocolateyToolsLocation
    Write-Output $Env:ChocolateyInstall
    Write-Output $Env:PATH
}

choco install --no-progress --confirm python --version=3.10.0 --force

choco install --no-progress --confirm gauge --force