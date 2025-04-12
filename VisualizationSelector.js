import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setVisualizationType } from '../redux/slices/querySlice';

const VisualizationSelector = () => {
  const dispatch = useDispatch();
  const { visualizationType } = useSelector(state => state.query);

  const handleChange = (e) => {
    dispatch(setVisualizationType(e.target.value));
  };

  return (
    <div className="visualization-selector">
      <select 
        className="form-select" 
        value={visualizationType} 
        onChange={handleChange}
        aria-label="Visualization type"
      >
        <option value="bar">Bar Chart</option>
        <option value="line">Line Chart</option>
        <option value="pie">Pie Chart</option>
        <option value="doughnut">Doughnut Chart</option>
      </select>
    </div>
  );
};

export default VisualizationSelector;
