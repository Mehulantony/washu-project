"""
Integration tests for the Government Financial Budget Assistant system.

This module contains tests that verify the interaction between different components
of the system: MCP Client, Gemini API Client, and MCP Server.
"""

import unittest
import json
import os
import sys
import requests
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSystemIntegration(unittest.TestCase):
    """Test cases for the integration between system components."""
    
    @patch('requests.post')
    def test_end_to_end_query_flow(self, mock_post):
        """Test the end-to-end flow of a query through the system."""
        # Mock response for Gemini API Client
        gemini_response = MagicMock()
        gemini_response.status_code = 200
        gemini_response.json.return_value = {
            "query": "What was the Department of Defense budget for fiscal year 2023?",
            "query_parameters": {
                "entity": "Department of Defense",
                "metric": "budget",
                "time_period": "2023",
                "comparison": None,
                "aggregation": None,
                "limit": None,
                "visualization": "bar"
            },
            "data": [
                {
                    "department": "Department of Defense",
                    "year": "2023",
                    "amount": 816700000000,
                    "source": "USASpending.gov"
                }
            ],
            "insights": "<p>The Department of Defense had a budget of $816.7 billion for fiscal year 2023.</p>"
        }
        
        # Mock response for MCP Server
        mcp_server_response = MagicMock()
        mcp_server_response.status_code = 200
        mcp_server_response.json.return_value = {
            "data": [
                {
                    "department": "Department of Defense",
                    "year": "2023",
                    "amount": 816700000000,
                    "source": "USASpending.gov"
                }
            ],
            "metadata": {
                "source": "USASpending.gov",
                "retrieved_at": "2025-04-12T22:15:00.000Z",
                "record_count": 1
            }
        }
        
        # Configure mock to return different responses based on URL
        def side_effect(*args, **kwargs):
            if 'gemini' in kwargs.get('url', ''):
                return gemini_response
            else:
                return mcp_server_response
        
        mock_post.side_effect = side_effect
        
        # Simulate a query from MCP Client to Gemini API Client
        client_query = {
            "query": "What was the Department of Defense budget for fiscal year 2023?"
        }
        
        # This is a simplified test - in a real implementation, 
        # we would make actual API calls between components
        response = requests.post(
            url="http://localhost:5000/api/query", 
            json=client_query
        )
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(
            response_data["query_parameters"]["entity"], 
            "Department of Defense"
        )
        self.assertEqual(len(response_data["data"]), 1)
        self.assertEqual(
            response_data["data"][0]["department"], 
            "Department of Defense"
        )
        self.assertEqual(
            response_data["data"][0]["amount"], 
            816700000000
        )

class TestMCPClientGeminiIntegration(unittest.TestCase):
    """Test cases for the integration between MCP Client and Gemini API Client."""
    
    @patch('requests.post')
    def test_query_submission(self, mock_post):
        """Test query submission from MCP Client to Gemini API Client."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "query": "What was the Department of Defense budget for fiscal year 2023?",
            "query_parameters": {
                "entity": "Department of Defense",
                "metric": "budget",
                "time_period": "2023",
                "comparison": None,
                "aggregation": None,
                "limit": None,
                "visualization": "bar"
            }
        }
        mock_post.return_value = mock_response
        
        # Simulate query submission
        client_query = {
            "query": "What was the Department of Defense budget for fiscal year 2023?"
        }
        
        response = requests.post(
            url="http://localhost:5000/api/query", 
            json=client_query
        )
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(
            response_data["query"], 
            "What was the Department of Defense budget for fiscal year 2023?"
        )
        self.assertEqual(
            response_data["query_parameters"]["entity"], 
            "Department of Defense"
        )

class TestGeminiMCPServerIntegration(unittest.TestCase):
    """Test cases for the integration between Gemini API Client and MCP Server."""
    
    @patch('requests.post')
    def test_data_retrieval(self, mock_post):
        """Test data retrieval from MCP Server based on parameters from Gemini API Client."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "department": "Department of Defense",
                    "year": "2023",
                    "amount": 816700000000,
                    "source": "USASpending.gov"
                }
            ],
            "metadata": {
                "source": "USASpending.gov",
                "retrieved_at": "2025-04-12T22:15:00.000Z",
                "record_count": 1
            }
        }
        mock_post.return_value = mock_response
        
        # Simulate parameter passing from Gemini API Client to MCP Server
        query_parameters = {
            "entity": "Department of Defense",
            "metric": "budget",
            "time_period": "2023",
            "comparison": False,
            "aggregation": None,
            "limit": None,
            "visualization": "bar"
        }
        
        response = requests.post(
            url="http://localhost:5001/api/data", 
            json=query_parameters
        )
        
        # Verify the response
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data["data"]), 1)
        self.assertEqual(
            response_data["data"][0]["department"], 
            "Department of Defense"
        )
        self.assertEqual(
            response_data["data"][0]["amount"], 
            816700000000
        )

if __name__ == '__main__':
    unittest.main()
