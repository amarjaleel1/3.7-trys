import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and print the output"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False

def initialize_git():
    """Initialize git repository and make first commit"""
    # Check if git is installed
    if not run_command("git --version"):
        print("Git is not installed. Please install git first.")
        return False
    
    # Initialize a new git repository
    if not run_command("git init"):
        return False
    
    # Add all files
    if not run_command("git add ."):
        return False
    
    # Make the initial commit
    if not run_command('git commit -m "Initial commit of CPU Pipeline Simulator"'):
        return False
    
    print("\nRepository initialized successfully!")
    print("\nTo connect to a remote GitHub repository, run:")
    print("git remote add origin https://github.com/yourusername/cpu-pipeline-simulator.git")
    print("git branch -M main")
    print("git push -u origin main")
    
    return True

if __name__ == "__main__":
    # Change to the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Initializing Git repository for CPU Pipeline Simulator...")
    initialize_git()
