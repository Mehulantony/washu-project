import React from 'react';

const About = () => {
  return (
    <div className="about-container">
      <div className="row mb-4">
        <div className="col-12">
          <h1>About the Government Financial Budget Assistant</h1>
        </div>
      </div>

      <div className="row">
        <div className="col-12">
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Overview</h5>
              <p className="card-text">
                The Government Financial Budget Assistant is a powerful tool designed for government finance officers and analysts to query and analyze U.S. government budget data using natural language. 
                This system leverages Google's Gemini Large Language Model (LLM) and follows the Model Context Protocol (MCP) architecture to process queries and provide detailed budget insights.
              </p>
            </div>
          </div>

          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">How It Works</h5>
              <p className="card-text">
                The system uses a three-component architecture:
              </p>
              <ol>
                <li>
                  <strong>MCP Client (Frontend):</strong> The user interface where you can submit natural language queries and view visualized results.
                </li>
                <li>
                  <strong>Gemini API Client:</strong> Processes your natural language queries using Google's Gemini LLM to extract structured parameters.
                </li>
                <li>
                  <strong>MCP Server (Backend):</strong> Retrieves and processes budget data from various U.S. government data sources based on the extracted parameters.
                </li>
              </ol>
            </div>
          </div>

          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Data Sources</h5>
              <p className="card-text">
                The Government Financial Budget Assistant integrates with several authoritative U.S. government budget data sources:
              </p>
              <ul>
                <li><strong>USASpending.gov API:</strong> Detailed federal spending data on contracts, grants, loans, and other financial assistance.</li>
                <li><strong>Treasury.gov APIs:</strong> Data on federal debt, revenue, and spending, including fiscal service data.</li>
                <li><strong>Data.gov Budget APIs:</strong> Various budget-related datasets and historical budget data.</li>
                <li><strong>Federal Reserve Economic Data (FRED):</strong> Economic indicators related to government spending and historical context.</li>
              </ul>
            </div>
          </div>

          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Example Queries</h5>
              <p className="card-text">
                You can ask questions like:
              </p>
              <ul>
                <li>"What was the Department of Defense budget for fiscal year 2023?"</li>
                <li>"Compare education spending between 2020 and 2022"</li>
                <li>"Show me the top 5 departments by budget allocation in 2023"</li>
                <li>"What percentage of the federal budget went to healthcare in 2022?"</li>
                <li>"How has infrastructure spending changed over the last 5 years?"</li>
              </ul>
            </div>
          </div>

          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Technology Stack</h5>
              <p className="card-text">
                The Government Financial Budget Assistant is built using modern technologies:
              </p>
              <ul>
                <li><strong>Frontend:</strong> React.js, Redux, Chart.js</li>
                <li><strong>Middleware:</strong> Google Gemini API, Python, FastAPI</li>
                <li><strong>Backend:</strong> Python, FastAPI, PostgreSQL</li>
                <li><strong>Data Processing:</strong> Pandas, NumPy</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
