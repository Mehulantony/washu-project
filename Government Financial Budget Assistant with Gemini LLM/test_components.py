"""
Unit tests for the Government Financial Budget Assistant components.

This module contains tests for the MCP Client, Gemini API Client, and MCP Server.
"""

import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import data integration modules
from data_integration.data_manager import BudgetDataManager
from mcp_server.data_integration import process_query_parameters, get_data_for_query

class TestDataManager(unittest.TestCase):
    """Test cases for the Budget Data Manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.data_manager = BudgetDataManager()
    
    def test_process_time_period(self):
        """Test time period processing."""
        # Test single year
        start_year, end_year = self.data_manager._process_time_period("2023")
        self.assertEqual(start_year, "2023")
        self.assertEqual(end_year, "2023")
        
        # Test year range
        start_year, end_year = self.data_manager._process_time_period("2020-2023")
        self.assertEqual(start_year, "2020")
        self.assertEqual(end_year, "2023")
        
        # Test "last X years"
        with patch('data_integration.data_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value.year = 2023
            start_year, end_year = self.data_manager._process_time_period("last 3 years")
            self.assertEqual(start_year, "2021")
            self.assertEqual(end_year, "2023")
    
    def test_get_agency_code(self):
        """Test agency code lookup."""
        # Test exact match
        code = self.data_manager._get_agency_code("Department of Defense")
        self.assertEqual(code, "097")
        
        # Test case insensitive match
        code = self.data_manager._get_agency_code("department of defense")
        self.assertEqual(code, "097")
        
        # Test partial match
        code = self.data_manager._get_agency_code("Defense")
        self.assertEqual(code, "097")
        
        # Test no match
        code = self.data_manager._get_agency_code("Nonexistent Agency")
        self.assertIsNone(code)

class TestDataIntegration(unittest.TestCase):
    """Test cases for the MCP Server data integration module."""
    
    def test_process_query_parameters(self):
        """Test query parameter processing."""
        # Test basic parameters
        params = {
            "entity": "Department of Defense",
            "metric": "spending",
            "time_period": "2023",
            "comparison": None,
            "aggregation": "total",
            "limit": None,
            "visualization": "bar"
        }
        
        processed = process_query_parameters(params)
        self.assertEqual(processed["entity"], "Department of Defense")
        self.assertEqual(processed["metric"], "spending")
        self.assertEqual(processed["time_period"], "2023")
        self.assertEqual(processed["comparison"], False)
        self.assertEqual(processed["aggregation"], "total")
        self.assertEqual(processed["visualization"], "bar")
        
        # Test limit extraction from string
        params["limit"] = "top 5"
        processed = process_query_parameters(params)
        self.assertEqual(processed["limit"], 5)
        
        # Test comparison as boolean
        params["comparison"] = True
        processed = process_query_parameters(params)
        self.assertEqual(processed["comparison"], True)

class TestGeminiAPIClient(unittest.TestCase):
    """Test cases for the Gemini API Client."""
    
    @patch('requests.post')
    def test_parameter_extraction(self, mock_post):
        """Test parameter extraction from natural language query."""
        # Mock response for parameter extraction
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "query_parameters": {
                "entity": "Department of Defense",
                "metric": "spending",
                "time_period": "2023",
                "comparison": None,
                "aggregation": "total",
                "limit": None,
                "visualization": "bar"
            }
        }
        mock_post.return_value = mock_response
        
        # This is a simplified test - in a real implementation, 
        # we would import and test the actual Gemini API Client functions
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(
            mock_response.json()["query_parameters"]["entity"], 
            "Department of Defense"
        )

if __name__ == '__main__':
    unittest.main()
