import apiClient from './apiClient';

export interface Transaction {
  id: string;
  type: string;
  from: string;
  to: string;
  amount: number;
  timestamp: string;
  status: string;
  txHash?: string;
  error?: string;
}

export const transactionsApi = {
  getTransactions: async (): Promise<Transaction[]> => {
    try {
      const response = await apiClient.get<any>('/transactions');
      console.log('Transactions raw response:', response);
      
      // Handle different possible response formats
      if (Array.isArray(response)) {
        return response;
      } else if (response && typeof response === 'object') {
        // Check if response has 'transactions' property
        if ('transactions' in response && Array.isArray(response.transactions)) {
          return response.transactions;
        }
        
        // Try to extract first array property from the response
        for (const key in response) {
          if (Array.isArray(response[key])) {
            return response[key];
          }
        }
      }
      
      return [];
    } catch (error) {
      console.error('Error fetching transactions:', error);
      return [];
    }
  },
  
  getTransactionById: async (id: string): Promise<Transaction | null> => {
    try {
      const response = await apiClient.get<any>(`/transactions/${id}`);
      console.log(`Transaction ${id} raw response:`, response);
      
      if (response && typeof response === 'object') {
        if ('id' in response) {
          return response as Transaction;
        }
        
        // Try to extract first object property that might be a transaction
        for (const key in response) {
          if (response[key] && typeof response[key] === 'object' && 'id' in response[key]) {
            return response[key] as Transaction;
          }
        }
      }
      
      return null;
    } catch (error) {
      console.error(`Error fetching transaction ${id}:`, error);
      return null;
    }
  }
}; 