#!/usr/bin/env python3
"""
Demo script showing how to use the daytona_goose package
"""
import os
import sys
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

# Import package functionality
from daytona_goose import execute_in_workspace
from daytona_goose.utils import generate_code

def run_example():
    """Run a simple example using the package"""
    print("🚀 Daytona-Goose Demo")
    print("=====================")
    
    # Option 1: Execute pre-written code
    example_code = """
def greet(name="World"):
    return f"Hello, {name} from Daytona sandbox!"

print(greet())
print(greet("User"))

# Show Python version
import sys
print(f"Python version: {sys.version}")
"""

    print("\n📝 Executing pre-written code in Daytona...")
    result = execute_in_workspace(example_code, cleanup=False)
    
    print("\nExecution result:")
    print("-----------------")
    print(result["output"])
    
    # Option 2: Generate and execute code
    prompt = "Write a function that calculates the nth Fibonacci number"
    
    print("\n🤖 Generating code with OpenAI...")
    generated_code = generate_code(prompt)
    
    if generated_code:
        print("\nGenerated code:")
        print("--------------")
        print(generated_code)
        
        print("\n🧪 Executing generated code in Daytona...")
        result = execute_in_workspace(generated_code, cleanup=True)
        
        print("\nExecution result:")
        print("-----------------")
        print(result["output"])
    else:
        print("❌ Failed to generate code")

if __name__ == "__main__":
    run_example()