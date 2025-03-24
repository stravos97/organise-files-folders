#!/bin/bash

# organize-files.sh - Script to run organize-tool with the provided configuration

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if organize-tool is installed
if ! command -v organize &> /dev/null; then
    echo "organize-tool is not installed. Installing now..."
    pip install -U organize-tool
fi

# Function to display usage information
show_usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -s, --simulate    Run in simulation mode (no actual changes)"
    echo "  -r, --run         Run the organization (default)"
    echo "  -c, --config      Specify a custom config file"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --simulate     # Test what would happen without making changes"
    echo "  $0 --run          # Actually organize the files"
    echo "  $0 --config /path/to/custom-config.yaml  # Use a custom config file"
}

# Default values
MODE="run"
CONFIG_FILE="$SCRIPT_DIR/organize.yaml"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--simulate)
            MODE="sim"
            shift
            ;;
        -r|--run)
            MODE="run"
            shift
            ;;
        -c|--config)
            CONFIG_FILE="$2"
            shift
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if the config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Config file not found: $CONFIG_FILE"
    exit 1
fi

# Run organize-tool with the specified mode and config file
echo "Running organize-tool in $MODE mode with config: $CONFIG_FILE"
organize $MODE "$CONFIG_FILE"

# Display completion message
if [ "$MODE" == "sim" ]; then
    echo ""
    echo "Simulation completed. No files were actually moved."
    echo "To actually organize files, run: $0 --run"
else
    echo ""
    echo "Organization completed successfully!"
fi
