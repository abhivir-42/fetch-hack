'use client';

import { useState } from 'react';
import MainLayout from '../components/MainLayout';
import UserInputForm from '../components/UserInputForm';
import TradeResult from '../components/TradeResult';
import AgentStatus from '../components/AgentStatus';
import { UserInputs, Transaction } from '../lib/types';
import { submitUserInputs } from '../lib/api';

export default function TradePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<Transaction | undefined>(undefined);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: UserInputs) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await submitUserInputs(data);
      if (response.status === 'success' && response.data) {
        setResult(response.data);
      } else {
        throw new Error(response.message || 'Failed to process trade request');
      }
    } catch (err) {
      console.error('Error submitting form:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <MainLayout>
      <div className="mx-auto max-w-6xl">
        <div className="mb-10">
          <h1 className="text-3xl md:text-4xl font-bold mb-3">
            <span className="gradient-text">Trade Analysis</span>
          </h1>
          <p className="text-gray-600 text-lg">
            Submit your trading parameters to get AI-powered analysis and recommendations.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2 space-y-8">
            <div className="card transition-all duration-300 hover:shadow-card-hover">
              <h2 className="text-xl font-semibold mb-6 border-b pb-3">Trading Parameters</h2>
              <UserInputForm onSubmit={handleSubmit} isLoading={isLoading} />
            </div>

            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded shadow-sm animate-fade-in">
                <div className="flex items-center">
                  <svg className="h-5 w-5 text-red-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <p className="font-medium">{error}</p>
                </div>
              </div>
            )}

            {(result || isLoading) && (
              <TradeResult result={result} isLoading={isLoading} />
            )}
          </div>

          <div className="md:col-span-1 space-y-6">
            <AgentStatus />
            
            <div className="card bg-gradient-to-br from-white to-gray-50 transition-all duration-300 hover:shadow-card-hover">
              <h2 className="text-lg font-semibold mb-4 pb-2 border-b">About This Service</h2>
              <div className="text-sm text-gray-600 space-y-3">
                <p>
                  This tool uses Fetch.ai agents to analyze cryptocurrency market conditions
                  and provide trading recommendations.
                </p>
                <p>
                  The system analyzes market data, fear & greed index, news, and other indicators
                  to help you make informed decisions.
                </p>
                <div className="bg-blue-50 border-l-4 border-blue-500 p-3 mt-4 rounded">
                  <p className="font-medium text-blue-700">
                    Always do your own research before making trading decisions.
                  </p>
                </div>
              </div>
            </div>
            
            <div className="card bg-primary/5 border border-primary/10 transition-all duration-300">
              <h2 className="text-lg font-semibold mb-3 text-primary">Need Help?</h2>
              <p className="text-sm text-gray-600 mb-4">
                Have questions about how to use this tool or interpret the results?
              </p>
              <a href="#" className="btn btn-outline text-primary border-primary/30 hover:bg-primary/5 w-full text-center text-sm">
                View Documentation
              </a>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
} 