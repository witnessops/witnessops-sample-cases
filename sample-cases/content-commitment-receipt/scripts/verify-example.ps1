$ErrorActionPreference = "Stop"
$SampleDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

if (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonExe = "py"
    $PythonPrefix = @("-3")
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $PythonExe = "python3"
    $PythonPrefix = @()
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonExe = "python"
    $PythonPrefix = @()
} else {
    throw "Python 3.9 or newer is required"
}

& $PythonExe @PythonPrefix (Join-Path $SampleDir "tools/sample_content_commitment.py") verify `
    --artifact (Join-Path $SampleDir "lifecycle/01-pre-disclosure/example-agreement.txt") `
    --receipt (Join-Path $SampleDir "lifecycle/02-public-commitment/receipt.json") `
    --disclosure (Join-Path $SampleDir "lifecycle/03-disclosure/disclosure.json")
