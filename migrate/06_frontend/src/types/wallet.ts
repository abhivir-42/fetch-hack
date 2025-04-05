export interface WalletInfo {
  address: string;
  network: string;
  isConnected: boolean;
  balance: string;
}

export interface WalletConnectionOptions {
  privateKey?: string;
  network: NetworkType;
}

export type NetworkType = 'ethereum' | 'base' | 'polygon' | 'bitcoin';

export interface TopupRequest {
  amount: number;
  network: NetworkType;
  address: string;
}

export interface TopupResponse {
  success: boolean;
  txHash?: string;
  error?: string;
  transaction?: {
    id: string;
    amount: number;
    timestamp: string;
  };
}

export interface NetworkOption {
  id: NetworkType;
  name: string;
  icon: string;
  isTestnet: boolean;
}

export interface InvestmentParameters {
  amount: number;
  network: NetworkType;
  investorType: InvestorType;
  riskStrategy: RiskStrategy;
}

export type InvestorType = 'long-term' | 'short-term' | 'speculative';
export type RiskStrategy = 'conservative' | 'balanced' | 'aggressive' | 'speculative'; 