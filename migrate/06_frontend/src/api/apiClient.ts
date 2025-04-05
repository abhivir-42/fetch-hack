import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { APIError } from '../types/api';

// Base API URL - would be environment-specific in production
const API_BASE_URL = 'http://localhost:8000/api';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => {
        console.log(`API Response for ${response.config.url}:`, response.data);
        return response.data;
      },
      (error: AxiosError) => {
        const apiError: APIError = {
          status: error.response?.status || 500,
          message: 'An unexpected error occurred',
          details: error.message,
        };

        // Try to extract error message from response if available
        if (error.response?.data) {
          const data = error.response.data as any;
          if (data.message) {
            apiError.message = data.message;
          }
          if (data.details) {
            apiError.details = data.details;
          }
        }

        // Handle token expiration/authentication errors
        if (apiError.status === 401) {
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }

        return Promise.reject(apiError);
      }
    );
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T, T>(url, config);
    return response;
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T, T>(url, data, config);
    return response;
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T, T>(url, data, config);
    return response;
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T, T>(url, config);
    return response;
  }
}

// Create a singleton instance
const apiClient = new ApiClient();
export default apiClient; 