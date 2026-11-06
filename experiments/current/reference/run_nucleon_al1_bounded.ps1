param(
    [Parameter(Mandatory = $true)][string]$Python,
    [Parameter(Mandatory = $true)][ValidateSet('nucleon', 'delta')][string]$Sector,
    [Parameter(Mandatory = $true)][ValidatePattern('^[A-Za-z0-9_-]+\.json$')][string]$OutputName
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../..')).Path
$pythonPath = (Resolve-Path -LiteralPath $Python).Path
$reportDirectory = Join-Path $root 'reports/reference'
$outputPath = Join-Path $reportDirectory $OutputName
$stdoutPath = "$outputPath.stdout.log"
$stderrPath = "$outputPath.stderr.log"

foreach ($path in @($outputPath, $stdoutPath, $stderrPath)) {
    if (Test-Path -LiteralPath $path) {
        throw "Refusing to replace an existing attempt: $path"
    }
}
if (-not (Test-Path -LiteralPath $reportDirectory -PathType Container)) {
    throw 'Expected reports/reference directory is missing.'
}

$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$arguments = @(
    '-m', 'experiments.current.reference.nucleon_gaussian_run',
    '--mode', 'al1', '--sector', $Sector,
    '--output', "reports/reference/$OutputName"
)

# This solver creates no child processes; the parent owns its hard deadline.
$process = Start-Process -FilePath $pythonPath -ArgumentList $arguments `
    -WorkingDirectory $root -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
try {
    if (-not $process.WaitForExit(300000)) {
        $process.Kill()
        $process.WaitForExit()
        Write-Output "INCONCLUSIVE: hard 300-second limit; retain partial output and logs."
        exit 124
    }
    # Refresh redirected streams and ExitCode before returning to the caller.
    $process.WaitForExit()
    Write-Output "Sector=$Sector ExitCode=$($process.ExitCode) Output=$outputPath"
    exit $process.ExitCode
}
finally {
    if (-not $process.HasExited) {
        $process.Kill()
        $process.WaitForExit()
    }
    $process.Dispose()
}
