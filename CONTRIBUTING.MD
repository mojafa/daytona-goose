# Contributing to Daytona-Goose-OpenAI Integration

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please help keep this project open and inclusive. By participating, you agree to:
- Be respectful and inclusive in your language and actions
- Be patient with new contributors
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Setting Up Your Development Environment

1. **Fork the repository**:
   Click the "Fork" button in the top right of the repository page.

2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/daytona-goose.git
   cd daytona-goose
   ```

3. **Set up a development environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e ".[dev]"
   ```

4. **Configure your environment**:
   Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   DAYTONA_API_KEY=your_daytona_api_key
   DAYTONA_SERVER_URL=https://app.daytona.io/api
   DAYTONA_TARGET=us
   ```

5. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

This project follows standard Python style guidelines:
- We use [Black](https://github.com/psf/black) for code formatting
- We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Docstrings should follow the [Google docstring format](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

To format your code:
```bash
black src/ tests/
```

### Testing

Before submitting code, please run the tests:
```bash
pytest
```

Write tests for new functionality. We use pytest for testing.

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Create a pull request** with a clear description:
   - What does this PR do?
   - Any specific implementation details?
   - Any issues this addresses?

### Commit Guidelines

- Use clear, descriptive commit messages
- Start with a verb in the present tense (e.g., "Add feature" not "Added feature")
- Reference issue numbers if applicable
- Keep commits focused on a single task

## Feature Requests and Bug Reports

### Submitting Feature Requests

Feature requests are welcome! Please provide:
- A clear description of the feature
- The problem it solves
- Any implementation ideas you have

### Reporting Bugs

When reporting bugs, please include:
- A clear description of the bug
- Steps to reproduce it
- Expected behavior vs. actual behavior
- Your environment details (OS, Python version, etc.)
- Screenshots if applicable

## Project Structure

Understanding the project structure will help you contribute effectively:

```
daytona-goose/
├── pyproject.toml        # Project metadata and dependencies
├── src/                  # Source code
│   └── daytona_goose/    # Main package
│       ├── __init__.py   # Package initialization
│       ├── daytona_executor.py # Core Daytona integration
│       ├── goose_handler.py   # Goose integration handler
│       └── utils.py     # Utility functions
├── tests/                # Test directory
│   ├── conftest.py       # Test fixtures
│   ├── test_executor.py  # Tests for executor
│   └── test_utils.py     # Tests for utilities
└── docs/                # Documentation
```

## Release Process

The maintainers will handle releases following this process:
1. Update version in `pyproject.toml`
2. Update changelog
3. Create release tag
4. Build and publish package

## Documentation

Good documentation is essential. Please update:
- Module and function docstrings in code
- README.md for user-facing changes
- Architecture documentation for significant changes

## Questions?

If you have questions about contributing, please open an issue or contact the project maintainers.

Thank you for contributing to the Daytona-Goose-OpenAI Integration!