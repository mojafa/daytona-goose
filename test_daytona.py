#!/usr/bin/env python3
"""
Test script for Daytona runner
"""

# Test code to run
test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print("Fibonacci Sequence:")
for i in range(10):
    print(f"fibonacci({i}) = {fibonacci(i)}")
"""

# Import subprocess to run the runner script
import subprocess

print("Testing Daytona runner...")
result = subprocess.run(["python", "daytona_runner.py", test_code], capture_output=True, text=True)

print("\nOutput:")
print("-" * 50)
print(result.stdout)

if result.stderr:
    print("\nErrors:")
    print("-" * 50)
    print(result.stderr)

print(f"\nExit code: {result.returncode}")
