"""
Data Integration Manager for Government Financial Budget Assistant

This module integrates data connectors for USASpending.gov and Treasury.gov
and provides a unified interface for the MCP Server to access budget data.
"""

import os
import logging
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Import data connectors
from usaspending_connector import (
    get_agency_budgetary_resources,
    get_agency_obligations_by_award_category,
    get_federal_accounts_by_agency,
    get_agency_overview,
    get_budget_data_by_time_period,
    get_top_agencies_by_budget,
    format_budget_data_for_client
)
from treasury_connector import (
    get_monthly_treasury_statement,
    get_federal_budget_outlays,
    get_federal_budget_receipts,
    get_deficit_analysis,
    get_agency_expenditures,
    get_historical_debt,
    get_budget_comparison_by_years,
    format_treasury_data_for_client
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
ENABLE_MOCK_DATA = os.getenv("ENABLE_MOCK_DATA", "true").lower() == "true"

class BudgetDataManager:
    """
    Manager class for retrieving and processing budget data from various sources.
    """
    
    def __init__(self):
        """Initialize the Budget Data Manager."""
        self.use_mock_data = ENABLE_MOCK_DATA
        logger.info(f"Budget Data Manager initialized. Using mock data: {self.use_mock_data}")
    
    def get_budget_data(self, parameters):
        """
        Retrieve budget data based on the provided parameters.
        
        Args:
            parameters (dict): Query parameters extracted from natural language query
                - entity: The government department, agency, or program
                - metric: The financial metric (spending, budget, allocation, funding)
                - time_period: The fiscal year or time range
                - comparison: Whether a comparison is requested
                - aggregation: The type of aggregation requested
                - limit: Number of results requested
                - visualization: Suggested visualization type
                
        Returns:
            dict: Formatted budget data for the MCP Client
        """
        logger.info(f"Retrieving budget data with parameters: {parameters}")
        
        # Extract parameters
        entity = parameters.get("entity")
        metric = parameters.get("metric")
        time_period = parameters.get("time_period")
        comparison = parameters.get("comparison")
        aggregation = parameters.get("aggregation")
        limit = parameters.get("limit")
        
        # Process time period
        start_year, end_year = self._process_time_period(time_period)
        
        # Determine which data source to use based on the metric
        if metric in ["spending", "outlays", "expenditures"]:
            # Use Treasury.gov for spending data
            return self._get_spending_data(entity, start_year, end_year, comparison, aggregation, limit)
        elif metric in ["budget", "allocation", "funding", "resources"]:
            # Use USASpending.gov for budget allocation data
            return self._get_budget_allocation_data(entity, start_year, end_year, comparison, aggregation, limit)
        elif metric in ["debt", "deficit"]:
            # Use Treasury.gov for debt and deficit data
            return self._get_debt_deficit_data(start_year, end_year, comparison)
        elif metric in ["receipts", "revenue", "income"]:
            # Use Treasury.gov for receipts data
            return self._get_receipts_data(start_year, end_year, comparison)
        else:
            # Default to budget allocation data
            return self._get_budget_allocation_data(entity, start_year, end_year, comparison, aggregation, limit)
    
    def _process_time_period(self, time_period):
        """
        Process the time period parameter to extract start and end years.
        
        Args:
            time_period (str): Time period string from query parameters
            
        Returns:
            tuple: (start_year, end_year)
        """
        if not time_period:
            # Default to current year
            current_year = datetime.now().year
            return str(current_year), str(current_year)
        
        if "-" in time_period:
            # Handle range like "2020-2022"
            parts = time_period.split("-")
            return parts[0], parts[1]
        elif "last" in time_period.lower() and "years" in time_period.lower():
            # Handle "last X years"
            import re
            match = re.search(r'last (\d+)', time_period.lower())
            if match:
                num_years = int(match.group(1))
                current_year = datetime.now().year
                return str(current_year - num_years + 1), str(current_year)
        
        # Single year
        return time_period, time_period
    
    def _get_spending_data(self, entity, start_year, end_year, comparison, aggregation, limit):
        """
        Retrieve spending data from Treasury.gov.
        
        Args:
            entity (str): Agency or department name
            start_year (str): Start fiscal year
            end_year (str): End fiscal year
            comparison (bool): Whether to compare years
            aggregation (str): Type of aggregation
            limit (int): Number of results to return
            
        Returns:
            dict: Formatted spending data
        """
        if comparison:
            # Get comparison data between years
            data = get_budget_comparison_by_years(start_year, end_year, entity)
        else:
            # Get spending data for a single year or range
            if start_year == end_year:
                # Single year
                data = get_federal_budget_outlays(start_year)
                if entity:
                    # Filter by agency
                    agency_data = get_agency_expenditures(start_year, entity)
                    data = agency_data if "error" not in agency_data else data
            else:
                # Multiple years - get data for each year and combine
                all_data = []
                for year in range(int(start_year), int(end_year) + 1):
                    year_data = get_federal_budget_outlays(str(year))
                    if "error" not in year_data and "data" in year_data:
                        all_data.extend(year_data["data"])
                
                data = {"data": all_data, "meta": {"record_count": len(all_data)}}
        
        # Apply limit if specified
        if limit and "data" in data and len(data["data"]) > limit:
            data["data"] = data["data"][:limit]
            if "meta" in data:
                data["meta"]["record_count"] = limit
        
        return format_treasury_data_for_client(data, "spending")
    
    def _get_budget_allocation_data(self, entity, start_year, end_year, comparison, aggregation, limit):
        """
        Retrieve budget allocation data from USASpending.gov.
        
        Args:
            entity (str): Agency or department name
            start_year (str): Start fiscal year
            end_year (str): End fiscal year
            comparison (bool): Whether to compare years
            aggregation (str): Type of aggregation
            limit (int): Number of results to return
            
        Returns:
            dict: Formatted budget allocation data
        """
        if comparison:
            # Get data for multiple years for comparison
            data = get_budget_data_by_time_period(entity, start_year, end_year)
            formatted_data = format_budget_data_for_client(data)
        else:
            if start_year == end_year:
                # Single year
                if entity:
                    # Get data for specific agency
                    agency_code = self._get_agency_code(entity)
                    if agency_code:
                        data = get_agency_budgetary_resources(agency_code, start_year)
                        formatted_data = format_budget_data_for_client(data)
                    else:
                        # Agency not found, get top agencies
                        data = get_top_agencies_by_budget(start_year, limit or 10)
                        formatted_data = format_budget_data_for_client(data)
                else:
                    # No specific agency, get top agencies by budget
                    data = get_top_agencies_by_budget(start_year, limit or 10)
                    formatted_data = format_budget_data_for_client(data)
            else:
                # Multiple years
                data = get_budget_data_by_time_period(entity, start_year, end_year)
                formatted_data = format_budget_data_for_client(data)
        
        return formatted_data
    
    def _get_debt_deficit_data(self, start_year, end_year, comparison):
        """
        Retrieve debt and deficit data from Treasury.gov.
        
        Args:
            start_year (str): Start fiscal year
            end_year (str): End fiscal year
            comparison (bool): Whether to compare years
            
        Returns:
            dict: Formatted debt and deficit data
        """
        if comparison or start_year != end_year:
            # Get historical debt data for the specified range
            data = get_historical_debt(start_year, end_year)
        else:
            # Get deficit analysis for a single year
            data = get_deficit_analysis(start_year)
        
        return format_treasury_data_for_client(data, "debt_deficit")
    
    def _get_receipts_data(self, start_year, end_year, comparison):
        """
        Retrieve receipts (revenue) data from Treasury.gov.
        
        Args:
            start_year (str): Start fiscal year
            end_year (str): End fiscal year
            comparison (bool): Whether to compare years
            
        Returns:
            dict: Formatted receipts data
        """
        if comparison or start_year != end_year:
            # Get receipts data for multiple years
            all_data = []
            for year in range(int(start_year), int(end_year) + 1):
                year_data = get_federal_budget_receipts(str(year))
                if "error" not in year_data and "data" in year_data:
                    all_data.extend(year_data["data"])
            
            data = {"data": all_data, "meta": {"record_count": len(all_data)}}
        else:
            # Get receipts data for a single year
            data = get_federal_budget_receipts(start_year)
        
        return format_treasury_data_for_client(data, "receipts")
    
    def _get_agency_code(self, agency_name):
        """
        Get the agency code for a given agency name.
        
        Args:
            agency_name (str): Name of the agency
            
        Returns:
            str: Agency code if found, None otherwise
        """
        # This is a simplified implementation
        # In a real system, this would query a database or API to get the agency code
        
        # Common agency codes
        agency_codes = {
            "department of agriculture": "012",
            "department of commerce": "013",
            "department of defense": "097",
            "department of education": "091",
            "department of energy": "089",
            "department of health and human services": "075",
            "department of homeland security": "070",
            "department of housing and urban development": "086",
            "department of the interior": "014",
            "department of justice": "015",
            "department of labor": "016",
            "department of state": "019",
            "department of transportation": "069",
            "department of the treasury": "020",
            "department of veterans affairs": "036",
            "environmental protection agency": "068",
            "national aeronautics and space administration": "080",
            "national science foundation": "049",
            "small business administration": "073",
            "social security administration": "028"
        }
        
        if not agency_name:
            return None
        
        # Normalize agency name
        normalized_name = agency_name.lower().strip()
        
        # Check for exact match
        if normalized_name in agency_codes:
            return agency_codes[normalized_name]
        
        # Check for partial match
        for name, code in agency_codes.items():
            if normalized_name in name or name in normalized_name:
                return code
        
        return None

# Create a singleton instance
budget_data_manager = BudgetDataManager()

def get_budget_data(parameters):
    """
    Main function to retrieve budget data based on query parameters.
    
    Args:
        parameters (dict): Query parameters extracted from natural language query
            
    Returns:
        dict: Formatted budget data for the MCP Client
    """
    return budget_data_manager.get_budget_data(parameters)
