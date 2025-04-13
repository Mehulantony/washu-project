import React from 'react';
import { Bar, Line, Pie, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const ResultsDisplay = ({ results, visualizationType }) => {
  if (!results) return null;

  const { data, insights, query_parameters } = results;

  // Format data for visualization
  const formatChartData = () => {
    if (!data || !data.length) return null;

    // Extract labels and values based on data structure
    const labels = data.map(item => item.label || item.category || item.department || item.year || item.name);
    const values = data.map(item => item.value || item.amount || item.budget || item.spending);
    
    // Set colors for charts
    const backgroundColors = [
      'rgba(54, 162, 235, 0.6)',
      'rgba(255, 99, 132, 0.6)',
      'rgba(255, 206, 86, 0.6)',
      'rgba(75, 192, 192, 0.6)',
      'rgba(153, 102, 255, 0.6)',
      'rgba(255, 159, 64, 0.6)',
      'rgba(199, 199, 199, 0.6)',
      'rgba(83, 102, 255, 0.6)',
      'rgba(40, 159, 64, 0.6)',
      'rgba(210, 199, 199, 0.6)',
    ];

    const chartData = {
      labels,
      datasets: [
        {
          label: query_parameters?.metric || 'Budget Amount',
          data: values,
          backgroundColor: backgroundColors,
          borderColor: backgroundColors.map(color => color.replace('0.6', '1')),
          borderWidth: 1,
        },
      ],
    };

    return chartData;
  };

  const chartData = formatChartData();

  const renderVisualization = () => {
    if (!chartData) return <p>No data available for visualization</p>;

    const options = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: query_parameters?.title || 'Budget Data Visualization',
        },
      },
    };

    switch (visualizationType) {
      case 'bar':
        return <Bar data={chartData} options={options} height={300} />;
      case 'line':
        return <Line data={chartData} options={options} height={300} />;
      case 'pie':
        return <Pie data={chartData} options={options} height={300} />;
      case 'doughnut':
        return <Doughnut data={chartData} options={options} height={300} />;
      default:
        return <Bar data={chartData} options={options} height={300} />;
    }
  };

  return (
    <div className="results-display">
      <div className="row">
        <div className="col-md-8">
          <div className="visualization-container">
            {renderVisualization()}
          </div>
        </div>
        <div className="col-md-4">
          <div className="insights-container">
            <h5>Insights</h5>
            <div className="card">
              <div className="card-body">
                {insights ? (
                  <div dangerouslySetInnerHTML={{ __html: insights }} />
                ) : (
                  <p>No insights available for this query.</p>
                )}
              </div>
            </div>
            
            <h5 className="mt-4">Query Parameters</h5>
            <div className="card">
              <div className="card-body">
                <ul className="list-group list-group-flush">
                  {query_parameters && Object.entries(query_parameters).map(([key, value]) => (
                    <li key={key} className="list-group-item">
                      <strong>{key}:</strong> {value}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {data && data.length > 0 && (
        <div className="row mt-4">
          <div className="col-12">
            <h5>Data Table</h5>
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead>
                  <tr>
                    {Object.keys(data[0]).map(key => (
                      <th key={key}>{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.map((item, index) => (
                    <tr key={index}>
                      {Object.values(item).map((value, i) => (
                        <td key={i}>{value}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;
