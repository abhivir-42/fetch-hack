import { MarketData } from '../types/api';

// Mock market data to avoid API rate limiting
const mockMarketData: MarketData[] = [
  {
    symbol: 'BTC',
    name: 'Bitcoin',
    currentPrice: 67800.45,
    priceChange24h: 1245.67,
    priceChangePercentage24h: 1.92,
    marketCap: 1345678900000,
    volume: 25678900000,
    lastUpdated: new Date().toISOString()
  },
  {
    symbol: 'ETH',
    name: 'Ethereum',
    currentPrice: 3482.12,
    priceChange24h: 67.89,
    priceChangePercentage24h: 2.01,
    marketCap: 419876543200,
    volume: 13456789000,
    lastUpdated: new Date().toISOString()
  },
  {
    symbol: 'SOL',
    name: 'Solana',
    currentPrice: 142.78,
    priceChange24h: -4.32,
    priceChangePercentage24h: -2.85,
    marketCap: 62345678900,
    volume: 3456789000,
    lastUpdated: new Date().toISOString()
  },
  {
    symbol: 'AVAX',
    name: 'Avalanche',
    currentPrice: 35.92,
    priceChange24h: 0.87,
    priceChangePercentage24h: 2.48,
    marketCap: 12876543210,
    volume: 765432100,
    lastUpdated: new Date().toISOString()
  }
];

export const marketApi = {
  /**
   * Get market data for all supported cryptocurrencies
   */
  getMarketData: async (): Promise<MarketData[]> => {
    try {
      console.log('Using mock market data to avoid API rate limits');
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      return mockMarketData;
    } catch (error) {
      console.error('Error fetching market data:', error);
      throw new Error('Failed to fetch market data. Please try again.');
    }
  },
  
  /**
   * Get price history for a specific cryptocurrency
   */
  getPriceHistory: async (symbol: string, timeframe: string): Promise<{ timestamp: number; price: number }[]> => {
    try {
      console.log(`Using mock price history data for ${symbol}`);
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Generate mock price history data
      const now = Date.now();
      const points = 24; // Number of data points
      const interval = timeframe === '24h' ? 3600000 : // 1 hour intervals for 24h
                       timeframe === '7d' ? 86400000 : // 1 day intervals for 7d
                       86400000 * 3; // 3 day intervals for 30d
      
      // Get the current price for this symbol
      const currentPrice = mockMarketData.find(data => data.symbol === symbol)?.currentPrice || 50000;
      
      // Generate random price data
      return Array.from({ length: points }).map((_, i) => {
        const timestamp = now - (points - i) * interval;
        const randomChange = (Math.random() - 0.5) * 0.05; // -2.5% to +2.5%
        const price = currentPrice * (1 + randomChange * (points - i) / points);
        return { timestamp, price };
      });
    } catch (error) {
      console.error(`Error fetching price history for ${symbol}:`, error);
      throw new Error(`Failed to fetch price history for ${symbol}. Please try again.`);
    }
  }
}; 