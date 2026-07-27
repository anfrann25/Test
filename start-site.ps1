Set-Location $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) { py serve.py }
elseif (Get-Command python -ErrorAction SilentlyContinue) { python serve.py }
else { Write-Error "Python 3 is required." }
