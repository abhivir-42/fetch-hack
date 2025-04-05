import axios from 'axios';

// Create a base API client with default configuration
export const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
});

// Add response interceptor to handle errors consistently
apiClient.interceptors.response.use(
  (response) => {
    // Return just the data for successful responses
    return response.data;
  },
  (error) => {
    // Handle error responses
    if (error.response) {
      // Server responded with a status code outside 2xx range
      console.error('API Error:', error.response.data);
      return Promise.reject({
        status: error.response.status,
        message: error.response.data.message || 'An error occurred',
        details: error.response.data.details,
      });
    } else if (error.request) {
      // Request was made but no response received
      console.error('API Request Error:', error.request);
      return Promise.reject({
        status: 0,
        message: 'No response from server. Please check your connection.',
      });
    } else {
      // Error in setting up the request
      console.error('API Setup Error:', error.message);
      return Promise.reject({
        status: 0,
        message: error.message,
      });
    }
  }
); 