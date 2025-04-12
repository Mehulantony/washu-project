import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { selectQuery } from '../redux/slices/historySlice';
import { setQueryText, processQuery } from '../redux/slices/querySlice';
import { useNavigate } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner';

const QueryHistory = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { queries, selectedQueryId } = useSelector(state => state.history);
  const { loading } = useSelector(state => state.query);

  const handleQuerySelect = (queryId, queryText) => {
    dispatch(selectQuery(queryId));
    dispatch(setQueryText(queryText));
    dispatch(processQuery(queryText));
    navigate('/'); // Navigate to dashboard to see results
  };

  const formatDate = (dateString) => {
    const options = { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };

  if (loading) {
    return (
      <div className="text-center my-5">
        <LoadingSpinner />
        <p>Loading query history...</p>
      </div>
    );
  }

  return (
    <div className="query-history-container">
      <div className="row mb-4">
        <div className="col-12">
          <h1>Query History</h1>
          <p className="lead">
            View and rerun your previous budget queries
          </p>
        </div>
      </div>

      {queries.length === 0 ? (
        <div className="alert alert-info">
          You haven't made any queries yet. Go to the Dashboard to ask questions about government budget data.
        </div>
      ) : (
        <div className="card">
          <div className="card-header">
            <h5>Your Previous Queries</h5>
          </div>
          <div className="list-group list-group-flush">
            {queries.map((query) => (
              <div 
                key={query.id}
                className={`list-group-item list-group-item-action ${selectedQueryId === query.id ? 'active' : ''}`}
                onClick={() => handleQuerySelect(query.id, query.text)}
              >
                <div className="d-flex w-100 justify-content-between">
                  <h5 className="mb-1">{query.text}</h5>
                  <small>{formatDate(query.timestamp)}</small>
                </div>
                <p className="mb-1">
                  {query.results?.insights?.substring(0, 100)}
                  {query.results?.insights?.length > 100 ? '...' : ''}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default QueryHistory;
