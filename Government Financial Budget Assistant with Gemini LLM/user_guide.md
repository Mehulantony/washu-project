# User Guide: Government Financial Budget Assistant

This guide provides instructions on how to use the Government Financial Budget Assistant to query and analyze U.S. government budget data using natural language.

## Getting Started

1. Access the application at: http://localhost:3000
2. You'll be presented with the main dashboard interface

## Submitting Queries

1. Type your question about government budget data in the query input box
2. Click the "Submit" button or press Enter
3. The system will process your query and display the results

### Example Queries

Try asking questions like:
- "What was the Department of Defense budget for fiscal year 2023?"
- "Compare education spending between 2020 and 2022"
- "Show me the top 5 departments by budget allocation in 2023"
- "What percentage of the federal budget went to healthcare in 2022?"
- "How has infrastructure spending changed over the last 5 years?"

## Understanding Results

The results are displayed in three main sections:

1. **Visualization**: Shows your data in chart form (bar, line, pie, or doughnut)
2. **Insights**: Provides natural language explanations of the data
3. **Data Table**: Shows the raw data in tabular format

### Changing Visualization Type

Use the dropdown menu above the visualization to switch between different chart types:
- Bar Chart: Good for comparing values across categories
- Line Chart: Best for showing trends over time
- Pie Chart: Useful for showing proportions of a whole
- Doughnut Chart: Similar to pie chart but with a hole in the center

## Query History

1. Click on "Query History" in the navigation menu
2. View a list of your previous queries
3. Click on any query to re-run it

## Tips for Effective Queries

- Be specific about the time period (e.g., "fiscal year 2023" or "2020-2022")
- Mention the specific department or agency if you want focused results
- Specify the type of visualization if you have a preference (e.g., "show as a line chart")
- Use comparison terms like "compare," "versus," or "difference between" for comparative analysis
- Specify limits like "top 5" or "bottom 10" to focus on the most relevant data

## Troubleshooting

If you encounter issues:

1. **No results displayed**: Try rephrasing your query to be more specific
2. **Incorrect data**: Ensure you're specifying the correct fiscal year and department
3. **System not responding**: Check if all components are running using `./run.sh`
4. **Visualization not loading**: Try switching to a different chart type

## Advanced Features

### Data Export

Currently, data export is not supported directly from the interface. However, you can:
1. Take screenshots of visualizations
2. Copy data from the data table

### Custom Date Ranges

For custom date ranges, use formats like:
- "last 5 years"
- "2018-2023"
- "from 2020 to 2023"

## Getting Help

For additional assistance, please refer to:
- The README.md file for technical details
- The architecture.md file for system design information
- Contact your system administrator for access issues
