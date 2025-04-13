import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { setQueryText, processQuery, clearResults } from '../redux/slices/querySlice';
import { addQueryToHistory } from '../redux/slices/historySlice';
import QueryInput from '../components/QueryInput';
import ResultsDisplay from '../components/ResultsDisplay';
import VisualizationSelector from '../components/VisualizationSelector';
import LoadingSpinner from '../components/LoadingSpinner';

const Dashboard = () => {
  const dispatch = useDispatch();
  const { queryText, results, loading, error, visualizationType } = useSelector(state => state.query);
  const [showExamples, setShowExamples] = useState(true);

  const handleQuerySubmit = (e) => {
    e.preventDefault();
    if (!queryText.trim()) return;
    
    dispatch(processQuery(queryText))
      .unwrap()
      .then(result => {
        dispatch(addQueryToHistory({ queryText, results: result }));
        setShowExamples(false);
      });
  };

  const handleQueryChange = (e) => {
    dispatch(setQueryText(e.target.value));
  };

  const handleClear = () => {
    dispatch(clearResults());
    dispatch(setQueryText(''));
    setShowExamples(true);
  };

  const exampleQueries = [
    "What was the Department of Defense budget for fiscal year 2023?",
    "Compare education spending between 2020 and 2022",
    "Show me the top 5 departments by budget allocation in 2023",
    "What percentage of the federal budget went to healthcare in 2022?",
    "How has infrastructure spending changed over the last 5 years?"
  ];

  const handleExampleClick = (query) => {
    dispatch(setQueryText(query));
  };

  return (
    <div className="dashboard-container">
      <div className="row mb-4">
        <div className="col-12">
          <h1>Government Financial Budget Assistant</h1>
          <p className="lead">
            Ask questions about U.S. government budget data using natural language
          </p>
        </div>
      </div>

      <div className="row">
        <div className="col-12">
          <QueryInput 
            queryText={queryText}
            handleQueryChange={handleQueryChange}
            handleQuerySubmit={handleQuerySubmit}
            handleClear={handleClear}
            loading={loading}
          />
        </div>
      </div>

      {showExamples && !results && !loading && (
        <div className="row mt-4">
          <div className="col-12">
            <div className="card">
              <div className="card-header">
                <h5>Example Queries</h5>
              </div>
              <div className="card-body">
                <ul className="list-group">
                  {exampleQueries.map((query, index) => (
                    <li 
                      key={index} 
                      className="list-group-item list-group-item-action"
                      onClick={() => handleExampleClick(query)}
                      style={{ cursor: 'pointer' }}
                    >
                      {query}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {loading && (
        <div className="row mt-4">
          <div className="col-12 text-center">
            <LoadingSpinner />
            <p>Processing your query...</p>
          </div>
        </div>
      )}

      {error && (
        <div className="row mt-4">
          <div className="col-12">
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          </div>
        </div>
      )}

      {results && (
        <div className="row mt-4">
          <div className="col-12">
            <div className="card results-container">
              <div className="card-header d-flex justify-content-between align-items-center">
                <h5>Results</h5>
                <VisualizationSelector />
              </div>
              <div className="card-body">
                <ResultsDisplay 
                  results={results} 
                  visualizationType={visualizationType} 
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
