// Agent Status Types
export interface AgentStatus {
  [key: string]: boolean;
}

// User Input Types
export interface UserInputs {
  topupWallet: string;
  topupAmount: number;
  privateKey: string;
  network: string;
  investorType: string;
  riskStrategy: string;
  reason: string;
}

// Market Data Types
export interface CoinData {
  name: string;
  symbol: string;
  current_price: number;
  market_cap: number;
  total_volume: number;
  price_change_24h: number;
}

export interface FearGreedData {
  value: number;
  value_classification: string;
  timestamp: string;
}

export interface SentimentAnalysis {
  data: FearGreedData[];
  status: string;
  timestamp: string;
}

export interface CryptoNews {
  articles: Article[];
}

export interface Article {
  source: {
    id: string | null;
    name: string;
  };
  author: string;
  title: string;
  description: string;
  url: string;
  urlToImage: string;
  publishedAt: string;
  content: string;
}

export interface Transaction {
  tx_hash?: string;
  status: string;
  message?: string;
  details?: string;
  action?: string;
  amount?: string | number;
  price?: number;
  timestamp: number;
}

// API Response Types
export interface ApiResponse<T> {
  status: 'success' | 'error' | 'pending';
  message?: string;
  data?: T;
}

export interface TradeDecision {
  action: 'BUY' | 'SELL' | 'HOLD';
  reasoning: string;
} 