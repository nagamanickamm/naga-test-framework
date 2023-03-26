$username = Read-Host 'Enter - Username'
$pat = Read-Host 'Enter - PAT'
pip install --upgrade --index-url https://${username}:${pat}@tfs.engineering.intelligentgaming.net/tfs/Neon-Collection/_packaging/Neon/pypi/simple -r neon\requirements.txt