import React from 'react';
import Card from '../common/Card';

interface PortfolioSummaryCardProps {
  totalValue: number;
  weeklyChange: number;
  isLoading?: boolean;
}

const PortfolioSummaryCard: React.FC<PortfolioSummaryCardProps> = ({ 
  totalValue, 
  weeklyChange,
  isLoading = false
}) => {
  // Format currency
  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  // Format percentage with + or - sign
  const formatPercentage = (percentage: number): string => {
    const sign = percentage >= 0 ? '+' : '';
    return `${sign}${percentage.toFixed(2)}%`;
  };

  // Determine color based on percentage
  const getPercentageColor = (percentage: number): string => {
    return percentage >= 0 
      ? 'text-green-600 dark:text-green-400' 
      : 'text-red-600 dark:text-red-400';
  };

  // Calculate progress bar width - cap at 100%
  const progressWidth = Math.min(Math.abs(weeklyChange) * 5, 100);

  return (
    <Card title="Portfolio Summary">
      <div className="flex items-center justify-between mb-4">
        <span className="text-gray-600 dark:text-gray-400">Total Value</span>
        {isLoading ? (
          <div className="h-6 w-24 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        ) : (
          <span className="text-xl font-semibold text-gray-900 dark:text-white">
            {formatCurrency(totalValue)}
          </span>
        )}
      </div>
      <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        {isLoading ? (
          <div className="h-full bg-gray-300 dark:bg-gray-600 animate-pulse"></div>
        ) : (
          <div
            className={`h-full ${
              weeklyChange >= 0 
                ? 'bg-green-600 dark:bg-green-500' 
                : 'bg-red-600 dark:bg-red-500'
            }`}
            style={{ width: `${progressWidth}%` }}
          ></div>
        )}
      </div>
      <div className="flex justify-between mt-2 text-sm">
        <span className="text-gray-600 dark:text-gray-400">Weekly Change</span>
        {isLoading ? (
          <div className="h-4 w-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
        ) : (
          <span className={getPercentageColor(weeklyChange)}>
            {formatPercentage(weeklyChange)}
          </span>
        )}
      </div>
    </Card>
  );
};

export default PortfolioSummaryCard; 