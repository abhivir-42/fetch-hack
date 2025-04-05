import apiClient from './apiClient';
import { WalletBalance } from '../types/api';
import { TopupRequest, WalletConnectionOptions, WalletInfo } from '../types/wallet';

// Use mock wallet service for now due to backend connectivity issues
export const walletApi = {
  connectWallet: async (options: WalletConnectionOptions): Promise<WalletInfo> => {
    try {
      const response = await apiClient.post<WalletInfo>('/wallet/connect', options);
      return response;
    } catch (error) {
      console.error('Error connecting wallet:', error);
      throw error;
    }
  },
  
  getBalance: async (address: string, network: string): Promise<WalletBalance> => {
    try {
      const response = await apiClient.get<WalletBalance>(`/wallet/balance?address=${address}&network=${network}`);
      return response;
    } catch (error) {
      console.error('Error fetching wallet balance:', error);
      throw error;
    }
  },
  
  requestTopup: async (request: TopupRequest): Promise<{ success: boolean, txHash?: string }> => {
    try {
      const response = await apiClient.post<{ success: boolean, txHash?: string }>('/wallet/topup', request);
      return response;
    } catch (error) {
      console.error('Error requesting topup:', error);
      throw error;
    }
  },
  
  disconnectWallet: async (): Promise<void> => {
    try {
      await apiClient.post<void>('/wallet/disconnect');
    } catch (error) {
      console.error('Error disconnecting wallet:', error);
      throw error;
    }
  }
}; 