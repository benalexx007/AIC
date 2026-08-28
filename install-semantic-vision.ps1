param(
    [string]$BootstrapPython = "C:\Users\DINH HUNG\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe",
    [string]$EnvironmentPath = "D:\AIC\.venv-semantic",
    [string]$ModelsPath = "D:\AIC\models\semantic",
    [string]$YoloModel = "yolo26n.pt",
    [string]$ClipModel = "ViT-B-32",
    [string]$ClipPretrained = "laion2b_s34b_b79k",
    [double]$MinimumFreeGB = 10,
    [switch]$SkipModelDownload,
    [switch]$KeepPipCache
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$smokeTest = Join-Path $workspaceRoot "semantic_vision_smoke_test.py"
$environmentPython = Join-Path $EnvironmentPath "Scripts\python.exe"
$reportPath = Join-Path $workspaceRoot "semantic-install-report.json"
$logPath = Join-Path $workspaceRoot "semantic-install.log"
$xpuIndex = "https://download.pytorch.org/whl/xpu"

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)][string]$Program,
        [Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments
    )

    Write-Host "RUN $Program $($Arguments -join ' ')"
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code $LASTEXITCODE`: $Program"
    }
}

function Assert-PathUnderWorkspace {
    param([Parameter(Mandatory = $true)][string]$PathToCheck)

    $workspaceFull = [IO.Path]::GetFullPath($workspaceRoot).TrimEnd('\') + '\'
    $candidateFull = [IO.Path]::GetFullPath($PathToCheck).TrimEnd('\') + '\'
    if (-not $candidateFull.StartsWith($workspaceFull, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Path must remain under $workspaceRoot`: $PathToCheck"
    }
}

Assert-PathUnderWorkspace -PathToCheck $EnvironmentPath
Assert-PathUnderWorkspace -PathToCheck $ModelsPath

if (-not (Test-Path -LiteralPath $BootstrapPython -PathType Leaf)) {
    throw "Bootstrap Python was not found: $BootstrapPython"
}
if (-not (Test-Path -LiteralPath $smokeTest -PathType Leaf)) {
    throw "Smoke-test script was not found: $smokeTest"
}

$driveRoot = [IO.Path]::GetPathRoot([IO.Path]::GetFullPath($EnvironmentPath))
$driveInfo = [IO.DriveInfo]::new($driveRoot)
$freeGB = [math]::Round($driveInfo.AvailableFreeSpace / 1GB, 2)
Write-Host "Free space on $driveRoot`: $freeGB GB"
if ($freeGB -lt $MinimumFreeGB) {
    throw "At least $MinimumFreeGB GB free is required before installation."
}

Start-Transcript -Path $logPath -Force | Out-Null
try {
    if (-not (Test-Path -LiteralPath $environmentPython -PathType Leaf)) {
        Write-Host "Creating isolated semantic-vision environment at $EnvironmentPath"
        Invoke-Checked -Program $BootstrapPython -Arguments @("-m", "venv", $EnvironmentPath)
    }

    Write-Host "Updating packaging tools"
    Invoke-Checked -Program $environmentPython -Arguments @("-m", "pip", "install", "--disable-pip-version-check", "--upgrade", "pip", "setuptools", "wheel")

    Write-Host "Installing official PyTorch XPU wheels for Intel Arc"
    Invoke-Checked -Program $environmentPython -Arguments @("-m", "pip", "install", "--disable-pip-version-check", "--upgrade", "torch", "torchvision", "--index-url", $xpuIndex)

    Write-Host "Installing semantic retrieval, detection, and clustering packages"
    Invoke-Checked -Program $environmentPython -Arguments @("-m", "pip", "install", "--disable-pip-version-check", "--upgrade-strategy", "only-if-needed", "open_clip_torch", "ultralytics", "scikit-learn")

    Write-Host "Checking dependency consistency"
    Invoke-Checked -Program $environmentPython -Arguments @("-m", "pip", "check")

    $smokeArguments = @(
        $smokeTest,
        "--models-dir", $ModelsPath,
        "--yolo-model", $YoloModel,
        "--clip-model", $ClipModel,
        "--clip-pretrained", $ClipPretrained,
        "--report", $reportPath
    )
    if (-not $SkipModelDownload) {
        $smokeArguments += "--download-models"
    }

    Write-Host "Running import, XPU, model-load, and inference checks"
    Invoke-Checked -Program $environmentPython -Arguments $smokeArguments

    if (-not $KeepPipCache) {
        Write-Host "Removing the reproducible pip download cache to save disk space"
        Invoke-Checked -Program $environmentPython -Arguments @("-m", "pip", "cache", "purge")
    }

    Write-Host "Semantic-vision installation completed successfully."
    Write-Host "Python: $environmentPython"
    Write-Host "Models: $ModelsPath"
    Write-Host "Report: $reportPath"
    Write-Host "Log: $logPath"
}
finally {
    Stop-Transcript | Out-Null
}
