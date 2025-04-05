export interface AuthResponse {
  token: string;
  user: {
    id: string;
    email: string;
  };
}

export interface WalletBalance {
  address: string;
  balance: string;
  network: string;
}

export interface MarketData {
  symbol: string;
  name: string;
  currentPrice: number;
  priceChange24h: number;
  priceChangePercentage24h: number;
  marketCap: number;
  volume: number;
  lastUpdated: string;
}

export interface Transaction {
  id: string;
  type: 'buy' | 'sell' | 'topup';
  status: 'pending' | 'completed' | 'failed';
  amount: number;
  timestamp: string;
  details: {
    network: string;
    token?: string;
    txHash?: string;
  };
}

export interface AgentStatus {
  id: string;
  name: string;
  status: 'online' | 'offline' | 'error';
  lastActive: string;
  type: string;
}

export interface HeartbeatData {
  timestamp: string;
  status: 'healthy' | 'warning' | 'error';
  response: {
    tradingEnabled: boolean;
    message: string;
  };
}

export interface APIError {
  status: number;
  message: string;
  details?: string;
} 