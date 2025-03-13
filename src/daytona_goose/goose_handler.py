#!/usr/bin/env python3
"""
Handler script for Goose integration
"""
import os
import sys
import tempfile
from .daytona_executor import execute_in_workspace

def handle_goose_request(code: str) -> str:
    """
    Handle code execution request from Goose
    
    Args:
        code: Python code to execute
        
    Returns:
        Execution result
    """
    # Set environment flag for automatic cleanup
    os.environ['DAYTONA_AUTO_CLEANUP'] = 'true'
    
    # Execute code with automatic cleanup
    result = execute_in_workspace(code, cleanup=True)
    
    # Return output
    return result.get('output', '')

def main():
    """Command-line entry point"""
    if len(sys.argv) > 1:
        # Code from command line argument
        code = sys.argv[1]
    else:
        # Read from stdin
        code = sys.stdin.read()
    
    if not code:
        print("No code provided")
        return 1
    
    # Execute and print results
    output = handle_goose_request(code)
    print(output)
    return 0

if __name__ == "__main__":
    sys.exit(main())