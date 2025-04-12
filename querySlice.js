import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { submitQuery } from '../../services/apiService';

export const processQuery = createAsyncThunk(
  'query/processQuery',
  async (queryText, { rejectWithValue }) => {
    try {
      const response = await submitQuery(queryText);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  queryText: '',
  results: null,
  loading: false,
  error: null,
  visualizationType: 'bar' // default visualization type
};

const querySlice = createSlice({
  name: 'query',
  initialState,
  reducers: {
    setQueryText: (state, action) => {
      state.queryText = action.payload;
    },
    clearResults: (state) => {
      state.results = null;
      state.error = null;
    },
    setVisualizationType: (state, action) => {
      state.visualizationType = action.payload;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(processQuery.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(processQuery.fulfilled, (state, action) => {
        state.loading = false;
        state.results = action.payload;
      })
      .addCase(processQuery.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'An error occurred while processing your query';
      });
  }
});

export const { setQueryText, clearResults, setVisualizationType } = querySlice.actions;
export default querySlice.reducer;
