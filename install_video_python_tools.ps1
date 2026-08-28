param(
    [string]$BootstrapPython = ""
)

$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $workspaceRoot ".venv-video"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

# Auto-detect Bootstrap Python from PATH if not provided
if (-not $BootstrapPython) {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($pythonCmd) {
        $BootstrapPython = $pythonCmd.Source
    } else {
        $pyCmd = Get-Command py -ErrorAction SilentlyContinue
        if ($pyCmd) {
            $BootstrapPython = $pyCmd.Source
        }
    }
}

if (-not $BootstrapPython -or -not (Test-Path -LiteralPath $BootstrapPython)) {
    throw "Bootstrap Python was not found. Please install Python 3.10+ and ensure 'python' is in your PATH, or pass -BootstrapPython 'C:\path\to\python.exe'."
}

Write-Host "Using bootstrap Python: $BootstrapPython"

if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Host "Creating virtual environment at $venvPath"
    & $BootstrapPython -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create the virtual environment at $venvPath."
    }
}

Write-Host "Updating Python packaging tools (pip, setuptools, wheel)"
& $venvPython -m pip install --disable-pip-version-check --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    throw "Failed to update Python packaging tools."
}

Write-Host "Installing Google Drive download, transcription, and scene detection packages"
& $venvPython -m pip install --disable-pip-version-check --upgrade gdown faster-whisper "scenedetect[opencv]"
if ($LASTEXITCODE -ne 0) {
    throw "Failed to install one or more video packages."
}

Write-Host "Verifying imports and installed versions"
& $venvPython -c "import cv2, faster_whisper, gdown, scenedetect; import importlib.metadata as metadata; packages=['gdown','faster-whisper','scenedetect','opencv-python']; print('Python tools ready:'); [print(f'  {name}={metadata.version(name)}') for name in packages]"
if ($LASTEXITCODE -ne 0) {
    throw "Package installation completed, but import verification failed."
}

Write-Host "---------------------------------------------------------"
Write-Host "SUCCESS: Video Python tools environment is ready!"
Write-Host "Virtual environment Python: $venvPython"
Write-Host "---------------------------------------------------------"
