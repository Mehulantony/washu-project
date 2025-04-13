#!/bin/bash

# Run script for the Government Financial Budget Assistant
# This script starts all three components of the system:
# 1. MCP Client (React frontend)
# 2. Gemini API Client (FastAPI middleware)
# 3. MCP Server (FastAPI backend)

# Configuration
MCP_CLIENT_PORT=3000
GEMINI_API_PORT=5000
MCP_SERVER_PORT=5001

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Government Financial Budget Assistant...${NC}"

# Function to check if a port is in use
is_port_in_use() {
  if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
    return 0
  else
    return 1
  fi
}

# Check if ports are available
for port in $MCP_CLIENT_PORT $GEMINI_API_PORT $MCP_SERVER_PORT; do
  if is_port_in_use $port; then
    echo -e "${YELLOW}Warning: Port $port is already in use. Component on this port may not start correctly.${NC}"
  fi
done

# Start MCP Server
echo -e "${GREEN}Starting MCP Server on port $MCP_SERVER_PORT...${NC}"
cd mcp_server
python3 -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -r requirements.txt 2>/dev/null || pip install fastapi uvicorn python-dotenv requests pandas
nohup uvicorn server:app --host 0.0.0.0 --port $MCP_SERVER_PORT --reload > ../logs/mcp_server.log 2>&1 &
MCP_SERVER_PID=$!
deactivate
cd ..
echo "MCP Server started with PID: $MCP_SERVER_PID"

# Start Gemini API Client
echo -e "${GREEN}Starting Gemini API Client on port $GEMINI_API_PORT...${NC}"
cd gemini_api_client
python3 -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -r requirements.txt 2>/dev/null || pip install fastapi uvicorn google-generativeai python-dotenv pydantic requests
nohup uvicorn main:app --host 0.0.0.0 --port $GEMINI_API_PORT --reload > ../logs/gemini_api.log 2>&1 &
GEMINI_API_PID=$!
deactivate
cd ..
echo "Gemini API Client started with PID: $GEMINI_API_PID"

# Start MCP Client
echo -e "${GREEN}Starting MCP Client on port $MCP_CLIENT_PORT...${NC}"
cd mcp_client
npm install 2>/dev/null || true
nohup npm start > ../logs/mcp_client.log 2>&1 &
MCP_CLIENT_PID=$!
cd ..
echo "MCP Client started with PID: $MCP_CLIENT_PID"

echo -e "${GREEN}All components started successfully!${NC}"
echo -e "${GREEN}Access the application at: http://localhost:$MCP_CLIENT_PORT${NC}"
echo ""
echo "To stop all components, run: ./stop.sh"

# Save PIDs to file for stop script
mkdir -p .pids
echo "$MCP_SERVER_PID" > .pids/mcp_server.pid
echo "$GEMINI_API_PID" > .pids/gemini_api.pid
echo "$MCP_CLIENT_PID" > .pids/mcp_client.pid
