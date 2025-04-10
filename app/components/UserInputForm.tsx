import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { UserInputs } from '../lib/types';

interface UserInputFormProps {
  onSubmit: (data: UserInputs) => void;
  isLoading?: boolean;
}

export default function UserInputForm({
  onSubmit,
  isLoading = false,
}: UserInputFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<UserInputs>({
    defaultValues: {
      topupWallet: 'yes',
      topupAmount: 6,
      privateKey: '',
      network: 'ethereum',
      investorType: 'speculative',
      riskStrategy: 'balanced',
      reason: '',
    },
  });

  const topupWallet = watch('topupWallet');

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Top up wallet?
          </label>
          <select
            {...register('topupWallet', { required: 'This field is required' })}
            className="input-field"
          >
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
          {errors.topupWallet && (
            <p className="mt-1 text-sm text-red-600">{errors.topupWallet.message}</p>
          )}
        </div>

        {topupWallet === 'yes' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Amount to top up with
            </label>
            <input
              type="number"
              step="0.1"
              min="0"
              {...register('topupAmount', {
                required: 'This field is required',
                min: {
                  value: 6,
                  message: 'You need at least 6 FET',
                },
              })}
              className="input-field"
            />
            {errors.topupAmount && (
              <p className="mt-1 text-sm text-red-600">{errors.topupAmount.message}</p>
            )}
          </div>
        )}

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            EVM Private Key
          </label>
          <input
            type="password"
            {...register('privateKey', { required: 'Private key is required' })}
            className="input-field"
            placeholder="Enter your EVM private key"
          />
          {errors.privateKey && (
            <p className="mt-1 text-sm text-red-600">{errors.privateKey.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Network
          </label>
          <select
            {...register('network', { required: 'This field is required' })}
            className="input-field"
          >
            <option value="ethereum">Ethereum</option>
            <option value="base">Base</option>
            <option value="polygon">Polygon</option>
            <option value="bitcoin">Bitcoin</option>
          </select>
          {errors.network && (
            <p className="mt-1 text-sm text-red-600">{errors.network.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Investor Type
          </label>
          <select
            {...register('investorType', { required: 'This field is required' })}
            className="input-field"
          >
            <option value="long-term">Long-term</option>
            <option value="short-term">Short-term</option>
            <option value="speculative">Speculative</option>
          </select>
          {errors.investorType && (
            <p className="mt-1 text-sm text-red-600">{errors.investorType.message}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Risk Strategy
          </label>
          <select
            {...register('riskStrategy', { required: 'This field is required' })}
            className="input-field"
          >
            <option value="conservative">Conservative</option>
            <option value="balanced">Balanced</option>
            <option value="aggressive">Aggressive</option>
            <option value="speculative">Speculative</option>
          </select>
          {errors.riskStrategy && (
            <p className="mt-1 text-sm text-red-600">{errors.riskStrategy.message}</p>
          )}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Reason for Trade Action
        </label>
        <textarea
          {...register('reason', {
            required: 'Please provide a reason',
            minLength: {
              value: 10,
              message: 'Reason should be at least 10 characters',
            },
          })}
          rows={4}
          className="input-field"
          placeholder="Why would you like to perform Buy/Sell/Hold action?"
        />
        {errors.reason && (
          <p className="mt-1 text-sm text-red-600">{errors.reason.message}</p>
        )}
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isLoading}
          className={`btn btn-primary ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
        >
          {isLoading ? 'Processing...' : 'Start Analysis'}
        </button>
      </div>
    </form>
  );
} 