import { Transaction } from '../lib/types';

interface TradeResultProps {
  result?: Transaction;
  isLoading: boolean;
}

export default function TradeResult({ result, isLoading }: TradeResultProps) {
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

  return (
    <div className="card">
      <h2 className="text-xl font-semibold mb-4">Trading Result</h2>
      
      <div className="mb-4">
        <span className={`inline-block px-3 py-1 rounded-full font-medium ${actionClass}`}>
          {action}
        </span>
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