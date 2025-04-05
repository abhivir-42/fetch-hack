import React, { useEffect } from 'react';
import { MarketData } from '../../types/api';

interface MarketOverviewProps {
  marketData: MarketData[];
  isLoading: boolean;
}

const MarketOverview: React.FC<MarketOverviewProps> = ({ marketData, isLoading }) => {
  // Debug logging to see what's in the marketData
  useEffect(() => {
    console.log('MarketOverview received data:', marketData);
  }, [marketData]);

  // Format price as USD
  const formatPrice = (price: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  // Format percentage with + or - sign
  const formatPercentage = (percentage: number): string => {
    const sign = percentage >= 0 ? '+' : '';
    return `${sign}${percentage.toFixed(2)}%`;
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead className="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Coin
            </th>
            <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Price
            </th>
            <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              24h Change
            </th>
            <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Market Cap
            </th>
          </tr>
        </thead>
        <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          {isLoading ? (
            <tr>
              <td colSpan={4} className="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
                Loading market data...
              </td>
            </tr>
          ) : !marketData || marketData.length === 0 ? (
            <tr>
              <td colSpan={4} className="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
                No market data available
              </td>
            </tr>
          ) : (
            marketData.map((coin) => (
              <tr key={coin.symbol} className="hover:bg-gray-50 dark:hover:bg-gray-750">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div>
                      <div className="text-sm font-medium text-gray-900 dark:text-white">
                        {coin.name}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        {coin.symbol}
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium text-gray-900 dark:text-white">
                  {formatPrice(coin.currentPrice)}
                </td>
                <td className={`px-6 py-4 whitespace-nowrap text-right text-sm font-medium ${
                  coin.priceChangePercentage24h >= 0 
                    ? 'text-green-600 dark:text-green-400' 
                    : 'text-red-600 dark:text-red-400'
                }`}>
                  {formatPercentage(coin.priceChangePercentage24h)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-gray-500 dark:text-gray-400">
                  {formatPrice(coin.marketCap / 1000000000)}B
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default MarketOverview; 