"""
USASpending.gov API Connector for Government Financial Budget Assistant

This module provides functions to retrieve budget data from the USASpending.gov API.
"""

import os
import requests
import json
import logging
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# API configuration
BASE_URL = "https://api.usaspending.gov/api/v2"
API_KEY = os.getenv("USASPENDING_API_KEY", "")

# Headers for API requests
HEADERS = {
    "Content-Type": "application/json"
}
if API_KEY:
    HEADERS["X-API-Key"] = API_KEY

def get_agency_budgetary_resources(agency_code, fiscal_year):
    """
    Retrieve budgetary resources and obligations for a specific agency and fiscal year.
    
    Args:
        agency_code (str): The agency code (e.g., "012" for Department of Agriculture)
        fiscal_year (str): The fiscal year (e.g., "2023")
        
    Returns:
        dict: JSON response containing budgetary resources data
    """
    endpoint = f"{BASE_URL}/agency/{agency_code}/budgetary_resources/"
    params = {"fiscal_year": fiscal_year}
    
    try:
        logger.info(f"Fetching budgetary resources for agency {agency_code} in FY {fiscal_year}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching budgetary resources: {str(e)}")
        return {"error": str(e)}

def get_agency_obligations_by_award_category(agency_code, fiscal_year):
    """
    Retrieve a breakdown of obligations by award category for a specific agency and fiscal year.
    
    Args:
        agency_code (str): The agency code (e.g., "012" for Department of Agriculture)
        fiscal_year (str): The fiscal year (e.g., "2023")
        
    Returns:
        dict: JSON response containing obligations by award category
    """
    endpoint = f"{BASE_URL}/agency/{agency_code}/obligations_by_award_category/"
    params = {"fiscal_year": fiscal_year}
    
    try:
        logger.info(f"Fetching obligations by award category for agency {agency_code} in FY {fiscal_year}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching obligations by award category: {str(e)}")
        return {"error": str(e)}

def get_agency_list():
    """
    Retrieve a list of all agencies available in USASpending.gov.
    
    Returns:
        list: List of agencies with their codes and names
    """
    # USASpending doesn't have a direct endpoint for agency list, so we use a workaround
    # by fetching the first page of agencies from the autocomplete endpoint
    endpoint = f"{BASE_URL}/autocomplete/awarding_agency/"
    data = {"search_text": ""}
    
    try:
        logger.info("Fetching agency list")
        response = requests.post(endpoint, json=data, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching agency list: {str(e)}")
        return {"error": str(e)}

def get_federal_accounts_by_agency(agency_code, fiscal_year):
    """
    Retrieve a list of federal accounts for a specific agency and fiscal year.
    
    Args:
        agency_code (str): The agency code (e.g., "012" for Department of Agriculture)
        fiscal_year (str): The fiscal year (e.g., "2023")
        
    Returns:
        dict: JSON response containing federal accounts data
    """
    endpoint = f"{BASE_URL}/agency/{agency_code}/federal_account/"
    params = {"fiscal_year": fiscal_year}
    
    try:
        logger.info(f"Fetching federal accounts for agency {agency_code} in FY {fiscal_year}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching federal accounts: {str(e)}")
        return {"error": str(e)}

def get_agency_overview(agency_code, fiscal_year=None):
    """
    Retrieve overview information for a specific agency.
    
    Args:
        agency_code (str): The agency code (e.g., "012" for Department of Agriculture)
        fiscal_year (str, optional): The fiscal year (e.g., "2023")
        
    Returns:
        dict: JSON response containing agency overview data
    """
    endpoint = f"{BASE_URL}/agency/{agency_code}/"
    params = {}
    if fiscal_year:
        params["fiscal_year"] = fiscal_year
    
    try:
        logger.info(f"Fetching overview for agency {agency_code}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching agency overview: {str(e)}")
        return {"error": str(e)}

def get_budget_data_by_time_period(agency_code=None, start_year=None, end_year=None):
    """
    Retrieve budget data for a specific time period, optionally filtered by agency.
    
    Args:
        agency_code (str, optional): The agency code to filter by
        start_year (str): The starting fiscal year (e.g., "2020")
        end_year (str): The ending fiscal year (e.g., "2023")
        
    Returns:
        pd.DataFrame: DataFrame containing budget data across the specified time period
    """
    # Initialize empty DataFrame to store results
    all_data = pd.DataFrame()
    
    # If no years specified, use current year
    if not start_year and not end_year:
        current_year = datetime.now().year
        fiscal_years = [str(current_year)]
    elif start_year and end_year:
        fiscal_years = [str(year) for year in range(int(start_year), int(end_year) + 1)]
    elif start_year:
        fiscal_years = [start_year]
    else:
        fiscal_years = [end_year]
    
    # If agency code is provided, get data for that agency
    if agency_code:
        for year in fiscal_years:
            try:
                # Get budgetary resources
                budget_data = get_agency_budgetary_resources(agency_code, year)
                
                # Convert to DataFrame
                if "error" not in budget_data:
                    df = pd.json_normalize(budget_data)
                    df["fiscal_year"] = year
                    df["agency_code"] = agency_code
                    
                    # Append to main DataFrame
                    all_data = pd.concat([all_data, df], ignore_index=True)
            except Exception as e:
                logger.error(f"Error processing data for agency {agency_code}, year {year}: {str(e)}")
    else:
        # If no agency code provided, get data for all major agencies
        agencies = get_agency_list()
        if "error" not in agencies and "results" in agencies:
            for agency in agencies["results"]:
                agency_code = agency.get("toptier_agency", {}).get("toptier_code")
                if agency_code:
                    for year in fiscal_years:
                        try:
                            # Get budgetary resources
                            budget_data = get_agency_budgetary_resources(agency_code, year)
                            
                            # Convert to DataFrame
                            if "error" not in budget_data:
                                df = pd.json_normalize(budget_data)
                                df["fiscal_year"] = year
                                df["agency_code"] = agency_code
                                df["agency_name"] = agency.get("toptier_agency", {}).get("name", "")
                                
                                # Append to main DataFrame
                                all_data = pd.concat([all_data, df], ignore_index=True)
                        except Exception as e:
                            logger.error(f"Error processing data for agency {agency_code}, year {year}: {str(e)}")
    
    return all_data

def get_top_agencies_by_budget(fiscal_year, limit=10):
    """
    Retrieve the top agencies by budget allocation for a specific fiscal year.
    
    Args:
        fiscal_year (str): The fiscal year (e.g., "2023")
        limit (int): Number of top agencies to return
        
    Returns:
        list: List of dictionaries containing agency data sorted by budget
    """
    # Get all agencies
    agencies = get_agency_list()
    
    if "error" in agencies or "results" not in agencies:
        return {"error": "Failed to retrieve agency list"}
    
    # Initialize list to store agency budget data
    agency_budgets = []
    
    # Fetch budget data for each agency
    for agency in agencies["results"]:
        agency_code = agency.get("toptier_agency", {}).get("toptier_code")
        agency_name = agency.get("toptier_agency", {}).get("name", "")
        
        if agency_code:
            try:
                # Get budgetary resources
                budget_data = get_agency_budgetary_resources(agency_code, fiscal_year)
                
                if "error" not in budget_data:
                    # Extract budget amount
                    budget_amount = budget_data.get("total_budgetary_resources", 0)
                    
                    # Add to list
                    agency_budgets.append({
                        "agency_code": agency_code,
                        "agency_name": agency_name,
                        "fiscal_year": fiscal_year,
                        "budget_amount": budget_amount
                    })
            except Exception as e:
                logger.error(f"Error processing budget data for agency {agency_code}: {str(e)}")
    
    # Sort by budget amount (descending) and limit results
    sorted_agencies = sorted(agency_budgets, key=lambda x: x["budget_amount"], reverse=True)
    return sorted_agencies[:limit]

def format_budget_data_for_client(data):
    """
    Format budget data for consumption by the MCP Client.
    
    Args:
        data: Raw budget data (DataFrame or list of dictionaries)
        
    Returns:
        dict: Formatted data ready for the MCP Client
    """
    if isinstance(data, pd.DataFrame):
        # Convert DataFrame to list of dictionaries
        records = data.to_dict(orient="records")
    else:
        records = data
    
    # Format the data according to the expected structure
    formatted_data = {
        "data": records,
        "metadata": {
            "source": "USASpending.gov",
            "retrieved_at": datetime.now().isoformat(),
            "record_count": len(records)
        }
    }
    
    return formatted_data

if __name__ == "__main__":
    # Example usage
    agency_code = "012"  # Department of Agriculture
    fiscal_year = "2023"
    
    # Get budgetary resources
    budget_data = get_agency_budgetary_resources(agency_code, fiscal_year)
    print(json.dumps(budget_data, indent=2))
    
    # Get obligations by award category
    obligations_data = get_agency_obligations_by_award_category(agency_code, fiscal_year)
    print(json.dumps(obligations_data, indent=2))
