import subprocess

# Execute the factorial.py script and print the output
result = subprocess.run(['python3', 'factorial.py'], capture_output=True, text=True)
print(result.stdout)