New-Item .\build\ -Name "lib" -ItemType "directory" -Force
Get-ChildItem -Path .\build\lib | Remove-Item -Recurse -Confirm:$false -Force

New-Item -ItemType Directory -Force -Path .\dist
python .\build\setup.py bdist_wheel