import { useState } from 'react';
import { Transaction } from '../lib/types';
import { executeTrade } from '../lib/api';

interface TradeResultProps {
  result?: Transaction;
  isLoading: boolean;
}

export default function TradeResult({ result, isLoading }: TradeResultProps) {
  const [showReasoning, setShowReasoning] = useState(false);
  const [swapStatus, setSwapStatus] = useState<string | null>(null);
  const [isSwapping, setIsSwapping] = useState(false);
  
  if (isLoading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center py-10">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          <p className="ml-4 text-lg">Processing your request...</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  // Function to determine action from result
  const getAction = () => {
    // First check if there's a direct action property
    if (typeof result.action === 'string') {
      return result.action;
    }
    
    // Otherwise check details or message
    const details = typeof result.details === 'string' ? result.details.toLowerCase() : '';
    const message = typeof result.message === 'string' ? result.message.toLowerCase() : '';
    
    if (details.includes('sell') || message.includes('sell') || 
        details.includes('ethusdc') || message.includes('ethusdc')) {
      return 'SELL';
    } else if (details.includes('buy') || message.includes('buy') || 
               details.includes('usdceth') || message.includes('usdceth')) {
      return 'BUY';
    } else if (details.includes('hold') || message.includes('hold')) {
      return 'HOLD';
    }
    return 'UNKNOWN';
  };

  const action = getAction();
  
  let actionClass = 'bg-gray-100 text-gray-800';
  if (action === 'BUY') {
    actionClass = 'bg-green-100 text-green-800';
  } else if (action === 'SELL') {
    actionClass = 'bg-red-100 text-red-800';
  } else if (action === 'HOLD') {
    actionClass = 'bg-blue-100 text-blue-800';
  }

  // Handle swap initiation
  const handleSwap = async () => {
    setIsSwapping(true);
    try {
      // Placeholder - would normally call executeTrade API
      // const response = await executeTrade(action, result.amount || 0);
      
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Set placeholder success status
      setSwapStatus('COMPLETED');
    } catch (error) {
      console.error('Error executing trade:', error);
      setSwapStatus('FAILED');
    } finally {
      setIsSwapping(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-4">Trading Result</h2>
      
      <div className="mb-4 flex items-center flex-wrap gap-2">
        <span className={`inline-block px-3 py-1 rounded-full font-medium ${actionClass}`}>
          {action}
        </span>
        
        {swapStatus && (
          <span className={`inline-block px-3 py-1 rounded-full font-medium ${
            swapStatus === 'COMPLETED' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            Swap {swapStatus}
          </span>
        )}
      </div>
      
      {(result.details || result.message) && (
        <div className="mb-4">
          <h3 className="text-gray-700 font-medium mb-2">Details</h3>
          <p className="text-gray-600">{result.details || result.message}</p>
        </div>
      )}
      
      {result.tx_hash && (
        <div className="mb-4">
          <h3 className="text-gray-700 font-medium mb-2">Transaction Hash</h3>
          <p className="text-sm bg-gray-100 p-2 rounded font-mono break-all">
            {result.tx_hash}
          </p>
        </div>
      )}
      
      <div className="mt-6 flex flex-col md:flex-row gap-4 justify-between">
        {!swapStatus && action !== 'HOLD' && (
          <button
            onClick={handleSwap}
            disabled={isSwapping}
            className={`px-4 py-2 rounded font-medium text-white ${
              isSwapping ? 'bg-gray-400' : action === 'BUY' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'
            } transition-colors`}
          >
            {isSwapping ? (
              <span className="flex items-center">
                <span className="inline-block h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
                Processing...
              </span>
            ) : (
              `Initiate ${action} Swap`
            )}
          </button>
        )}
        
        <button
          onClick={() => setShowReasoning(!showReasoning)}
          className="text-sm px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded transition self-start"
        >
          {showReasoning ? 'Hide AI Analysis' : 'Show AI Analysis'}
        </button>
      </div>
      
      {showReasoning && (
        <div className="mt-3 p-4 bg-gray-50 rounded border border-gray-200">
          <h3 className="text-base font-medium mb-3">AI Analysis & Reasoning</h3>
          
          <div className="space-y-3">
            <div>
              <h4 className="text-sm font-semibold text-gray-700">Recommendation:</h4>
              <p className="text-sm text-gray-700">
                <span className={`inline-block px-2 py-0.5 rounded-full font-medium ${actionClass} mr-2`}>
                  {action}
                </span>
                {result.amount && `${result.amount} ETH`}
                {result.price && ` at approximately $${result.price}`}
              </p>
            </div>
            
            <div>
              <h4 className="text-sm font-semibold text-gray-700">Analysis:</h4>
              <p className="text-sm text-gray-700 whitespace-pre-line">
                {result.reasoning || result.details || "No detailed analysis available."}
              </p>
            </div>
            
            {result.message && result.message !== result.details && (
              <div>
                <h4 className="text-sm font-semibold text-gray-700">Additional Information:</h4>
                <p className="text-sm text-gray-700">{result.message}</p>
              </div>
            )}
          </div>
        </div>
      )}
      
      <div className="text-sm text-gray-500 mt-4">
        {result.timestamp && (
          <p>
            Processed at: {new Date(result.timestamp * 1000).toLocaleString()}
          </p>
        )}
      </div>
    </div>
  );
} 