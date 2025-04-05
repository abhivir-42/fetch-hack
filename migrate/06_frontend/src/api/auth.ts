import apiClient from './apiClient';
import { AuthResponse } from '../types/api';

interface LoginCredentials {
  email: string;
  password: string;
}

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    try {
      const response = await apiClient.post<AuthResponse>('/auth/login', credentials);
      
      // Store the token in localStorage
      if (response && response.token) {
        localStorage.setItem('auth_token', response.token);
      }
      
      return response;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },
  
  logout: async (): Promise<void> => {
    try {
      // Our API server doesn't have a logout endpoint yet, 
      // so we'll just clear the local token
      localStorage.removeItem('auth_token');
      
      // When implemented:
      // await apiClient.post<void>('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  },
  
  checkAuthStatus: async (): Promise<AuthResponse> => {
    // For now, we'll just check if a token exists locally
    // Our API server doesn't have a status endpoint yet
    return new Promise((resolve, reject) => {
      const token = localStorage.getItem('auth_token');
      
      if (token) {
        resolve({
          token,
          user: {
            id: '1',
            email: 'user@example.com',
          },
        });
      } else {
        reject({
          status: 401,
          message: 'Not authenticated',
        });
      }
    });
    
    // When implemented:
    // return apiClient.get<AuthResponse>('/auth/status');
  },
}; 