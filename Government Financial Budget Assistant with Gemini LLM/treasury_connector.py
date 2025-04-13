"""
Treasury.gov API Connector for Government Financial Budget Assistant

This module provides functions to retrieve budget data from the Treasury.gov Fiscal Service API.
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
BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
API_KEY = os.getenv("TREASURY_API_KEY", "")

# Headers for API requests
HEADERS = {
    "Content-Type": "application/json"
}
if API_KEY:
    HEADERS["X-API-Key"] = API_KEY

def get_debt_to_penny(start_date=None, end_date=None):
    """
    Retrieve the daily U.S. national debt data.
    
    Args:
        start_date (str, optional): Start date in YYYY-MM-DD format
        end_date (str, optional): End date in YYYY-MM-DD format
        
    Returns:
        dict: JSON response containing debt data
    """
    endpoint = f"{BASE_URL}/v2/accounting/od/debt_to_penny"
    params = {
        "format": "json",
        "page[size]": 10000
    }
    
    if start_date:
        params["filter"] = f"record_date:gte:{start_date}"
        if end_date:
            params["filter"] += f",record_date:lte:{end_date}"
    elif end_date:
        params["filter"] = f"record_date:lte:{end_date}"
    
    try:
        logger.info(f"Fetching debt to penny data from {start_date} to {end_date}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching debt to penny data: {str(e)}")
        return {"error": str(e)}

def get_monthly_treasury_statement(fiscal_year=None):
    """
    Retrieve Monthly Treasury Statement (MTS) data for federal budget receipts and outlays.
    
    Args:
        fiscal_year (str, optional): The fiscal year (e.g., "2023")
        
    Returns:
        dict: JSON response containing MTS data
    """
    endpoint = f"{BASE_URL}/v1/accounting/mts/mts_table_5"
    params = {
        "format": "json",
        "page[size]": 10000
    }
    
    if fiscal_year:
        params["filter"] = f"fiscal_year:eq:{fiscal_year}"
    
    try:
        logger.info(f"Fetching Monthly Treasury Statement data for FY {fiscal_year}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Monthly Treasury Statement data: {str(e)}")
        return {"error": str(e)}

def get_federal_budget_outlays(fiscal_year=None):
    """
    Retrieve federal budget outlays by agency and account.
    
    Args:
        fiscal_year (str, optional): The fiscal year (e.g., "2023")
        
    Returns:
        dict: JSON response containing federal budget outlays data
    """
    endpoint = f"{BASE_URL}/v1/accounting/mts/mts_table_9"
    params = {
        "format": "json",
        "page[size]": 10000
    }
    
    if fiscal_year:
        params["filter"] = f"fiscal_year:eq:{fiscal_year}"
    
    try:
        logger.info(f"Fetching federal budget outlays data for FY {fiscal_year}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching federal budget outlays data: {str(e)}")
        return {"error": str(e)}

def get_federal_budget_receipts(fiscal_year=None):
    """
    Retrieve federal budget receipts by source.
    
    Args:
        fiscal_year (str, optional): The fiscal year (e.g., "2023")
        
    Returns:
        dict: JSON response containing federal budget receipts data
    """
    endpoint = f"{BASE_URL}/v1/accounting/mts/mts_table_4"
    params = {
        "format": "json",
        "page[size]": 10000
    }
    
    if fiscal_year:
        params["filter"] = f"fiscal_year:eq:{fiscal_year}"
    
    try:
        logger.info(f"Fetching federal budget receipts data for FY {fiscal_year}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching federal budget receipts data: {str(e)}")
        return {"error": str(e)}

def get_deficit_analysis(fiscal_year=None):
    """
    Retrieve deficit analysis data.
    
    Args:
        fiscal_year (str, optional): The fiscal year (e.g., "2023")
        
    Returns:
        dict: JSON response containing deficit analysis data
    """
    endpoint = f"{BASE_URL}/v1/accounting/mts/mts_table_1"
    params = {
        "format": "json",
        "page[size]": 10000
    }
    
    if fiscal_year:
        params["filter"] = f"fiscal_year:eq:{fiscal_year}"
    
    try:
        logger.info(f"Fetching deficit analysis data for FY {fiscal_year}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching deficit analysis data: {str(e)}")
        return {"error": str(e)}

def get_agency_expenditures(fiscal_year=None, agency_name=None):
    """
    Retrieve agency expenditures data.
    
    Args:
        fiscal_year (str, optional): The fiscal year (e.g., "2023")
        agency_name (str, optional): The name of the agency to filter by
        
    Returns:
        dict: JSON response containing agency expenditures data
    """
    endpoint = f"{BASE_URL}/v1/accounting/mts/mts_table_5"
    params = {
        "format": "json",
        "page[size]": 10000
    }
    
    filter_params = []
    if fiscal_year:
        filter_params.append(f"fiscal_year:eq:{fiscal_year}")
    if agency_name:
        filter_params.append(f"current_fytd_net_outly_amt:gt:0,classification_desc:contains:{agency_name}")
    
    if filter_params:
        params["filter"] = ",".join(filter_params)
    
    try:
        logger.info(f"Fetching agency expenditures data for FY {fiscal_year}, agency {agency_name}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching agency expenditures data: {str(e)}")
        return {"error": str(e)}

def get_historical_debt(start_year=None, end_year=None):
    """
    Retrieve historical debt data.
    
    Args:
        start_year (str, optional): Start year (e.g., "2010")
        end_year (str, optional): End year (e.g., "2023")
        
    Returns:
        dict: JSON response containing historical debt data
    """
    endpoint = f"{BASE_URL}/v2/accounting/od/debt_outstanding"
    params = {
        "format": "json",
        "page[size]": 10000,
        "sort": "-record_date"
    }
    
    filter_params = []
    if start_year:
        start_date = f"{start_year}-01-01"
        filter_params.append(f"record_date:gte:{start_date}")
    if end_year:
        end_date = f"{end_year}-12-31"
        filter_params.append(f"record_date:lte:{end_date}")
    
    if filter_params:
        params["filter"] = ",".join(filter_params)
    
    try:
        logger.info(f"Fetching historical debt data from {start_year} to {end_year}")
        response = requests.get(endpoint, params=params, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching historical debt data: {str(e)}")
        return {"error": str(e)}

def format_treasury_data_for_client(data, data_type):
    """
    Format Treasury.gov data for consumption by the MCP Client.
    
    Args:
        data: Raw Treasury.gov data
        data_type (str): Type of data (e.g., "debt", "outlays", "receipts")
        
    Returns:
        dict: Formatted data ready for the MCP Client
    """
    if "error" in data:
        return {"error": data["error"]}
    
    if "data" not in data:
        return {"error": "Invalid data format from Treasury.gov API"}
    
    # Format the data according to the expected structure
    formatted_data = {
        "data": data["data"],
        "metadata": {
            "source": "Treasury.gov",
            "data_type": data_type,
            "retrieved_at": datetime.now().isoformat(),
            "record_count": len(data["data"]),
            "api_info": data.get("meta", {})
        }
    }
    
    return formatted_data

def get_budget_comparison_by_years(start_year, end_year, agency_name=None):
    """
    Compare budget data between two fiscal years, optionally filtered by agency.
    
    Args:
        start_year (str): Starting fiscal year (e.g., "2020")
        end_year (str): Ending fiscal year (e.g., "2023")
        agency_name (str, optional): Name of the agency to filter by
        
    Returns:
        dict: Comparison data between the two fiscal years
    """
    # Get data for both years
    start_year_data = get_federal_budget_outlays(start_year)
    end_year_data = get_federal_budget_outlays(end_year)
    
    if "error" in start_year_data or "error" in end_year_data:
        return {"error": "Failed to retrieve data for comparison"}
    
    # Convert to DataFrames
    start_df = pd.DataFrame(start_year_data["data"])
    end_df = pd.DataFrame(end_year_data["data"])
    
    # Filter by agency if specified
    if agency_name:
        start_df = start_df[start_df["classification_desc"].str.contains(agency_name, case=False, na=False)]
        end_df = end_df[end_df["classification_desc"].str.contains(agency_name, case=False, na=False)]
    
    # Prepare comparison data
    comparison_data = []
    
    # Group by agency/department
    start_grouped = start_df.groupby("classification_desc").sum().reset_index()
    end_grouped = end_df.groupby("classification_desc").sum().reset_index()
    
    # Merge the data
    merged_df = pd.merge(
        start_grouped[["classification_desc", "current_fytd_net_outly_amt"]], 
        end_grouped[["classification_desc", "current_fytd_net_outly_amt"]], 
        on="classification_desc", 
        how="outer",
        suffixes=(f"_{start_year}", f"_{end_year}")
    )
    
    # Fill NaN values with 0
    merged_df = merged_df.fillna(0)
    
    # Calculate change and percentage change
    merged_df[f"change_{start_year}_to_{end_year}"] = merged_df[f"current_fytd_net_outly_amt_{end_year}"] - merged_df[f"current_fytd_net_outly_amt_{start_year}"]
    merged_df[f"percent_change_{start_year}_to_{end_year}"] = (
        (merged_df[f"current_fytd_net_outly_amt_{end_year}"] - merged_df[f"current_fytd_net_outly_amt_{start_year}"]) / 
        merged_df[f"current_fytd_net_outly_amt_{start_year}"] * 100
    ).replace([float('inf'), -float('inf')], 0)
    
    # Convert to list of dictionaries
    comparison_data = merged_df.to_dict(orient="records")
    
    return {
        "data": comparison_data,
        "metadata": {
            "source": "Treasury.gov",
            "data_type": "budget_comparison",
            "start_year": start_year,
            "end_year": end_year,
            "agency_filter": agency_name,
            "retrieved_at": datetime.now().isoformat(),
            "record_count": len(comparison_data)
        }
    }

if __name__ == "__main__":
    # Example usage
    fiscal_year = "2023"
    
    # Get Monthly Treasury Statement data
    mts_data = get_monthly_treasury_statement(fiscal_year)
    print(json.dumps(mts_data, indent=2))
    
    # Get federal budget outlays
    outlays_data = get_federal_budget_outlays(fiscal_year)
    print(json.dumps(outlays_data, indent=2))
