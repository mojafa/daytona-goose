#!/usr/bin/env python3
"""
Simple direct executor for Daytona - avoids module import issues
"""
import os
import sys
import json
import time
import signal
import tempfile
import threading
import subprocess
from pathlib import Path
from typing import Dict, Any

# Set environment variable to auto-cleanup
os.environ["DAYTONA_AUTO_CLEANUP"] = "true"

def show_spinner():
    """Show a spinner while processing"""
    spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    for char in spinner_chars:
        sys.stdout.write(char)
        sys.stdout.flush()
        sys.stdout.write('\b')
        time.sleep(0.1)

def execute_in_daytona(code: str) -> Dict[str, Any]:
    """
    Execute Python code in Daytona directly using subprocess
    
    Args:
        code: The Python code to execute
        
    Returns:
        Dictionary with execution results
    """
    # Write code to a temporary file
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            temp_file = f.name
            f.write(code)
        
        print("\n📁 Creating Daytona workspace...")
        
        # Call daytona_executor module, but using subprocess to avoid import issues
        cmd = [sys.executable, "-m", "daytona_goose.daytona_executor", temp_file]
        
        # Execute and capture output
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Process the output
        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if result.stderr else None,
            "exit_code": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "output": f"Execution error: {str(e)}",
            "error": str(e),
            "exit_code": 1
        }
    finally:
        # Clean up temp file
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except:
                pass

def main():
    """Command-line entry point"""
    try:
        # Get the code
        if len(sys.argv) > 1:
            # If file exists, read from file
            if os.path.exists(sys.argv[1]):
                with open(sys.argv[1], 'r') as f:
                    code = f.read()
            else:
                # Otherwise it's the code directly
                code = sys.argv[1]
        else:
            # Read code from stdin
            code = sys.stdin.read()
        
        if not code:
            print("No code provided")
            return 1
        
        # Execute in Daytona
        result = execute_in_daytona(code)
        
        # Print the result
        if result["error"]:
            print(f"Error: {result['error']}")
        
        if result["output"]:
            print(result["output"])
        
        return 0 if result["success"] else 1
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())