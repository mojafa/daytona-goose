# Goose + Daytona SDK Integration

This example demonstrates how to integrate [Goose](https://github.com/block/goose) with the Daytona SDK to enable AI-assisted development environment management.

## What is Goose?

Goose is an open source, extensible AI agent that goes beyond code suggestions. It allows you to install, execute, edit, and test with any LLM. Goose can be extended with custom command handlers to interact with various development tools and services.

## What is Daytona?

[Daytona](https://www.daytona.io/) is a platform for managing cloud development environments. Its SDK allows programmatic control of workspaces, making it ideal for AI agent integration.

## Features of this Integration

This integration adds the following commands to Goose:

- `daytona:list-workspaces` - Lists all available Daytona workspaces
- `daytona:create-workspace <name> <git_url>` - Creates a new workspace from a Git repository
- `daytona:delete-workspace <name>` - Deletes a workspace
- `daytona:start-workspace <name>` - Starts a stopped workspace

## Prerequisites

- Python 3.8+
- Goose installed (`pip install goose-agent`)
- Daytona SDK installed (`pip install daytona-sdk`)
- Daytona account with API key
- OpenAI API key (or another supported LLM provider)

## Setup

1. Set the required environment variables:
   ```bash
   export DAYTONA_API_KEY="your_daytona_api_key"
   export OPENAI_API_KEY="your_openai_api_key"
   ```

2. Run the example:
   ```bash
   python goose_daytona_example.py
   ```

## Example Usage

Once the Goose agent is running with Daytona integration, you can use natural language to manage your development environments:

```
> I need to work on the project at https://github.com/username/repo. Can you set up a workspace for me?

Sure, I'll create a new Daytona workspace for that repository.
Executing: daytona:create-workspace user-repo https://github.com/username/repo
Workspace 'user-repo' created successfully. ID: ws-12345

> Show me my workspaces

Executing: daytona:list-workspaces
Available workspaces:
1. user-repo (⚫ Stopped) - https://github.com/username/repo

> Please start my user-repo workspace

Executing: daytona:start-workspace user-repo
Workspace 'user-repo' started successfully.
```

## How It Works

The integration uses a custom `DaytonaCommandHandler` class that extends Goose's `CommandHandler`. This handler intercepts Daytona-related commands and uses the Daytona SDK to perform the requested operations.

## Extending Further

You can extend this integration to support more Daytona features:
- Add commands for managing workspace configurations
- Implement workspace sharing functionality
- Add support for different cloud providers
- Integrate with Goose's file editing capabilities to modify code in Daytona workspaces

## Contributing

Contributions to improve this integration are welcome. Please feel free to submit pull requests or open issues.