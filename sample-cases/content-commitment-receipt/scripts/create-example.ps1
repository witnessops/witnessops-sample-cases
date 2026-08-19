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

& $PythonExe @PythonPrefix (Join-Path $SampleDir "tools/sample_content_commitment.py") commit `
    --artifact (Join-Path $SampleDir "lifecycle/01-pre-disclosure/example-agreement.txt") `
    --artifact-label "example-agreement.txt" `
    --claimed-created-at "2026-08-19T05:30:00Z" `
    --nonce-hex "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f" `
    --receipt (Join-Path $SampleDir "lifecycle/02-public-commitment/receipt.json") `
    --opening-record (Join-Path $SampleDir "lifecycle/01-pre-disclosure/opening-record.json") `
    --force

& $PythonExe @PythonPrefix (Join-Path $SampleDir "tools/sample_content_commitment.py") disclose `
    --receipt (Join-Path $SampleDir "lifecycle/02-public-commitment/receipt.json") `
    --opening-record (Join-Path $SampleDir "lifecycle/01-pre-disclosure/opening-record.json") `
    --disclosure (Join-Path $SampleDir "lifecycle/03-disclosure/disclosure.json") `
    --force

Write-Output "SAMPLE_REGENERATED=PASS"
