#!/bin/bash

# Stop script for the Government Financial Budget Assistant
# This script stops all three components of the system:
# 1. MCP Client (React frontend)
# 2. Gemini API Client (FastAPI middleware)
# 3. MCP Server (FastAPI backend)

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Stopping Government Financial Budget Assistant...${NC}"

# Check if PID files exist
mkdir -p .pids

# Stop MCP Client
if [ -f .pids/mcp_client.pid ]; then
    MCP_CLIENT_PID=$(cat .pids/mcp_client.pid)
    if ps -p $MCP_CLIENT_PID > /dev/null; then
        echo -e "${GREEN}Stopping MCP Client (PID: $MCP_CLIENT_PID)...${NC}"
        kill -15 $MCP_CLIENT_PID 2>/dev/null || kill -9 $MCP_CLIENT_PID 2>/dev/null
        echo "MCP Client stopped."
    else
        echo -e "${YELLOW}MCP Client (PID: $MCP_CLIENT_PID) is not running.${NC}"
    fi
    rm .pids/mcp_client.pid
else
    echo -e "${YELLOW}MCP Client PID file not found. Process may not be running.${NC}"
fi

# Stop Gemini API Client
if [ -f .pids/gemini_api.pid ]; then
    GEMINI_API_PID=$(cat .pids/gemini_api.pid)
    if ps -p $GEMINI_API_PID > /dev/null; then
        echo -e "${GREEN}Stopping Gemini API Client (PID: $GEMINI_API_PID)...${NC}"
        kill -15 $GEMINI_API_PID 2>/dev/null || kill -9 $GEMINI_API_PID 2>/dev/null
        echo "Gemini API Client stopped."
    else
        echo -e "${YELLOW}Gemini API Client (PID: $GEMINI_API_PID) is not running.${NC}"
    fi
    rm .pids/gemini_api.pid
else
    echo -e "${YELLOW}Gemini API Client PID file not found. Process may not be running.${NC}"
fi

# Stop MCP Server
if [ -f .pids/mcp_server.pid ]; then
    MCP_SERVER_PID=$(cat .pids/mcp_server.pid)
    if ps -p $MCP_SERVER_PID > /dev/null; then
        echo -e "${GREEN}Stopping MCP Server (PID: $MCP_SERVER_PID)...${NC}"
        kill -15 $MCP_SERVER_PID 2>/dev/null || kill -9 $MCP_SERVER_PID 2>/dev/null
        echo "MCP Server stopped."
    else
        echo -e "${YELLOW}MCP Server (PID: $MCP_SERVER_PID) is not running.${NC}"
    fi
    rm .pids/mcp_server.pid
else
    echo -e "${YELLOW}MCP Server PID file not found. Process may not be running.${NC}"
fi

# Kill any remaining uvicorn processes
UVICORN_PIDS=$(pgrep -f "uvicorn")
if [ ! -z "$UVICORN_PIDS" ]; then
    echo -e "${GREEN}Stopping remaining uvicorn processes...${NC}"
    kill -15 $UVICORN_PIDS 2>/dev/null || kill -9 $UVICORN_PIDS 2>/dev/null
fi

# Kill any remaining npm processes
NPM_PIDS=$(pgrep -f "npm start")
if [ ! -z "$NPM_PIDS" ]; then
    echo -e "${GREEN}Stopping remaining npm processes...${NC}"
    kill -15 $NPM_PIDS 2>/dev/null || kill -9 $NPM_PIDS 2>/dev/null
fi

echo -e "${GREEN}All components stopped successfully!${NC}"
