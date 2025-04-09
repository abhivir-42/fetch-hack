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
      <div className="mx-auto max-w-5xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Trade Analysis</h1>
          <p className="text-gray-600">
            Submit your trading parameters to get AI-powered analysis and recommendations.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2">
            <div className="card mb-8">
              <h2 className="text-xl font-semibold mb-4">Trading Parameters</h2>
              <UserInputForm onSubmit={handleSubmit} isLoading={isLoading} />
            </div>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
                <p>{error}</p>
              </div>
            )}

            {(result || isLoading) && (
              <TradeResult result={result} isLoading={isLoading} />
            )}
          </div>

          <div className="md:col-span-1">
            <AgentStatus />
            
            <div className="card p-4 mt-6">
              <h2 className="text-lg font-semibold mb-3">About This Service</h2>
              <div className="text-sm text-gray-600 space-y-2">
                <p>
                  This tool uses Fetch.ai agents to analyze cryptocurrency market conditions
                  and provide trading recommendations.
                </p>
                <p>
                  The system analyzes market data, fear & greed index, news, and other indicators
                  to help you make informed decisions.
                </p>
                <p>
                  <strong>Note:</strong> Always do your own research before making trading decisions.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
} 