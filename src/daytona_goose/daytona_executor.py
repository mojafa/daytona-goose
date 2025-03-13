#!/usr/bin/env python3
"""
Daytona workspace management and code execution module
"""
import os
import sys
import json
import time
import signal
import threading
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

from daytona_sdk import CreateWorkspaceParams, Daytona, DaytonaConfig
from dotenv import load_dotenv

# Active workspaces for cleanup
active_workspaces = []

def signal_handler(signum, frame):
    """Handle Ctrl+C to display active workspaces and exit"""
    print("\n\n⚠️ Process cancelled by user")
    if active_workspaces:
        print("Active workspaces will continue running:")
        for workspace in active_workspaces:
            print(f"- Workspace ID: {workspace.id}")
        print("\nYou can clean them up manually later using:")
        print("- The Daytona web interface")
        print("- The Daytona CLI")
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

class Config:
    """Server configuration class that loads environment variables for Daytona setup"""
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv('DAYTONA_API_KEY')
        if not self.api_key:
            raise ValueError("DAYTONA_API_KEY is required")

        self.server_url = os.getenv('DAYTONA_SERVER_URL', 'https://app.daytona.io/api')
        self.target = os.getenv('DAYTONA_TARGET', 'us')
        self.timeout = float(os.getenv('DAYTONA_TIMEOUT', '30.0'))
        self.verify_ssl = os.getenv('VERIFY_SSL', 'false').lower() in ('true', '1', 'yes')

    def get_daytona_config(self):
        """Return a DaytonaConfig object"""
        return DaytonaConfig(
            api_key=self.api_key,
            server_url=self.server_url,
            target=self.target
        )

class WorkspaceManager:
    """Manages Daytona workspaces for code execution"""
    def __init__(self):
        try:
            self.config = Config()
            self.daytona_client = Daytona(config=self.config.get_daytona_config())
            self.temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
            os.makedirs(self.temp_dir, exist_ok=True)
            self.spinner_done = True
        except Exception as e:
            print(f"Error initializing WorkspaceManager: {e}")
            raise

    def show_spinner_until_done(self):
        """Show spinner animation until done flag is set"""
        import itertools
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        while not self.spinner_done:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            sys.stdout.write('\b')
            time.sleep(0.1)

    def create_workspace(self, name="Goose-Daytona") -> Optional[Any]:
        """
        Create a new Daytona workspace
        
        Args:
            name: Name for the workspace
            
        Returns:
            Workspace object or None if creation failed
        """
        try:
            print(f"\n📁 Creating workspace {name}...")
            
            # Show spinner while creating workspace
            self.spinner_done = False
            spinner_thread = threading.Thread(target=self.show_spinner_until_done)
            spinner_thread.start()
            
            workspace_params = CreateWorkspaceParams(
                language="python",
                target=self.config.target,
                name=name
            )
            
            workspace = self.daytona_client.create(workspace_params)
            active_workspaces.append(workspace)
            
            # Wait for workspace to initialize
            time.sleep(3)
            
            # Stop the spinner
            self.spinner_done = True
            spinner_thread.join()
            
            print(f"✅ Workspace created successfully (ID: {workspace.id})")
            return workspace
        except Exception as e:
            self.spinner_done = True
            if 'spinner_thread' in locals():
                spinner_thread.join()
            print(f"❌ Workspace creation error: {e}")
            return None

    def execute_code(self, workspace, code: str, language="python") -> Dict[str, Any]:
        """
        Execute code in the workspace
        
        Args:
            workspace: Daytona workspace object
            code: The code to execute
            language: Programming language of the code
            
        Returns:
            Dictionary with execution results
        """
        try:
            print(f"📝 Deploying code to workspace {workspace.id}...")
            
            # Write code to a temp file
            temp_file = os.path.join(self.temp_dir, f"code_{workspace.id}.{language}")
            os.makedirs(os.path.dirname(temp_file), exist_ok=True)
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Read the temp file
            with open(temp_file, 'rb') as f:
                file_content = f.read()
            
            # Upload to workspace
            remote_path = f"/home/daytona/code.{language}"
            try:
                workspace.fs.upload_file(remote_path, file_content)
                print(f"✅ Code uploaded to {remote_path}")
            except Exception as e:
                print(f"⚠️ File upload failed: {e}")
                # Fall back to process.exec
                workspace.process.exec(f"cat > {remote_path} << 'EOF'\n{code}\nEOF")
            
            # Find Python interpreter
            python_check = workspace.process.exec("which python3 || which python")
            if python_check.exit_code == 0:
                python_path = python_check.result.strip()
            else:
                python_path = "python3"  # Default

            print(f"🧪 Executing code in workspace {workspace.id}...")
            result = workspace.process.exec(f"{python_path} {remote_path} 2>&1")
            
            print(f"Execution result (exit code {result.exit_code}):")
            output = result.result.strip()
            
            return {
                "success": result.exit_code == 0,
                "output": output,
                "exit_code": result.exit_code
            }
        except Exception as e:
            print(f"❌ Execution error: {e}")
            return {
                "success": False,
                "output": str(e),
                "exit_code": 1
            }
        finally:
            # Clean up temp file
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass

    def cleanup_workspace(self, workspace) -> bool:
        """
        Remove a workspace
        
        Args:
            workspace: Daytona workspace object
            
        Returns:
            True if cleanup was successful, False otherwise
        """
        try:
            self.daytona_client.remove(workspace)
            if workspace in active_workspaces:
                active_workspaces.remove(workspace)
            print(f"✅ Workspace {workspace.id} removed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to remove workspace: {e}")
            return False

def execute_in_workspace(code: str, language: str = "python", cleanup: bool = True) -> Dict[str, Any]:
    """
    High-level function to execute code in a Daytona workspace
    
    Args:
        code: The code to execute
        language: Programming language of the code
        cleanup: Whether to clean up the workspace after execution
        
    Returns:
        Dictionary with execution results
    """
    try:
        manager = WorkspaceManager()
        workspace = manager.create_workspace()
        
        if not workspace:
            return {"success": False, "output": "Failed to create workspace", "exit_code": 1}
        
        result = manager.execute_code(workspace, code, language)
        
        if cleanup:
            manager.cleanup_workspace(workspace)
        else:
            print(f"⚠️ Workspace {workspace.id} is still running")
        
        return result
    except Exception as e:
        return {"success": False, "output": f"Execution failed: {str(e)}", "exit_code": 1}

def main():
    """Command-line entry point for direct execution"""
    try:
        # Determine if we're running as a module or directly
        is_module_call = len(sys.argv) > 1 and sys.argv[0].endswith('__main__.py')
        
        # Check if we're being called by Goose
        is_goose = 'GOOSE_SESSION_ID' in os.environ or any('goose' in arg.lower() for arg in sys.argv)
        
        # Get the code to execute
        code = ""
        if len(sys.argv) > 1:
            # If it's a file path, read the file
            if os.path.exists(sys.argv[1]):
                with open(sys.argv[1], 'r') as f:
                    code = f.read()
            else:
                # Otherwise treat it as code directly
                code = sys.argv[1]
        else:
            # Read from stdin
            code = sys.stdin.read()
        
        if not code:
            print(json.dumps({"error": "No code provided"}))
            return 1
        
        # Set automatic cleanup based on context
        # Always clean up when called by Goose
        cleanup = True if is_goose else os.getenv('DAYTONA_AUTO_CLEANUP', 'true').lower() in ('true', '1', 'yes')
        
        # Only ask for input if not called by Goose and auto cleanup is not set
        if not is_goose and os.getenv('DAYTONA_AUTO_CLEANUP') is None:
            try:
                cleanup = input("\nClean up workspace after execution? (y/n, default: y): ").lower() != 'n'
            except (EOFError, KeyboardInterrupt):
                # Handle the case where input is not available
                cleanup = True
        
        # Execute code
        result = execute_in_workspace(code, cleanup=cleanup)
        
        # Print result
        print(result.get("output", ""))
        return 0 if result.get("success", False) else 1
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())