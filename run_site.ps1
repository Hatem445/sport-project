# PowerShell script to launch the FitLife AI server and open the browser
# Usage: right‑click and "Run with PowerShell" or execute from a PowerShell prompt.

# change to project directory (script location)
Push-Location -Path $PSScriptRoot

# activate virtual environment if present
if (Test-Path .\venv\Scripts\Activate.ps1) {
    Write-Host "Activating virtual environment..."
    . .\venv\Scripts\Activate.ps1
} else {
    Write-Host "No virtual environment found, continuing with system Python."
}

# start the Flask server in the current shell so the logs are visible here
Write-Host "Starting Flask server on http://localhost:5000..."

# run python app.py and start listening in background job
$job = Start-Job -ScriptBlock { python app.py }

# wait until the server is actually listening on port 5000
Write-Host "Waiting for server to accept connections..."
$maxWait = 30  # seconds
$elapsed = 0
while ($elapsed -lt $maxWait) {
    $conn = Test-NetConnection -ComputerName localhost -Port 5000
    if ($conn.TcpTestSucceeded) {
        Write-Host "Server is up (elapsed ${elapsed}s)"
        break
    }
    Start-Sleep -Seconds 1
    $elapsed++
}
if ($elapsed -ge $maxWait) {
    Write-Host "Warning: server did not start within $maxWait seconds.  Inspect job output."
}

# open default browser to the app URL
Start-Process "http://localhost:5000"

Write-Host "To view server logs, use Get-Job -Id $($job.Id) | Receive-Job -Keep"
# return to original location
Pop-Location
