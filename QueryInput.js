import React from 'react';

const QueryInput = ({ queryText, handleQueryChange, handleQuerySubmit, handleClear, loading }) => {
  return (
    <div className="query-input-container">
      <form onSubmit={handleQuerySubmit}>
        <div className="input-group mb-3">
          <input
            type="text"
            className="form-control query-input"
            placeholder="Ask a question about U.S. government budget data..."
            value={queryText}
            onChange={handleQueryChange}
            disabled={loading}
          />
          <button
            className="btn btn-primary query-button"
            type="submit"
            disabled={!queryText.trim() || loading}
          >
            Submit
          </button>
          <button
            className="btn btn-outline-secondary"
            type="button"
            onClick={handleClear}
            disabled={loading}
          >
            Clear
          </button>
        </div>
      </form>
    </div>
  );
};

export default QueryInput;
