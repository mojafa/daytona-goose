#!/bin/bash
# Simple wrapper script for running code in Daytona

# Set environment variable to auto-cleanup
export DAYTONA_AUTO_CLEANUP=true

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if code is provided as an argument
if [ "$1" == "-f" ] && [ -n "$2" ]; then
    # Run code from a file
    python -m daytona_goose.daytona_executor "$2"
elif [ -n "$1" ]; then
    # Run code directly
    echo "$1" | python -m daytona_goose.daytona_executor
else
    # Read from stdin
    python -m daytona_goose.daytona_executor
fi