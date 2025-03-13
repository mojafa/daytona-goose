def calculate_factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * calculate_factorial(n-1)

for i in range(10):
    print(f"{i}! = {calculate_factorial(i)}")