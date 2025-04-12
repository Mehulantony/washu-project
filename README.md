# Government Financial Budget Assistant

A comprehensive system that allows government finance officers and analysts to submit natural language queries and receive detailed budget insights using structured U.S. government budget data.

## Architecture Overview

The Government Financial Budget Assistant follows the Model Context Protocol (MCP) architecture and consists of three main components:

1. **MCP Client**: React-based frontend interface for submitting queries and visualizing results
2. **Gemini API Client**: FastAPI middleware that processes natural language queries using Google's Gemini LLM
3. **MCP Server**: FastAPI backend that retrieves and processes budget data from various government sources

## Features

- Natural language query processing for government budget data
- Integration with USASpending.gov and Treasury.gov APIs
- Detailed data visualization with multiple chart types
- Historical budget data comparison
- Agency and department-specific budget analysis
- Query history tracking

## Installation

### Prerequisites

- Node.js 20.x or higher
- Python 3.10 or higher
- npm
- pip

### Setup

1. Clone the repository:
```
git clone https://github.com/your-organization/government-budget-assistant.git
cd government-budget-assistant
```

2. Set up environment variables:
```
# For Gemini API Client
cp gemini_api_client/.env.example gemini_api_client/.env
# Edit the .env file to add your Gemini API key

# For MCP Server
cp mcp_server/.env.example mcp_server/.env
# Edit the .env file to configure data sources
```

3. Create necessary directories:
```
mkdir -p logs .pids
```

4. Make scripts executable:
```
chmod +x run.sh stop.sh run_tests.sh
```

## Usage

### Starting the Application

To start all components of the Government Financial Budget Assistant:

```
./run.sh
```

This will start:
- MCP Client on port 3000
- Gemini API Client on port 5000
- MCP Server on port 5001

Access the application at: http://localhost:3000

### Stopping the Application

To stop all components:

```
./stop.sh
```

### Running Tests

To run all unit and integration tests:

```
./run_tests.sh
```

## Example Queries

The Government Financial Budget Assistant can answer questions like:

- "What was the Department of Defense budget for fiscal year 2023?"
- "Compare education spending between 2020 and 2022"
- "Show me the top 5 departments by budget allocation in 2023"
- "What percentage of the federal budget went to healthcare in 2022?"
- "How has infrastructure spending changed over the last 5 years?"

## Data Sources

The system integrates with the following U.S. government budget data sources:

1. **USASpending.gov API**:
   - Provides detailed federal spending data
   - Offers information on contracts, grants, loans, and other financial assistance

2. **Treasury.gov APIs**:
   - Provides data on federal debt, revenue, and spending
   - Includes fiscal service data APIs

## Component Details

### MCP Client

The frontend interface built with React, Redux, and Chart.js for data visualization.

Key files:
- `mcp_client/src/App.js`: Main application component
- `mcp_client/src/pages/Dashboard.js`: Main query interface
- `mcp_client/src/components/ResultsDisplay.js`: Data visualization component

### Gemini API Client

The middleware that processes natural language queries using Google's Gemini LLM.

Key files:
- `gemini_api_client/main.py`: FastAPI application
- `gemini_api_client/.env.example`: Configuration template

### MCP Server

The backend that retrieves and processes budget data from various government sources.

Key files:
- `mcp_server/server.py`: FastAPI application
- `mcp_server/data_integration.py`: Integration with data sources
- `mcp_server/.env.example`: Configuration template

### Data Integration

Connectors for government budget data sources.

Key files:
- `data_integration/usaspending_connector.py`: USASpending.gov API connector
- `data_integration/treasury_connector.py`: Treasury.gov API connector
- `data_integration/data_manager.py`: Unified data manager

## Testing

The system includes comprehensive unit and integration tests:

- `tests/test_components.py`: Unit tests for individual components
- `tests/test_integration.py`: Integration tests for component interactions

## License

[MIT License](LICENSE)

## Acknowledgements

- Google Gemini LLM for natural language processing
- USASpending.gov for federal spending data
- Treasury.gov for fiscal data
