import React, { useState } from 'react';
import { useWallet } from '../../contexts/WalletContext';
import Card from '../common/Card';
import Input from '../common/Input';
import Button from '../common/Button';
import { NetworkType } from '../../types/wallet';
import { ExclamationCircleIcon, ShieldCheckIcon, CreditCardIcon, ArrowPathIcon } from '@heroicons/react/24/outline';
// Remove the direct import until the API is properly connected
// import { walletApi } from '../../api/walletApi';

const networks: { id: NetworkType; name: string }[] = [
  { id: 'ethereum', name: 'Ethereum' },
  { id: 'base', name: 'Base' },
  { id: 'polygon', name: 'Polygon' },
  { id: 'bitcoin', name: 'Bitcoin' },
];

interface ValidationError {
  privateKey?: string;
  topupAmount?: string;
}

const WalletConnect: React.FC = () => {
  const { walletInfo, connectWallet, disconnectWallet, isConnecting, error } = useWallet();
  const [privateKey, setPrivateKey] = useState('');
  const [network, setNetwork] = useState<NetworkType>('ethereum');
  const [validationErrors, setValidationErrors] = useState<ValidationError>({});
  const [showTopup, setShowTopup] = useState(false);
  const [topupAmount, setTopupAmount] = useState('');
  const [isProcessingTopup, setIsProcessingTopup] = useState(false);
  const [topupSuccess, setTopupSuccess] = useState(false);
  const [topupError, setTopupError] = useState('');

  // Validate private key - basic ethereum key validation
  const validatePrivateKey = (key: string): string | undefined => {
    if (!key.trim()) {
      return 'Private key is required';
    }
    
    // Check if it's a valid hex string of correct length
    if (!/^(0x)?[0-9a-fA-F]{64}$/.test(key)) {
      return 'Invalid private key format';
    }
    
    return undefined;
  };

  // Validate topup amount - must be numeric and greater than 0
  const validateTopupAmount = (amount: string): string | undefined => {
    if (!amount.trim()) {
      return 'Amount is required';
    }
    
    const numericAmount = parseFloat(amount);
    if (isNaN(numericAmount) || numericAmount <= 0) {
      return 'Amount must be a positive number';
    }
    
    if (numericAmount > 10000) {
      return 'Maximum topup amount is $10,000';
    }
    
    return undefined;
  };

  const handleConnect = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate private key
    const keyError = validatePrivateKey(privateKey);
    setValidationErrors({ privateKey: keyError });
    
    if (keyError) {
      return;
    }

    try {
      // Encrypt the private key before sending (in a real app)
      // This is a simple example and should be enhanced with proper encryption
      const encryptedKey = `encrypted:${privateKey.slice(0, 5)}...`;
      
      await connectWallet({
        privateKey: encryptedKey,
        network,
      });
      
      // Clear private key from state after successful connection
      setPrivateKey('');
    } catch (err) {
      console.error('Error connecting wallet:', err);
    }
  };

  const handleDisconnect = async () => {
    try {
      await disconnectWallet();
      setShowTopup(false);
      setTopupSuccess(false);
      setTopupError('');
      setTopupAmount('');
    } catch (err) {
      console.error('Error disconnecting wallet:', err);
    }
  };
  
  const handleTopup = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate topup amount
    const amountError = validateTopupAmount(topupAmount);
    setValidationErrors({ topupAmount: amountError });
    
    if (amountError) {
      return;
    }
    
    setIsProcessingTopup(true);
    setTopupSuccess(false);
    setTopupError('');
    
    try {
      // Simulate a successful topup
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulate 90% success rate
      if (Math.random() > 0.1) {
        setTopupSuccess(true);
        setTopupAmount('');
      } else {
        setTopupError('Topup failed. Please try again.');
      }
    } catch (err) {
      console.error('Error processing topup:', err);
      setTopupError('An error occurred while processing your topup request.');
    } finally {
      setIsProcessingTopup(false);
    }
  };

  return (
    <Card title="Wallet Connection" className="mb-6">
      {error && (
        <div className="mb-4 p-3 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md text-sm flex items-start">
          <ExclamationCircleIcon className="h-5 w-5 mr-2 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {walletInfo?.isConnected ? (
        <div>
          <div className="mb-4">
            <div className="font-medium text-gray-700 dark:text-gray-300 mb-1">Connected Address</div>
            <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-md text-gray-800 dark:text-gray-200 font-mono text-sm break-all">
              {walletInfo.address}
            </div>
          </div>
          
          <div className="mb-4">
            <div className="font-medium text-gray-700 dark:text-gray-300 mb-1">Network</div>
            <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-md text-gray-800 dark:text-gray-200 text-sm">
              {networks.find(n => n.id === walletInfo.network)?.name || walletInfo.network}
            </div>
          </div>
          
          <div className="mb-4">
            <div className="font-medium text-gray-700 dark:text-gray-300 mb-1">Balance</div>
            <div className="p-3 bg-gray-100 dark:bg-gray-700 rounded-md text-gray-800 dark:text-gray-200 text-sm">
              {walletInfo.balance} {walletInfo.network === 'ethereum' ? 'ETH' : 
                walletInfo.network === 'bitcoin' ? 'BTC' : 
                walletInfo.network === 'polygon' ? 'MATIC' : 'Tokens'}
            </div>
          </div>
          
          {!showTopup ? (
            <div className="flex space-x-4">
              <Button
                variant="primary"
                onClick={() => setShowTopup(true)}
                icon={<CreditCardIcon className="h-5 w-5 mr-2" />}
              >
                Topup Wallet
              </Button>
              
              <Button
                variant="outline"
                onClick={handleDisconnect}
              >
                Disconnect Wallet
              </Button>
            </div>
          ) : (
            <form onSubmit={handleTopup} className="border-t border-gray-200 dark:border-gray-700 mt-4 pt-4">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Topup Wallet</h3>
              
              {topupSuccess && (
                <div className="mb-4 p-3 bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-300 rounded-md text-sm flex items-start">
                  <ShieldCheckIcon className="h-5 w-5 mr-2 flex-shrink-0" />
                  <span>Topup successful! Your balance will be updated shortly.</span>
                </div>
              )}
              
              {topupError && (
                <div className="mb-4 p-3 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md text-sm flex items-start">
                  <ExclamationCircleIcon className="h-5 w-5 mr-2 flex-shrink-0" />
                  <span>{topupError}</span>
                </div>
              )}
              
              <div className="mb-4">
                <Input
                  label="Amount in USD"
                  type="number"
                  step="0.01"
                  min="0.01"
                  placeholder="Enter amount to topup"
                  value={topupAmount}
                  onChange={(e) => setTopupAmount(e.target.value)}
                  disabled={isProcessingTopup}
                  error={validationErrors.topupAmount}
                  fullWidth
                />
              </div>
              
              <div className="flex space-x-4">
                <Button
                  type="submit"
                  isLoading={isProcessingTopup}
                  icon={<CreditCardIcon className="h-5 w-5 mr-2" />}
                >
                  Process Topup
                </Button>
                
                <Button
                  variant="outline"
                  onClick={() => {
                    setShowTopup(false);
                    setValidationErrors({});
                    setTopupAmount('');
                  }}
                  disabled={isProcessingTopup}
                >
                  Cancel
                </Button>
              </div>
            </form>
          )}
        </div>
      ) : (
        <form onSubmit={handleConnect}>
          <div className="mb-4">
            <div className="font-medium text-gray-700 dark:text-gray-300 mb-1">Select Network</div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {networks.map((net) => (
                <button
                  key={net.id}
                  type="button"
                  className={`p-3 border rounded-md text-center ${
                    network === net.id
                      ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-300'
                      : 'border-gray-300 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750'
                  }`}
                  onClick={() => setNetwork(net.id)}
                >
                  {net.name}
                </button>
              ))}
            </div>
          </div>
          
          <div className="mb-6">
            <Input
              label="Private Key"
              type="password"
              placeholder="Enter your private key"
              value={privateKey}
              onChange={(e) => setPrivateKey(e.target.value)}
              error={validationErrors.privateKey}
              fullWidth
            />
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Never share your private key. This field is for demonstration only.
            </p>
          </div>
          
          <Button
            type="submit"
            isLoading={isConnecting}
            fullWidth
          >
            Connect Wallet
          </Button>
        </form>
      )}
    </Card>
  );
};

export default WalletConnect; 