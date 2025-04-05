import React, { useState, useEffect } from 'react';
import { marketApi } from '../../api/market';
import Card from '../common/Card';
import { ArrowTrendingUpIcon, ArrowTrendingDownIcon } from '@heroicons/react/24/outline';

interface PriceData {
  timestamp: number;
  price: number;
}

interface CryptoPriceChartProps {
  symbol: string;
  name: string;
  currentPrice: number;
  priceChangePercent: number;
}

type TimeFrame = '24h' | '7d' | '30d';

const CryptoPriceChart: React.FC<CryptoPriceChartProps> = ({
  symbol,
  name,
  currentPrice,
  priceChangePercent,
}) => {
  const [timeframe, setTimeframe] = useState<TimeFrame>('24h');
  const [priceData, setPriceData] = useState<PriceData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch price history when symbol or timeframe changes
  useEffect(() => {
    const fetchPriceHistory = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const data = await marketApi.getPriceHistory(symbol, timeframe);
        setPriceData(data);
      } catch (err) {
        console.error(`Failed to fetch price history for ${symbol}:`, err);
        setError('Failed to load price history data');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchPriceHistory();
  }, [symbol, timeframe]);

  // Get min and max values for scaling the chart
  const minPrice = Math.min(...priceData.map(d => d.price));
  const maxPrice = Math.max(...priceData.map(d => d.price));
  const priceRange = maxPrice - minPrice;
  
  // Format price with commas and dollar sign
  const formatPrice = (price: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  // Format percentage change with + or - sign
  const formatPercentage = (value: number): string => {
    const prefix = value >= 0 ? '+' : '';
    return `${prefix}${value.toFixed(2)}%`;
  };

  // Format date based on timeframe
  const formatDate = (timestamp: number): string => {
    const date = new Date(timestamp);
    
    switch(timeframe) {
      case '24h':
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      case '7d':
        return date.toLocaleDateString([], { weekday: 'short' });
      case '30d':
        return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
      default:
        return date.toLocaleDateString();
    }
  };

  return (
    <Card title={`${name} Price Chart`} className="mb-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {formatPrice(currentPrice)}
          </div>
          <div className={`flex items-center ${priceChangePercent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {priceChangePercent >= 0 ? (
              <ArrowTrendingUpIcon className="w-4 h-4 mr-1" />
            ) : (
              <ArrowTrendingDownIcon className="w-4 h-4 mr-1" />
            )}
            <span>{formatPercentage(priceChangePercent)}</span>
          </div>
        </div>
        
        <div className="flex space-x-2">
          <button
            className={`px-2 py-1 text-xs rounded-md ${timeframe === '24h' 
              ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200' 
              : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'}`}
            onClick={() => setTimeframe('24h')}
          >
            24H
          </button>
          <button
            className={`px-2 py-1 text-xs rounded-md ${timeframe === '7d' 
              ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200' 
              : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'}`}
            onClick={() => setTimeframe('7d')}
          >
            7D
          </button>
          <button
            className={`px-2 py-1 text-xs rounded-md ${timeframe === '30d' 
              ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200' 
              : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'}`}
            onClick={() => setTimeframe('30d')}
          >
            30D
          </button>
        </div>
      </div>
      
      {isLoading ? (
        <div className="h-64 flex items-center justify-center text-gray-500 dark:text-gray-400">
          Loading price data...
        </div>
      ) : error ? (
        <div className="h-64 flex items-center justify-center text-red-500 dark:text-red-400">
          {error}
        </div>
      ) : priceData.length === 0 ? (
        <div className="h-64 flex items-center justify-center text-gray-500 dark:text-gray-400">
          No price data available
        </div>
      ) : (
        <div className="relative h-64">
          {/* Chart grid */}
          <div className="absolute inset-0 grid grid-cols-1 grid-rows-4 gap-0">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="w-full border-b border-gray-200 dark:border-gray-700"></div>
            ))}
          </div>
          
          {/* Chart line */}
          <svg className="absolute inset-0 w-full h-full" preserveAspectRatio="none">
            <defs>
              <linearGradient id={`gradient-${symbol}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor={priceChangePercent >= 0 ? '#10B981' : '#EF4444'} stopOpacity="0.2" />
                <stop offset="100%" stopColor={priceChangePercent >= 0 ? '#10B981' : '#EF4444'} stopOpacity="0" />
              </linearGradient>
            </defs>
            
            {/* Price line */}
            {priceData.length > 1 && (
              <>
                <path
                  d={`
                    M ${priceData.map((d, i) => 
                      `${(i / (priceData.length - 1)) * 100}% ${100 - ((d.price - minPrice) / priceRange) * 100}%`
                    ).join(' L ')}
                  `}
                  fill="none"
                  stroke={priceChangePercent >= 0 ? '#10B981' : '#EF4444'}
                  strokeWidth="2"
                />
                
                {/* Area under the line */}
                <path
                  d={`
                    M ${priceData[0] ? (0) + '% ' + (100 - ((priceData[0].price - minPrice) / priceRange) * 100) + '%' : ''}
                    L ${priceData.map((d, i) => 
                      `${(i / (priceData.length - 1)) * 100}% ${100 - ((d.price - minPrice) / priceRange) * 100}%`
                    ).join(' L ')}
                    L ${priceData[priceData.length - 1] ? (100) + '% ' + (100) + '%' : ''}
                    L ${priceData[0] ? (0) + '% ' + (100) + '%' : ''}
                  `}
                  fill={`url(#gradient-${symbol})`}
                />
              </>
            )}
          </svg>
          
          {/* X-axis labels */}
          <div className="absolute bottom-0 left-0 right-0 flex justify-between text-xs text-gray-500 dark:text-gray-400 px-2">
            {priceData.length > 0 && [
              formatDate(priceData[0].timestamp),
              formatDate(priceData[Math.floor(priceData.length / 2)].timestamp),
              formatDate(priceData[priceData.length - 1].timestamp),
            ].map((label, i) => (
              <div key={i}>{label}</div>
            ))}
          </div>
          
          {/* Y-axis labels */}
          <div className="absolute top-0 bottom-0 right-0 flex flex-col justify-between text-xs text-gray-500 dark:text-gray-400 py-2">
            <div>{formatPrice(maxPrice)}</div>
            <div>{formatPrice(minPrice)}</div>
          </div>
        </div>
      )}
    </Card>
  );
};

export default CryptoPriceChart; 