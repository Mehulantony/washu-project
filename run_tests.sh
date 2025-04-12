#!/bin/bash

# Test script for the Government Financial Budget Assistant
# This script runs all unit and integration tests

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Running tests for Government Financial Budget Assistant...${NC}"

# Create logs directory if it doesn't exist
mkdir -p logs

# Run unit tests
echo -e "${GREEN}Running unit tests...${NC}"
cd tests
python3 -m unittest test_components.py > ../logs/unit_tests.log 2>&1
UNIT_TEST_RESULT=$?

if [ $UNIT_TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}Unit tests passed successfully!${NC}"
else
    echo -e "${RED}Unit tests failed. Check logs/unit_tests.log for details.${NC}"
fi

# Run integration tests
echo -e "${GREEN}Running integration tests...${NC}"
python3 -m unittest test_integration.py > ../logs/integration_tests.log 2>&1
INTEGRATION_TEST_RESULT=$?

if [ $INTEGRATION_TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}Integration tests passed successfully!${NC}"
else
    echo -e "${RED}Integration tests failed. Check logs/integration_tests.log for details.${NC}"
fi

cd ..

# Overall test result
if [ $UNIT_TEST_RESULT -eq 0 ] && [ $INTEGRATION_TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}All tests passed successfully!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Check logs for details.${NC}"
    exit 1
fi
