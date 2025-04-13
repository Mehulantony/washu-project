"""
Integration module for connecting the MCP Server with data sources.

This module integrates the data manager with the MCP Server to provide
access to government budget data from USASpending.gov and Treasury.gov.
"""

import os
import sys
import logging
from pathlib import Path

# Add data_integration directory to path
current_dir = Path(__file__).resolve().parent
data_integration_dir = current_dir.parent / "data_integration"
sys.path.append(str(data_integration_dir))

# Import data manager
from data_manager import get_budget_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_query_parameters(parameters):
    """
    Process query parameters from the Gemini API Client and prepare them
    for the data manager.
    
    Args:
        parameters (dict): Parameters extracted by Gemini LLM
            
    Returns:
        dict: Processed parameters for the data manager
    """
    logger.info(f"Processing query parameters: {parameters}")
    
    # Extract parameters
    entity = parameters.get("entity")
    metric = parameters.get("metric")
    time_period = parameters.get("time_period")
    comparison = parameters.get("comparison")
    aggregation = parameters.get("aggregation")
    limit = parameters.get("limit")
    visualization = parameters.get("visualization")
    
    # Process limit parameter
    if isinstance(limit, str) and limit:
        # Extract numeric value from strings like "top 5"
        import re
        match = re.search(r'(\d+)', limit)
        if match:
            limit = int(match.group(1))
        else:
            limit = 10  # Default limit
    
    # Prepare processed parameters
    processed_params = {
        "entity": entity,
        "metric": metric,
        "time_period": time_period,
        "comparison": bool(comparison),
        "aggregation": aggregation,
        "limit": limit,
        "visualization": visualization
    }
    
    logger.info(f"Processed parameters: {processed_params}")
    return processed_params

def get_data_for_query(parameters):
    """
    Main function to retrieve budget data based on query parameters.
    
    Args:
        parameters (dict): Parameters extracted by Gemini LLM
            
    Returns:
        dict: Formatted budget data for the MCP Client
    """
    # Process parameters
    processed_params = process_query_parameters(parameters)
    
    # Get data from data manager
    data = get_budget_data(processed_params)
    
    # Add visualization suggestion if not already present
    if "metadata" in data and not data.get("metadata", {}).get("visualization"):
        data["metadata"]["visualization"] = processed_params.get("visualization", "bar")
    
    return data

def get_available_agencies():
    """
    Get a list of available government agencies.
    
    Returns:
        list: List of agency names
    """
    # This would typically query the data sources
    # For now, return a static list of major agencies
    return [
        "Department of Agriculture",
        "Department of Commerce",
        "Department of Defense",
        "Department of Education",
        "Department of Energy",
        "Department of Health and Human Services",
        "Department of Homeland Security",
        "Department of Housing and Urban Development",
        "Department of the Interior",
        "Department of Justice",
        "Department of Labor",
        "Department of State",
        "Department of Transportation",
        "Department of the Treasury",
        "Department of Veterans Affairs",
        "Environmental Protection Agency",
        "National Aeronautics and Space Administration",
        "National Science Foundation",
        "Small Business Administration",
        "Social Security Administration"
    ]

def get_available_fiscal_years():
    """
    Get a list of available fiscal years.
    
    Returns:
        list: List of fiscal years
    """
    # This would typically query the data sources
    # For now, return a static list of recent fiscal years
    current_year = 2023  # In a real implementation, this would be dynamic
    return [str(year) for year in range(current_year - 9, current_year + 1)]
