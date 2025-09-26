#!/usr/bin/env python3
"""
Script to create a git repository with 10k files to reproduce performance issues.
This will:
1. Initialize a git repository
2. Create 10,000 small files
3. Commit all files in a single commit
4. Move all files to a new subdirectory (to trigger git operations on many files)
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        raise

def main():
    repo_path = Path.cwd()
    print(f"Setting up reproduction in: {repo_path}")
    
    # Step 1: Initialize git repository
    print("\n=== Step 1: Initializing git repository ===")
    run_command(["git", "init"], cwd=repo_path)
    run_command(["git", "config", "user.name", "Test User"], cwd=repo_path)
    run_command(["git", "config", "user.email", "test@example.com"], cwd=repo_path)
    
    # Step 2: Create 10,000 files
    print("\n=== Step 2: Creating 10,000 files ===")
    for i in range(10000):
        file_path = repo_path / f"file_{i:05d}.txt"
        with open(file_path, 'w') as f:
            f.write(f"This is file number {i}\n")
            f.write(f"Content for testing git performance\n")
            f.write(f"File created for reproduction of issue\n")
        
        if (i + 1) % 1000 == 0:
            print(f"Created {i + 1} files...")
    
    print("All 10,000 files created!")
    
    # Step 3: Add all files to git
    print("\n=== Step 3: Adding all files to git ===")
    run_command(["git", "add", "."], cwd=repo_path)
    
    # Step 4: Commit all files
    print("\n=== Step 4: Committing all files ===")
    run_command(["git", "commit", "-m", "Add 10,000 files for performance testing"], cwd=repo_path)
    
    # Step 5: Create a subdirectory and move all files there
    print("\n=== Step 5: Moving all files to subdirectory ===")
    subdir = repo_path / "moved_files"
    subdir.mkdir(exist_ok=True)
    
    # Move all txt files to the subdirectory
    import shutil
    txt_files = list(repo_path.glob("file_*.txt"))
    print(f"Moving {len(txt_files)} files to subdirectory...")
    
    for i, file_path in enumerate(txt_files):
        new_path = subdir / file_path.name
        shutil.move(str(file_path), str(new_path))
        
        if (i + 1) % 1000 == 0:
            print(f"Moved {i + 1} files...")
    
    print("All files moved!")
    
    # Step 6: Add the changes (this should trigger the performance issue)
    print("\n=== Step 6: Adding moved files (this may be slow) ===")
    run_command(["git", "add", "."], cwd=repo_path)
    
    # Step 7: Commit the move operation
    print("\n=== Step 7: Committing file moves ===")
    run_command(["git", "commit", "-m", "Move all 10,000 files to subdirectory"], cwd=repo_path)
    
    print("\n=== Reproduction setup complete! ===")
    print(f"Repository created at: {repo_path}")
    print("Git log:")
    run_command(["git", "log", "--oneline"], cwd=repo_path)
    
    print(f"\nRepository stats:")
    run_command(["git", "rev-list", "--count", "HEAD"], cwd=repo_path)
    print("Files in moved_files directory:")
    moved_files_count = len(list(subdir.glob("*.txt")))
    print(f"{moved_files_count} files")

if __name__ == "__main__":
    main()
