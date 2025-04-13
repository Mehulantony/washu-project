from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import logging
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API endpoints
USASPENDING_API_URL = "https://api.usaspending.gov"
TREASURY_API_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"

# Initialize FastAPI app
app = FastAPI(
    title="Government Financial Budget Assistant - MCP Server",
    description="Backend server for retrieving and processing U.S. government budget data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request and response models
class DataRequest(BaseModel):
    entity: Optional[str] = None
    metric: Optional[str] = None
    time_period: Optional[str] = None
    comparison: Optional[bool] = None
    aggregation: Optional[str] = None
    limit: Optional[int] = None
    visualization: Optional[str] = None

class DataResponse(BaseModel):
    data: List[Dict[str, Any]]
    metadata: Dict[str, Any]

# Mock data for development/testing
MOCK_BUDGET_DATA = {
    "departments": {
        "Department of Defense": {
            "2023": 816700000000,
            "2022": 782000000000,
            "2021": 740500000000,
            "2020": 721500000000,
            "2019": 686000000000
        },
        "Department of Health and Human Services": {
            "2023": 1718000000000,
            "2022": 1626000000000,
            "2021": 1504000000000,
            "2020": 1399000000000,
            "2019": 1285000000000
        },
        "Department of Education": {
            "2023": 79800000000,
            "2022": 76400000000,
            "2021": 73000000000,
            "2020": 72300000000,
            "2019": 71000000000
        },
        "Department of Transportation": {
            "2023": 105000000000,
            "2022": 90000000000,
            "2021": 87000000000,
            "2020": 86000000000,
            "2019": 84000000000
        },
        "Department of Veterans Affairs": {
            "2023": 301000000000,
            "2022": 284000000000,
            "2021": 243000000000,
            "2020": 218000000000,
            "2019": 201000000000
        },
        "Department of Homeland Security": {
            "2023": 56700000000,
            "2022": 52000000000,
            "2021": 49800000000,
            "2020": 51700000000,
            "2019": 47500000000
        },
        "Department of Housing and Urban Development": {
            "2023": 71900000000,
            "2022": 65300000000,
            "2021": 60300000000,
            "2020": 56500000000,
            "2019": 53800000000
        },
        "Department of Energy": {
            "2023": 45300000000,
            "2022": 41900000000,
            "2021": 39600000000,
            "2020": 38500000000,
            "2019": 35500000000
        },
        "Department of Justice": {
            "2023": 38700000000,
            "2022": 35200000000,
            "2021": 33400000000,
            "2020": 32400000000,
            "2019": 30900000000
        },
        "Department of Agriculture": {
            "2023": 228000000000,
            "2022": 199000000000,
            "2021": 184000000000,
            "2020": 154000000000,
            "2019": 150000000000
        }
    }
}

# Data source connectors
async def fetch_usaspending_data(entity=None, fiscal_year=None, limit=10):
    """
    Fetch budget data from USASpending.gov API
    """
    try:
        # In a real implementation, this would make actual API calls
        # For now, we'll simulate the API response
        
        logger.info(f"Fetching USASpending data for entity={entity}, fiscal_year={fiscal_year}")
        
        # Simulate API call delay
        import asyncio
        await asyncio.sleep(0.5)
        
        # Return mock data based on parameters
        if entity and entity in MOCK_BUDGET_DATA["departments"]:
            dept_data = MOCK_BUDGET_DATA["departments"][entity]
            if fiscal_year and fiscal_year in dept_data:
                return [{
                    "department": entity,
                    "year": fiscal_year,
                    "amount": dept_data[fiscal_year],
                    "source": "USASpending.gov"
                }]
            else:
                return [
                    {"department": entity, "year": year, "amount": amount, "source": "USASpending.gov"}
                    for year, amount in dept_data.items()
                ]
        else:
            # Return data for all departments
            result = []
            for dept, years in MOCK_BUDGET_DATA["departments"].items():
                if fiscal_year and fiscal_year in years:
                    result.append({
                        "department": dept,
                        "year": fiscal_year,
                        "amount": years[fiscal_year],
                        "source": "USASpending.gov"
                    })
                elif not fiscal_year:
                    for year, amount in years.items():
                        result.append({
                            "department": dept,
                            "year": year,
                            "amount": amount,
                            "source": "USASpending.gov"
                        })
            
            # Apply limit
            if limit and len(result) > limit:
                result = sorted(result, key=lambda x: x["amount"], reverse=True)[:limit]
                
            return result
    
    except Exception as e:
        logger.error(f"Error fetching USASpending data: {str(e)}")
        return []

async def fetch_treasury_data(entity=None, fiscal_year=None, limit=10):
    """
    Fetch budget data from Treasury.gov API
    """
    try:
        # In a real implementation, this would make actual API calls
        # For now, we'll simulate the API response
        
        logger.info(f"Fetching Treasury data for entity={entity}, fiscal_year={fiscal_year}")
        
        # Simulate API call delay
        import asyncio
        await asyncio.sleep(0.5)
        
        # Return mock data with slight variations from USASpending
        if entity and entity in MOCK_BUDGET_DATA["departments"]:
            dept_data = MOCK_BUDGET_DATA["departments"][entity]
            if fiscal_year and fiscal_year in dept_data:
                # Add slight variation to amount
                amount = dept_data[fiscal_year]
                amount_with_variation = amount * (1 + (hash(entity) % 5) / 100)  # +/- 5% variation
                
                return [{
                    "department": entity,
                    "year": fiscal_year,
                    "amount": amount_with_variation,
                    "source": "Treasury.gov"
                }]
            else:
                return [
                    {
                        "department": entity, 
                        "year": year, 
                        "amount": amount * (1 + (hash(entity + year) % 5) / 100),
                        "source": "Treasury.gov"
                    }
                    for year, amount in dept_data.items()
                ]
        else:
            # Return data for all departments
            result = []
            for dept, years in MOCK_BUDGET_DATA["departments"].items():
                if fiscal_year and fiscal_year in years:
                    amount = years[fiscal_year]
                    amount_with_variation = amount * (1 + (hash(dept) % 5) / 100)
                    result.append({
                        "department": dept,
                        "year": fiscal_year,
                        "amount": amount_with_variation,
                        "source": "Treasury.gov"
                    })
                elif not fiscal_year:
                    for year, amount in years.items():
                        amount_with_variation = amount * (1 + (hash(dept + year) % 5) / 100)
                        result.append({
                            "department": dept,
                            "year": year,
                            "amount": amount_with_variation,
                            "source": "Treasury.gov"
                        })
            
            # Apply limit
            if limit and len(result) > limit:
                result = sorted(result, key=lambda x: x["amount"], reverse=True)[:limit]
                
            return result
    
    except Exception as e:
        logger.error(f"Error fetching Treasury data: {str(e)}")
        return []

# Data processing functions
def process_time_period(time_period):
    """
    Process time period parameter to extract fiscal years
    """
    years = []
    
    if not time_period:
        return ["2023"]  # Default to most recent year
    
    if "-" in time_period:
        # Handle range like "2020-2022"
        start_year, end_year = time_period.split("-")
        years = [str(year) for year in range(int(start_year), int(end_year) + 1)]
    elif "last" in time_period.lower() and "years" in time_period.lower():
        # Handle "last X years"
        import re
        match = re.search(r'last (\d+)', time_period.lower())
        if match:
            num_years = int(match.group(1))
            current_year = 2023  # In a real implementation, this would be dynamic
            years = [str(year) for year in range(current_year - num_years + 1, current_year + 1)]
    else:
        # Single year
        years = [time_period]
    
    return years

def apply_aggregation(data, aggregation_type):
    """
    Apply aggregation to the data based on the specified type
    """
    if not aggregation_type or not data:
        return data
    
    result = []
    
    if aggregation_type.lower() == "total":
        # Group by department and sum amounts
        dept_totals = {}
        for item in data:
            dept = item["department"]
            if dept not in dept_totals:
                dept_totals[dept] = 0
            dept_totals[dept] += item["amount"]
        
        # Convert to list format
        for dept, total in dept_totals.items():
            result.append({
                "department": dept,
                "amount": total,
                "aggregation": "total"
            })
    
    elif aggregation_type.lower() == "average":
        # Group by department and calculate average
        dept_amounts = {}
        for item in data:
            dept = item["department"]
            if dept not in dept_amounts:
                dept_amounts[dept] = []
            dept_amounts[dept].append(item["amount"])
        
        # Calculate averages
        for dept, amounts in dept_amounts.items():
            avg = sum(amounts) / len(amounts)
            result.append({
                "department": dept,
                "amount": avg,
                "aggregation": "average"
            })
    
    elif aggregation_type.lower() == "percentage":
        # Calculate total budget
        total_budget = sum(item["amount"] for item in data)
        
        # Group by department
        dept_amounts = {}
        for item in data:
            dept = item["department"]
            if dept not in dept_amounts:
                dept_amounts[dept] = 0
            dept_amounts[dept] += item["amount"]
        
        # Calculate percentages
        for dept, amount in dept_amounts.items():
            percentage = (amount / total_budget) * 100
            result.append({
                "department": dept,
                "amount": amount,
                "percentage": percentage,
                "aggregation": "percentage"
            })
    
    return result or data

@app.post("/api/data", response_model=DataResponse)
async def get_budget_data(request: DataRequest):
    """
    Retrieve budget data based on the parameters extracted from the natural language query.
    """
    try:
        logger.info(f"Received data request: {request}")
        
        # Process the request parameters
        entity = request.entity
        years = process_time_period(request.time_period)
        limit = request.limit or 10
        
        # Fetch data from multiple sources
        data = []
        
        # In a real implementation, we would fetch from actual APIs
        # For now, we'll use our mock data connectors
        for year in years:
            # Fetch from USASpending
            usaspending_data = await fetch_usaspending_data(entity, year, limit)
            data.extend(usaspending_data)
            
            # Fetch from Treasury
            # Uncomment to include Treasury data
            # treasury_data = await fetch_treasury_data(entity, year, limit)
            # data.extend(treasury_data)
        
        # Apply aggregation if specified
        if request.aggregation:
            data = apply_aggregation(data, request.aggregation)
        
        # Apply limit if specified and not already applied in data source connectors
        if request.limit and len(data) > request.limit:
            # Sort by amount (descending) before applying limit
            data.sort(key=lambda x: x["amount"], reverse=True)
            data = data[:request.limit]
        
        # Add metadata
        metadata = {
            "query_parameters": request.dict(),
            "result_count": len(data),
            "sources": ["USASpending.gov"],  # Add Treasury.gov if used
            "years": years
        }
        
        return {
            "data": data,
            "metadata": metadata
        }
    
    except Exception as e:
        logger.error(f"Error retrieving budget data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data retrieval failed: {str(e)}")

@app.get("/api/departments")
async def get_departments():
    """
    Get list of available government departments
    """
    departments = list(MOCK_BUDGET_DATA["departments"].keys())
    return {"departments": departments}

@app.get("/api/years")
async def get_fiscal_years():
    """
    Get list of available fiscal years
    """
    # Extract unique years from the mock data
    years = set()
    for dept_data in MOCK_BUDGET_DATA["departments"].values():
        years.update(dept_data.keys())
    
    return {"fiscal_years": sorted(list(years), reverse=True)}

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for the MCP Server.
    """
    return {"status": "healthy", "service": "mcp-server"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=5001, reload=True)
