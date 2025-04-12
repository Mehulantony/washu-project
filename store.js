import { configureStore } from '@reduxjs/toolkit';
import queryReducer from './slices/querySlice';
import historyReducer from './slices/historySlice';
import authReducer from './slices/authSlice';

const store = configureStore({
  reducer: {
    query: queryReducer,
    history: historyReducer,
    auth: authReducer
  }
});

export default store;
