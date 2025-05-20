import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictDemand = async (data) => {
  try {
    const response = await api.post('/predict', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to predict demand');
  }
};

export const getInventoryRecommendations = async () => {
  try {
    const response = await api.get('/recommend');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to get recommendations');
  }
};

export const trainModel = async () => {
  try {
    const response = await api.post('/train');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to train model');
  }
};

export default api; 