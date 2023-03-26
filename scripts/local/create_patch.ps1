git diff > change.patch
Get-Content change.patch | Set-Content -Encoding utf8 change_new.patch