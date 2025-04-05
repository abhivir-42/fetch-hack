import React, { useState } from 'react';
import MainLayout from '../layouts/MainLayout';
import WalletConnect from '../components/wallet/WalletConnect';
import InvestmentForm from '../components/forms/InvestmentForm';
import { InvestmentParameters } from '../types/wallet';
import Card from '../components/common/Card';

const Settings: React.FC = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [lastDecision, setLastDecision] = useState<string | null>(null);

  const handleInvestmentSubmit = (parameters: InvestmentParameters) => {
    setIsSubmitting(true);
    
    // Mock API call
    setTimeout(() => {
      // Generate mock reasoning
      const reasoning = `Based on the ${parameters.investorType} investor profile and ${parameters.riskStrategy} risk strategy, we recommend a portfolio allocation focused on ${getRecommendation(parameters)}.`;
      
      setLastDecision(reasoning);
      setIsSubmitting(false);
    }, 1500);
  };

  // Helper function to generate recommendations based on parameters
  const getRecommendation = (params: InvestmentParameters): string => {
    if (params.investorType === 'conservative') {
      if (params.riskStrategy === 'low') {
        return 'stablecoins and established large-cap assets like BTC and ETH (80% stable, 20% growth)';
      } else if (params.riskStrategy === 'moderate') {
        return 'a mix of established assets with some mid-cap opportunities (60% stable, 40% growth)';
      } else {
        return 'a balanced portfolio with some strategic high-potential investments (50% stable, 50% growth)';
      }
    } else if (params.investorType === 'balanced') {
      if (params.riskStrategy === 'low') {
        return 'established assets with some strategic altcoin positions (60% stable, 40% growth)';
      } else if (params.riskStrategy === 'moderate') {
        return 'a diverse mix of assets across market caps with emerging chains (40% stable, 60% growth)';
      } else {
        return 'growth-focused assets with strategic investments in newer protocols (30% stable, 70% growth)';
      }
    } else {
      if (params.riskStrategy === 'low') {
        return 'growth-focused assets with some established cryptocurrencies as anchors (40% stable, 60% growth)';
      } else if (params.riskStrategy === 'moderate') {
        return 'primarily high-growth assets with strategic positions in emerging technologies (25% stable, 75% growth)';
      } else {
        return 'high-potential assets, new protocols, and strategic investments in emerging market sectors (15% stable, 85% growth)';
      }
    }
  };

  return (
    <MainLayout>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <p className="text-gray-600 dark:text-gray-400">Manage your wallet and investment preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <WalletConnect />
          
          <InvestmentForm 
            onSubmit={handleInvestmentSubmit} 
            isLoading={isSubmitting}
          />
        </div>
        
        <div>
          <Card title="AI Reasoning" className="h-full">
            {isSubmitting ? (
              <div className="flex items-center justify-center py-12">
                <div className="animate-pulse text-gray-500 dark:text-gray-400">
                  Analyzing investment parameters...
                </div>
              </div>
            ) : lastDecision ? (
              <div>
                <div className="mb-4 text-gray-700 dark:text-gray-300">
                  {lastDecision}
                </div>
                <div className="mt-6 border-t border-gray-200 dark:border-gray-700 pt-4">
                  <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">Risk Assessment</h3>
                  <div className="mt-2 flex items-center">
                    <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div className="bg-indigo-600 h-2 rounded-full" style={{ width: '65%' }}></div>
                    </div>
                    <span className="ml-3 text-sm text-gray-600 dark:text-gray-400">Moderate</span>
                  </div>
                </div>
                <div className="mt-4">
                  <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">Expected Return</h3>
                  <div className="mt-2 flex items-center">
                    <div className="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div className="bg-green-500 h-2 rounded-full" style={{ width: '75%' }}></div>
                    </div>
                    <span className="ml-3 text-sm text-gray-600 dark:text-gray-400">+12-18%</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <p className="text-gray-500 dark:text-gray-400 mb-2">
                  Submit your investment parameters to see AI-generated reasoning
                </p>
                <p className="text-sm text-gray-400 dark:text-gray-500">
                  Our AI will analyze your preferences and provide recommendations.
                </p>
              </div>
            )}
          </Card>
        </div>
      </div>
    </MainLayout>
  );
};

export default Settings; 