# Daytona-Goose-OpenAI Integration

A secure framework for executing AI-generated code in isolated sandbox environments. This project integrates:

- **[Daytona](https://app.daytona.io)** - A secure, isolated sandbox for code execution
- **[Goose](https://github.com/block/goose-plugins)** - An open source, extensible AI agent that goes beyond code suggestions - install, execute, edit, and test with any LLM
- **[OpenAI](https://openai.com)** - LLM capabilities for code generation

## 🚀 Features

- Execute Python code in secure, isolated Daytona workspaces
- Generate code using OpenAI's models
- Automated workspace creation and cleanup
- Integrates with Goose AI for conversational code execution
- Simple CLI tools for direct execution

## 📋 Requirements

- Python 3.12+
- Daytona account with API key
- OpenAI API key
- Goose AI (optional, for conversational interface)

## 📦 Installation

### Using UV (recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/daytona-goose.git
cd daytona-goose

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/daytona-goose.git
cd daytona-goose

# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## ⚙️ Configuration

Create a `.env` file in the root directory with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
DAYTONA_API_KEY=your_daytona_api_key
DAYTONA_SERVER_URL=https://app.daytona.io/api
DAYTONA_TARGET=us
```

Make the runner script executable:

```bash
chmod +x run_daytona.sh
chmod +x daytona_runner.py
```

## 🖥️ Usage

### Direct Execution

Use the runner script to execute Python code directly in a Daytona sandbox:

```bash
# Run code directly
./run_daytona.sh "print('Hello from Daytona!')"

# Run code from a file
./run_daytona.sh -f examples/factorial.py

# Pipe code to the script
echo "print('Hello from pipe!')" | ./run_daytona.sh
```

### Using Goose (Conversational Interface)

Start a conversation with Goose and ask it to run code in Daytona:

```bash
# Start Goose with our configuration
goose run goose-config.yaml
```

In the Goose session, you can request code execution:

```
Run this Python code in Daytona:

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"fibonacci({i}) = {fibonacci(i)}")
```

Goose will execute the code in a Daytona sandbox and show you the results.

### Demo

Run the included demo to see the integration in action:

```bash
python demo.py
```

## 📁 Project Structure

```
daytona-goose/
├── pyproject.toml        # Project metadata and dependencies
├── .env                  # Environment variables (API keys)
├── goose-config.yaml     # Goose configuration
├── run_daytona.sh        # Shell wrapper for Daytona execution
├── daytona_runner.py     # Direct runner script for Goose integration
├── demo.py               # Demo script showing usage
├── examples/             # Example Python scripts
│   └── factorial.py      # Factorial calculation example
├── src/                  # Source code
│   └── daytona_goose/    # Main package
│       ├── __init__.py   # Package initialization
│       ├── daytona_executor.py # Core Daytona integration
│       ├── goose_handler.py   # Goose integration handler
│       └── utils.py     # Utility functions
└── docs/                # Documentation
    └── architecture-diagram.md # Project architecture
```

## 🛠️ How It Works

1. **Code Execution Flow**:
   - Code is sent to the Daytona executor
   - A secure workspace is created in Daytona cloud
   - Code is uploaded and executed in the sandbox
   - Results are returned to the user
   - Workspace is automatically cleaned up

2. **Integration with Goose**:
   - Goose uses OpenAI to interpret user requests
   - When code execution is requested, Goose calls the Daytona executor
   - Results are displayed back to the user in the Goose session

## 📚 Examples

### Calculate Factorial

```python
def calculate_factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * calculate_factorial(n-1)

for i in range(10):
    print(f"{i}! = {calculate_factorial(i)}")
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.MD](CONTRIBUTING.MD) for details.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💬 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/daytona-goose/issues) on GitHub.