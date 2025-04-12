# Developer Guide: Government Financial Budget Assistant

This guide provides technical information for developers who will maintain and extend the Government Financial Budget Assistant system.

## System Architecture

The system follows the Model Context Protocol (MCP) architecture with three main components:

1. **MCP Client**: React-based frontend
2. **Gemini API Client**: FastAPI middleware using Google's Gemini LLM
3. **MCP Server**: FastAPI backend for data retrieval and processing

### Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   MCP Client    │────▶│  Gemini API     │────▶│   MCP Server    │
│   (React.js)    │◀────│  Client         │◀────│   (FastAPI)     │
│                 │     │  (FastAPI)      │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        │
                                                        ▼
                                         ┌─────────────────────────────┐
                                         │                             │
                                         │   Government Budget APIs    │
                                         │   (USASpending.gov,         │
                                         │    Treasury.gov)            │
                                         │                             │
                                         └─────────────────────────────┘
```

## Development Environment Setup

### Prerequisites

- Node.js 20.x or higher
- Python 3.10 or higher
- npm
- pip

### Local Development Setup

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

3. Start each component in development mode:

**MCP Client:**
```
cd mcp_client
npm install
npm start
```

**Gemini API Client:**
```
cd gemini_api_client
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```

**MCP Server:**
```
cd mcp_server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --reload --port 5001
```

## Code Structure

### MCP Client

```
mcp_client/
├── public/                # Static assets
├── src/
│   ├── components/        # Reusable UI components
│   ├── pages/             # Page components
│   ├── redux/             # State management
│   │   └── slices/        # Redux slices
│   ├── services/          # API services
│   └── utils/             # Utility functions
├── package.json           # Dependencies and scripts
└── README.md              # Client-specific documentation
```

### Gemini API Client

```
gemini_api_client/
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variables template
```

### MCP Server

```
mcp_server/
├── server.py              # FastAPI application
├── data_integration.py    # Integration with data sources
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variables template
```

### Data Integration

```
data_integration/
├── usaspending_connector.py  # USASpending.gov API connector
├── treasury_connector.py     # Treasury.gov API connector
└── data_manager.py           # Unified data manager
```

## Key Technologies

- **Frontend**: React.js, Redux, Chart.js
- **Backend**: FastAPI, Python
- **AI/ML**: Google Gemini LLM
- **Data Processing**: Pandas, NumPy
- **Testing**: Python unittest, Jest

## Adding New Features

### Adding a New Data Source

1. Create a new connector in the `data_integration` directory
2. Implement the standard connector interface
3. Update the `data_manager.py` to include the new data source
4. Update the MCP Server to use the new data source

Example connector interface:
```python
def get_data(parameters):
    """
    Retrieve data based on parameters.
    
    Args:
        parameters (dict): Query parameters
            
    Returns:
        dict: Formatted data
    """
    pass

def format_data_for_client(data):
    """
    Format data for consumption by the MCP Client.
    
    Args:
        data: Raw data
        
    Returns:
        dict: Formatted data
    """
    pass
```

### Adding a New Visualization Type

1. Update the `VisualizationSelector.js` component to include the new chart type
2. Implement the rendering logic in `ResultsDisplay.js`
3. Update the Gemini API Client to recognize the new visualization type in queries

## Testing

### Running Tests

To run all tests:
```
./run_tests.sh
```

To run specific tests:
```
cd tests
python -m unittest test_components.py
python -m unittest test_integration.py
```

### Writing New Tests

1. Add unit tests to `tests/test_components.py`
2. Add integration tests to `tests/test_integration.py`
3. Follow the existing test patterns

## Deployment

### Production Deployment

For production deployment:

1. Build the React client:
```
cd mcp_client
npm run build
```

2. Set up a production server (e.g., Nginx) to serve the static files

3. Deploy the FastAPI applications using Gunicorn:
```
# Gemini API Client
gunicorn -w 4 -k uvicorn.workers.UvicornWorker gemini_api_client.main:app

# MCP Server
gunicorn -w 4 -k uvicorn.workers.UvicornWorker mcp_server.server:app
```

### Environment Variables

**Gemini API Client:**
- `GEMINI_API_KEY`: Your Google Gemini API key
- `MCP_SERVER_URL`: URL of the MCP Server

**MCP Server:**
- `USASPENDING_API_KEY`: API key for USASpending.gov (optional)
- `TREASURY_API_KEY`: API key for Treasury.gov (optional)
- `ENABLE_MOCK_DATA`: Set to "true" to use mock data instead of real APIs

## Troubleshooting

### Common Issues

1. **API Rate Limiting**: Government APIs may have rate limits. Implement caching to reduce API calls.

2. **Gemini API Errors**: Check your API key and ensure you're using the correct model version.

3. **Data Format Changes**: Government APIs may change their data formats. Monitor for changes and update connectors accordingly.

### Logging

Logs are stored in the `logs` directory:
- `mcp_client.log`: Frontend logs
- `gemini_api.log`: Gemini API Client logs
- `mcp_server.log`: MCP Server logs
- `unit_tests.log`: Unit test logs
- `integration_tests.log`: Integration test logs

## Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Run tests to ensure everything works
4. Submit a pull request

## License

[MIT License](LICENSE)
