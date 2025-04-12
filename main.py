from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
import json
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:5001/api")

if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables. Using placeholder.")
    GEMINI_API_KEY = "placeholder_api_key"

genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI(
    title="Government Financial Budget Assistant - Gemini API Client",
    description="Middleware for processing natural language queries about U.S. government budget data using Gemini LLM",
    version="1.0.0"
)

# Define request and response models
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

class QueryResponse(BaseModel):
    query: str
    query_parameters: Dict[str, Any]
    data: List[Dict[str, Any]]
    insights: str

# Gemini model configuration
MODEL_NAME = "gemini-1.5-pro"

# Define parameter extraction prompt template
PARAMETER_EXTRACTION_PROMPT = """
You are a specialized parameter extraction system for a Government Financial Budget Assistant.
Your task is to analyze a natural language query about U.S. government budget data and extract structured parameters.

Extract the following parameters from the query:
1. entity: The government department, agency, or program being queried (e.g., "Department of Defense", "Medicare")
2. metric: The financial metric being requested (e.g., "spending", "budget", "allocation", "funding")
3. time_period: The fiscal year or time range (e.g., "2023", "2020-2022", "last 5 years")
4. comparison: Whether a comparison is requested and between what entities or time periods
5. aggregation: The type of aggregation requested (e.g., "total", "average", "percentage")
6. limit: Number of results requested (e.g., "top 5", "bottom 10")
7. visualization: Suggested visualization type (e.g., "bar chart", "line chart", "pie chart")

For the query: "{query}"

Return ONLY a JSON object with these parameters. If a parameter is not present in the query, set its value to null.
"""

async def extract_parameters(query: str) -> Dict[str, Any]:
    """
    Use Gemini LLM to extract structured parameters from a natural language query.
    """
    try:
        # Create the prompt with the user's query
        prompt = PARAMETER_EXTRACTION_PROMPT.format(query=query)
        
        # Generate response from Gemini
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        
        # Extract and parse the JSON response
        response_text = response.text
        
        # Handle potential formatting issues in the response
        try:
            # Try to parse the response as JSON
            parameters = json.loads(response_text)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from the text
            import re
            json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                parameters = json.loads(json_match.group(1))
            else:
                # Fallback to a simple extraction approach
                parameters = {
                    "entity": None,
                    "metric": None,
                    "time_period": None,
                    "comparison": None,
                    "aggregation": None,
                    "limit": None,
                    "visualization": None
                }
                
                # Try to extract parameters from the text
                if "Department of Defense" in query or "DoD" in query:
                    parameters["entity"] = "Department of Defense"
                if "spending" in query.lower():
                    parameters["metric"] = "spending"
                if "2023" in query:
                    parameters["time_period"] = "2023"
                if "compare" in query.lower() or "comparison" in query.lower():
                    parameters["comparison"] = True
                
        logger.info(f"Extracted parameters: {parameters}")
        return parameters
    
    except Exception as e:
        logger.error(f"Error extracting parameters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Parameter extraction failed: {str(e)}")

async def fetch_budget_data(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Forward the structured parameters to the MCP Server to fetch budget data.
    """
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/data",
            json=parameters,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching budget data: {str(e)}")
        # Return mock data for development/testing
        return {
            "data": [
                {"department": "Department of Defense", "year": "2023", "amount": 816700000000},
                {"department": "Department of Defense", "year": "2022", "amount": 782000000000}
            ],
            "insights": "The Department of Defense budget increased by approximately 4.4% from 2022 to 2023."
        }

async def generate_insights(query: str, parameters: Dict[str, Any], data: List[Dict[str, Any]]) -> str:
    """
    Use Gemini LLM to generate natural language insights about the budget data.
    """
    try:
        # Create a prompt for generating insights
        data_str = json.dumps(data, indent=2)
        prompt = f"""
        You are a Government Financial Budget Assistant providing insights on U.S. government budget data.
        
        Original query: "{query}"
        
        Extracted parameters: {json.dumps(parameters, indent=2)}
        
        Budget data: {data_str}
        
        Provide 3-5 concise, informative insights about this budget data. Focus on key trends, comparisons, 
        and notable findings. Format your response as HTML paragraphs (<p> tags) for easy display.
        """
        
        # Generate response from Gemini
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        
        insights = response.text
        
        # Ensure insights are formatted as HTML
        if not insights.strip().startswith("<p>"):
            insights = "<p>" + insights.replace("\n\n", "</p><p>") + "</p>"
            
        return insights
    
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        return "<p>Unable to generate insights for this query. Please try a different query.</p>"

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a natural language query about U.S. government budget data.
    """
    try:
        # Extract structured parameters from the query using Gemini
        parameters = await extract_parameters(request.query)
        
        # Fetch budget data from MCP Server using the extracted parameters
        budget_data = await fetch_budget_data(parameters)
        
        # Generate insights about the budget data using Gemini
        insights = await generate_insights(request.query, parameters, budget_data["data"])
        
        # Construct the response
        response = {
            "query": request.query,
            "query_parameters": parameters,
            "data": budget_data["data"],
            "insights": insights
        }
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for the Gemini API Client.
    """
    return {"status": "healthy", "service": "gemini-api-client"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
