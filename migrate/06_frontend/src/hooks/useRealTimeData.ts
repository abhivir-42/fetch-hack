import { useState, useEffect, useCallback } from 'react';
import { marketApi } from '../api/market';
import { agentsApi } from '../api/agents';
import { MarketData, HeartbeatData } from '../types/api';
import { Agent } from '../types/agents';

export type DataType = 'market' | 'agents' | 'heartbeat';

interface UseRealTimeDataProps {
  dataType: DataType;
  pollingInterval?: number;
  enabled?: boolean;
}

interface UseRealTimeDataReturn<T> {
  data: T | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

/**
 * Hook for real-time data fetching with polling
 * @param dataType Type of data to fetch ('market', 'agents', or 'heartbeat')
 * @param pollingInterval Interval in ms between polls (default: 60000ms or 60s)
 * @param enabled Whether polling is enabled (default: false to reduce API calls)
 */
export function useRealTimeData<T>({
  dataType,
  pollingInterval = 60000,
  enabled = false,
}: UseRealTimeDataProps): UseRealTimeDataReturn<T> {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Function to fetch data based on data type
  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      let result;
      
      switch (dataType) {
        case 'market':
          console.log('Fetching market data...');
          result = await marketApi.getMarketData();
          console.log('Received market data:', result);
          break;
        case 'agents':
          console.log('Fetching agent data...');
          result = await agentsApi.getAgents();
          console.log('Received agent data:', result);
          break;
        case 'heartbeat':
          console.log('Fetching heartbeat data...');
          result = await agentsApi.getHeartbeat();
          console.log('Received heartbeat data:', result);
          break;
        default:
          throw new Error(`Unsupported data type: ${dataType}`);
      }
      
      setData(result as T);
    } catch (err) {
      console.error(`Error fetching ${dataType} data:`, err);
      setError(`Failed to fetch ${dataType} data. Please try again.`);
    } finally {
      setIsLoading(false);
    }
  }, [dataType]);

  // Manual refetch function
  const refetch = useCallback(async () => {
    return fetchData();
  }, [fetchData]);

  // Set up polling only if enabled
  useEffect(() => {
    if (!enabled) return;
    
    // Initial fetch
    fetchData();
    
    // Set up polling interval
    const intervalId = setInterval(() => {
      fetchData();
    }, pollingInterval);
    
    // Clean up on unmount
    return () => {
      clearInterval(intervalId);
    };
  }, [fetchData, pollingInterval, enabled]);

  return { data, isLoading, error, refetch };
}

/**
 * Specialized hook for real-time market data
 */
export function useRealTimeMarketData(
  pollingInterval = 60000,
  enabled = false
): UseRealTimeDataReturn<MarketData[]> {
  return useRealTimeData<MarketData[]>({
    dataType: 'market',
    pollingInterval,
    enabled,
  });
}

/**
 * Specialized hook for real-time agent statuses
 */
export function useRealTimeAgentStatuses(
  pollingInterval = 60000,
  enabled = false
): UseRealTimeDataReturn<Agent[]> {
  return useRealTimeData<Agent[]>({
    dataType: 'agents',
    pollingInterval,
    enabled,
  });
}

/**
 * Specialized hook for real-time heartbeat data
 */
export function useRealTimeHeartbeat(
  pollingInterval = 60000,
  enabled = false
): UseRealTimeDataReturn<HeartbeatData> {
  return useRealTimeData<HeartbeatData>({
    dataType: 'heartbeat',
    pollingInterval,
    enabled,
  });
} 