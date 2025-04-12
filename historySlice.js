import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  queries: [],
  selectedQueryId: null
};

const historySlice = createSlice({
  name: 'history',
  initialState,
  reducers: {
    addQueryToHistory: (state, action) => {
      const newQuery = {
        id: Date.now().toString(),
        text: action.payload.queryText,
        timestamp: new Date().toISOString(),
        results: action.payload.results
      };
      state.queries.unshift(newQuery); // Add to beginning of array
    },
    selectQuery: (state, action) => {
      state.selectedQueryId = action.payload;
    },
    clearHistory: (state) => {
      state.queries = [];
      state.selectedQueryId = null;
    }
  }
});

export const { addQueryToHistory, selectQuery, clearHistory } = historySlice.actions;
export default historySlice.reducer;
