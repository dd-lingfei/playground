#!/bin/bash

# Item Catalog MCP Server Startup Script
# =====================================

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Get the project root directory (parent of mcp directory)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Starting Item Catalog MCP Server..."
echo "==================================="
echo "Script directory: $SCRIPT_DIR"
echo "Project root: $PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "❌ Virtual environment not found at $PROJECT_ROOT/venv"
    echo "   Please run from the project root:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   python3 -m pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source "$PROJECT_ROOT/venv/bin/activate"

# Check if MCP dependencies are installed
if ! python -c "import mcp.server" 2>/dev/null; then
    echo "📦 Installing MCP dependencies..."
    pip install -r "$PROJECT_ROOT/requirements.txt"
fi

# Check if SnowflakeClient can be imported from clients package
if ! python -c "import sys; sys.path.insert(0, '$PROJECT_ROOT'); from clients import SnowflakeClient" 2>/dev/null; then
    echo "❌ Cannot import SnowflakeClient from clients package. Please check your setup."
    exit 1
fi

echo "🚀 Starting Item Catalog MCP Server..."
echo "   The server will communicate via stdio with AI assistants"
echo "   Available tools: check_item_menu_history, check_item_level_details"
echo "   Press Ctrl+C to stop"
echo ""

# Run the MCP server with proper Python path
cd "$PROJECT_ROOT"
PYTHONPATH="$PROJECT_ROOT" python "$SCRIPT_DIR/mcp_server.py" 