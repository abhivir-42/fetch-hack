import axios from 'axios';
import { 
  AgentStatus, 
  ApiResponse, 
  CoinData, 
  CryptoNews, 
  SentimentAnalysis,
  Transaction,
  UserInputs
} from './types';

const API_URL = 'http://localhost:8600/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getAgentStatus = async (): Promise<AgentStatus> => {
  const response = await api.get<AgentStatus>('/status');
  return response.data;
};

export const getMarketData = async (): Promise<CoinData> => {
  const response = await api.get<CoinData>('/market-data');
  return response.data;
};

export const getSentimentAnalysis = async (): Promise<SentimentAnalysis> => {
  const response = await api.get<SentimentAnalysis>('/sentiment-analysis');
  return response.data;
};

export const getNews = async (): Promise<CryptoNews> => {
  const response = await api.get<CryptoNews>('/news');
  return response.data;
};

export const getTransactions = async (): Promise<Transaction[]> => {
  const response = await api.get<Transaction[]>('/transactions');
  return response.data;
};

export const executeTrade = async (
  action: string,
  amount: number
): Promise<ApiResponse<Transaction>> => {
  const response = await api.post<ApiResponse<Transaction>>('/execute-trade', {
    action,
    amount,
  });
  return response.data;
};

export const startAgent = async (
  agent: string
): Promise<ApiResponse<null>> => {
  const response = await api.post<ApiResponse<null>>('/start-agent', {
    agent,
  });
  return response.data;
};

export const startAllAgents = async (): Promise<ApiResponse<null>> => {
  const response = await api.post<ApiResponse<null>>('/start-all');
  return response.data;
};

export const submitUserInputs = async (
  inputs: UserInputs
): Promise<ApiResponse<Transaction>> => {
  // This is a new endpoint that we'll need to add to the backend
  const response = await api.post<ApiResponse<Transaction>>('/submit-inputs', inputs);
  return response.data;
};

export default api; 