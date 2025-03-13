#!/usr/bin/env python3
"""
Factorial function example for Daytona execution
"""

def factorial(n: int) -> int:
    """
    Calculate the factorial of a non-negative integer.
    
    Args:
        n: The number to calculate factorial for
        
    Returns:
        The factorial of n
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def main():
    """Calculate and print factorials of numbers 0-10"""
    print("Factorial Calculator:")
    print("=====================")
    
    for i in range(11):
        result = factorial(i)
        print(f"{i}! = {result}")
    
    # Test a larger number
    n = 20
    print(f"\nFactorial of {n} is: {factorial(n)}")

if __name__ == "__main__":
    main()