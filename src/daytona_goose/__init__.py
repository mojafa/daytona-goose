"""
Daytona-Goose-OpenAI integration package

This package provides tools to:
1. Create and manage Daytona workspaces
2. Execute code in sandboxed environments
3. Integrate with Goose AI for testing
"""

__version__ = "0.1.0"

from .daytona_executor import WorkspaceManager, execute_in_workspace
from .goose_handler import handle_goose_request
from .utils import generate_code, load_environment