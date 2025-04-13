import axios from 'axios';

// Base URL for the Gemini API Client
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add request interceptor for authentication
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Submit natural language query to the Gemini API Client
export const submitQuery = async (queryText) => {
  return await apiClient.post('/query', { query: queryText });
};

// Get query history for the current user
export const getQueryHistory = async () => {
  return await apiClient.get('/history');
};

// Get detailed results for a specific query
export const getQueryDetails = async (queryId) => {
  return await apiClient.get(`/query/${queryId}`);
};

// User authentication services
export const loginUser = async (credentials) => {
  return await apiClient.post('/auth/login', credentials);
};

export const registerUser = async (userData) => {
  return await apiClient.post('/auth/register', userData);
};

export const logoutUser = async () => {
  localStorage.removeItem('authToken');
  return await apiClient.post('/auth/logout');
};

export default apiClient;
