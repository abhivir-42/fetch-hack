import React, { useState } from 'react';
import Card from '../common/Card';
import Input from '../common/Input';
import Button from '../common/Button';
import { InvestmentParameters, InvestorType, NetworkType, RiskStrategy } from '../../types/wallet';

interface InvestmentFormProps {
  onSubmit: (parameters: InvestmentParameters) => void;
  isLoading?: boolean;
}

const InvestmentForm: React.FC<InvestmentFormProps> = ({ 
  onSubmit, 
  isLoading = false 
}) => {
  const [amount, setAmount] = useState<number>(100);
  const [network, setNetwork] = useState<NetworkType>('ethereum');
  const [investorType, setInvestorType] = useState<InvestorType>('balanced');
  const [riskStrategy, setRiskStrategy] = useState<RiskStrategy>('moderate');
  const [errors, setErrors] = useState<{amount?: string}>({});

  const networks = [
    { id: 'ethereum', name: 'Ethereum' },
    { id: 'base', name: 'Base' },
    { id: 'arbitrum', name: 'Arbitrum' },
    { id: 'optimism', name: 'Optimism' },
  ];

  const investorTypes = [
    { id: 'conservative', name: 'Conservative' },
    { id: 'balanced', name: 'Balanced' },
    { id: 'aggressive', name: 'Aggressive' },
  ];

  const riskStrategies = [
    { id: 'low', name: 'Low Risk' },
    { id: 'moderate', name: 'Moderate Risk' },
    { id: 'high', name: 'High Risk' },
  ];

  const validateForm = () => {
    const newErrors: {amount?: string} = {};
    let isValid = true;

    if (!amount || amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0';
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    onSubmit({
      amount,
      network,
      investorType,
      riskStrategy,
    });
  };

  return (
    <Card title="Investment Parameters">
      <form onSubmit={handleSubmit}>
        <div className="space-y-4">
          <div>
            <Input
              label="Amount (USD)"
              type="number"
              id="amount"
              min="1"
              step="1"
              value={amount}
              onChange={(e) => setAmount(Number(e.target.value))}
              error={errors.amount}
              disabled={isLoading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Network
            </label>
            <select
              className="block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white p-2"
              value={network}
              onChange={(e) => setNetwork(e.target.value as NetworkType)}
              disabled={isLoading}
            >
              {networks.map((net) => (
                <option key={net.id} value={net.id}>
                  {net.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Investor Type
            </label>
            <div className="grid grid-cols-3 gap-3">
              {investorTypes.map((type) => (
                <button
                  key={type.id}
                  type="button"
                  className={`
                    px-3 py-2 text-sm font-medium rounded-md 
                    ${investorType === type.id
                      ? 'bg-indigo-600 text-white'
                      : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600'
                    }
                  `}
                  onClick={() => setInvestorType(type.id as InvestorType)}
                  disabled={isLoading}
                >
                  {type.name}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Risk Strategy
            </label>
            <div className="grid grid-cols-3 gap-3">
              {riskStrategies.map((strategy) => (
                <button
                  key={strategy.id}
                  type="button"
                  className={`
                    px-3 py-2 text-sm font-medium rounded-md 
                    ${riskStrategy === strategy.id
                      ? 'bg-indigo-600 text-white'
                      : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600'
                    }
                  `}
                  onClick={() => setRiskStrategy(strategy.id as RiskStrategy)}
                  disabled={isLoading}
                >
                  {strategy.name}
                </button>
              ))}
            </div>
          </div>

          <div className="mt-6">
            <Button
              type="submit"
              isLoading={isLoading}
              fullWidth
            >
              Submit Investment
            </Button>
          </div>
        </div>
      </form>
    </Card>
  );
};

export default InvestmentForm; 