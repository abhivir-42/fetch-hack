import React, { createContext, useContext, useState, ReactNode } from 'react';
import { walletApi } from '../api/wallet';
import { WalletInfo, WalletConnectionOptions, NetworkType } from '../types/wallet';
import { WalletBalance } from '../types/api';

interface WalletContextType {
  walletInfo: WalletInfo | null;
  balance: WalletBalance | null;
  isConnecting: boolean;
  error: string | null;
  connectWallet: (options: WalletConnectionOptions) => Promise<void>;
  disconnectWallet: () => Promise<void>;
  requestTopup: (amount: number, network: NetworkType) => Promise<{ success: boolean, txHash?: string }>;
}

const WalletContext = createContext<WalletContextType | undefined>(undefined);

interface WalletProviderProps {
  children: ReactNode;
}

export const WalletProvider: React.FC<WalletProviderProps> = ({ children }) => {
  const [walletInfo, setWalletInfo] = useState<WalletInfo | null>(null);
  const [balance, setBalance] = useState<WalletBalance | null>(null);
  const [isConnecting, setIsConnecting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  const connectWallet = async (options: WalletConnectionOptions): Promise<void> => {
    setIsConnecting(true);
    setError(null);
    
    try {
      const info = await walletApi.connectWallet(options);
      setWalletInfo(info);
      
      // Get wallet balance
      if (info.address) {
        const balanceInfo = await walletApi.getBalance(info.address, info.network);
        setBalance(balanceInfo);
      }
      
      // No return value needed for void Promise
    } catch (err: any) {
      setError(err.message || 'Failed to connect wallet');
      throw err;
    } finally {
      setIsConnecting(false);
    }
  };
  
  const disconnectWallet = async (): Promise<void> => {
    try {
      await walletApi.disconnectWallet();
      setWalletInfo(null);
      setBalance(null);
    } catch (err: any) {
      setError(err.message || 'Failed to disconnect wallet');
      throw err;
    }
  };
  
  const requestTopup = async (amount: number, network: NetworkType) => {
    try {
      return await walletApi.requestTopup({ amount, network });
    } catch (err: any) {
      setError(err.message || 'Failed to request topup');
      throw err;
    }
  };
  
  return (
    <WalletContext.Provider
      value={{
        walletInfo,
        balance,
        isConnecting,
        error,
        connectWallet,
        disconnectWallet,
        requestTopup
      }}
    >
      {children}
    </WalletContext.Provider>
  );
};

// Custom hook for using the wallet context
export const useWallet = (): WalletContextType => {
  const context = useContext(WalletContext);
  
  if (context === undefined) {
    throw new Error('useWallet must be used within a WalletProvider');
  }
  
  return context;
}; 