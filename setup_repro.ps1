# PowerShell script to create git repository with 10k files for performance testing

Write-Host "=== Setting up Git Performance Reproduction ===" -ForegroundColor Green

# Step 1: Initialize git repository
Write-Host "`n=== Step 1: Initializing git repository ===" -ForegroundColor Yellow
git init
git config user.name "Test User"
git config user.email "test@example.com"

# Step 2: Create 10,000 files
Write-Host "`n=== Step 2: Creating 10,000 files ===" -ForegroundColor Yellow
for ($i = 0; $i -lt 10000; $i++) {
    $filename = "file_{0:D5}.txt" -f $i
    $content = @"
This is file number $i
Content for testing git performance
File created for reproduction of issue
"@
    Set-Content -Path $filename -Value $content
    
    if (($i + 1) % 1000 -eq 0) {
        Write-Host "Created $($i + 1) files..."
    }
}

Write-Host "All 10,000 files created!" -ForegroundColor Green

# Step 3: Add all files to git
Write-Host "`n=== Step 3: Adding all files to git ===" -ForegroundColor Yellow
git add .

# Step 4: Commit all files
Write-Host "`n=== Step 4: Committing all files ===" -ForegroundColor Yellow
git commit -m "Add 10,000 files for performance testing"

# Step 5: Create subdirectory and move all files
Write-Host "`n=== Step 5: Moving all files to subdirectory ===" -ForegroundColor Yellow
New-Item -ItemType Directory -Name "moved_files" -Force | Out-Null

$txtFiles = Get-ChildItem -Name "file_*.txt"
Write-Host "Moving $($txtFiles.Count) files to subdirectory..."

$counter = 0
foreach ($file in $txtFiles) {
    Move-Item $file "moved_files\"
    $counter++
    
    if ($counter % 1000 -eq 0) {
        Write-Host "Moved $counter files..."
    }
}

Write-Host "All files moved!" -ForegroundColor Green

# Step 6: Add the changes (this should trigger the performance issue)
Write-Host "`n=== Step 6: Adding moved files (this may be slow) ===" -ForegroundColor Yellow
git add .

# Step 7: Commit the move operation
Write-Host "`n=== Step 7: Committing file moves ===" -ForegroundColor Yellow
git commit -m "Move all 10,000 files to subdirectory"

# Show results
Write-Host "`n=== Reproduction setup complete! ===" -ForegroundColor Green
Write-Host "Repository created at: $(Get-Location)"
Write-Host "`nGit log:"
git log --oneline

Write-Host "`nRepository stats:"
$commitCount = git rev-list --count HEAD
Write-Host "Total commits: $commitCount"
$movedFilesCount = (Get-ChildItem "moved_files\*.txt").Count
Write-Host "Files in moved_files directory: $movedFilesCount"
