# PowerShell script to invoke the photo importer via uv
$modearg = "--cam=panasonic"
$pythonScript = "photo_importer.py"

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: uv is not installed or not on PATH. Install from https://docs.astral.sh/uv/"
    exit 1
}

if (Test-Path $pythonScript) {
    Write-Host "Invoking Python script via uv: $pythonScript"

    & uv run $pythonScript $modearg

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python script executed successfully."
    } else {
        Write-Host "Python script execution failed with exit code: $LASTEXITCODE"
    }
} else {
    Write-Host "Error: Python script not found at $pythonScript"
}
