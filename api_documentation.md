# API Documentation: Government Financial Budget Assistant

This document provides detailed information about the APIs used in the Government Financial Budget Assistant system.

## MCP Client to Gemini API Client

### Query Submission

**Endpoint:** `POST /api/query`

**Description:** Submit a natural language query for processing

**Request Body:**
```json
{
  "query": "What was the Department of Defense budget for fiscal year 2023?",
  "user_id": "optional_user_id"
}
```

**Response:**
```json
{
  "query": "What was the Department of Defense budget for fiscal year 2023?",
  "query_parameters": {
    "entity": "Department of Defense",
    "metric": "budget",
    "time_period": "2023",
    "comparison": null,
    "aggregation": null,
    "limit": null,
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
```

### Query History

**Endpoint:** `GET /api/history`

**Description:** Retrieve query history for a user

**Query Parameters:**
- `user_id` (optional): ID of the user to retrieve history for

**Response:**
```json
{
  "queries": [
    {
      "id": "1649812345",
      "query": "What was the Department of Defense budget for fiscal year 2023?",
      "timestamp": "2025-04-12T21:45:30.000Z",
      "parameters": {
        "entity": "Department of Defense",
        "metric": "budget",
        "time_period": "2023"
      }
    }
  ]
}
```

## Gemini API Client to MCP Server

### Data Retrieval

**Endpoint:** `POST /api/data`

**Description:** Retrieve budget data based on structured parameters

**Request Body:**
```json
{
  "entity": "Department of Defense",
  "metric": "budget",
  "time_period": "2023",
  "comparison": false,
  "aggregation": null,
  "limit": null,
  "visualization": "bar"
}
```

**Response:**
```json
{
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
```

### Available Agencies

**Endpoint:** `GET /api/departments`

**Description:** Get a list of available government departments/agencies

**Response:**
```json
{
  "departments": [
    "Department of Agriculture",
    "Department of Commerce",
    "Department of Defense",
    "Department of Education",
    "Department of Energy"
  ]
}
```

### Available Fiscal Years

**Endpoint:** `GET /api/years`

**Description:** Get a list of available fiscal years

**Response:**
```json
{
  "fiscal_years": [
    "2023",
    "2022",
    "2021",
    "2020",
    "2019"
  ]
}
```

## External APIs

### USASpending.gov API

The system integrates with the USASpending.gov API to retrieve federal spending data.

**Key Endpoints Used:**
- `/api/v2/agency/<TOPTIER_AGENCY_CODE>/budgetary_resources/`: Returns budgetary resources and obligations for the agency and fiscal year requested
- `/api/v2/agency/<TOPTIER_AGENCY_CODE>/obligations_by_award_category/`: Returns a breakdown of obligations by award category within a single fiscal year
- `/api/v2/agency/<TOPTIER_AGENCY_CODE>/federal_account/`: Returns a list of Federal Accounts and Treasury Accounts for the agency in a single fiscal year

For full documentation, visit: https://api.usaspending.gov/docs/endpoints

### Treasury.gov Fiscal Service API

The system integrates with the Treasury.gov Fiscal Service API to retrieve debt, deficit, and receipts data.

**Key Endpoints Used:**
- `/v2/accounting/od/debt_to_penny`: Retrieves the daily U.S. national debt data
- `/v1/accounting/mts/mts_table_5`: Retrieves Monthly Treasury Statement (MTS) data for federal budget receipts and outlays
- `/v1/accounting/mts/mts_table_9`: Retrieves federal budget outlays by agency and account
- `/v1/accounting/mts/mts_table_4`: Retrieves federal budget receipts by source

For full documentation, visit: https://fiscaldata.treasury.gov/api-documentation/

## Error Handling

All APIs return standard HTTP status codes:

- `200`: Success
- `400`: Bad request (invalid parameters)
- `401`: Unauthorized (authentication required)
- `404`: Resource not found
- `500`: Server error

Error responses include a detail message:

```json
{
  "detail": "Error message describing the issue"
}
```
