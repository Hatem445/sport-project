#!/usr/bin/env pwsh

# Script to push code to GitHub
$gitPath = "C:\Program Files\Git\bin\git.exe"

# Set working directory
Set-Location "C:\Users\ALANDALUS\Desktop\VAS\PYTH"

# Check current status
Write-Host "Checking git status..."
& $gitPath status

# Add all files
Write-Host "`nAdding all files..."
& $gitPath add .

# Commit
$commitMessage = "Update: Push to GitHub repository"
Write-Host "`nCommitting with message: $commitMessage"
& $gitPath commit -m $commitMessage

# Push to origin main
Write-Host "`nPushing to GitHub..."
& $gitPath push -u origin main

Write-Host "`nDone!"
