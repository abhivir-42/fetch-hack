import React from 'react';
import Card from '../common/Card';
import { HeartbeatData } from '../../types/api';

interface SystemStatusCardProps {
  heartbeat: HeartbeatData | null;
  agentsOnline: number;
  totalAgents: number;
  isLoading: boolean;
}

const SystemStatusCard: React.FC<SystemStatusCardProps> = ({ 
  heartbeat, 
  agentsOnline,
  totalAgents,
  isLoading
}) => {
  const getStatusBadgeClass = (status: string) => {
    switch(status) {
      case 'healthy':
        return 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200';
      case 'warning':
        return 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200';
      case 'error':
        return 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200';
      default:
        return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200';
    }
  };
  
  return (
    <Card title="System Status">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-gray-600 dark:text-gray-400">Heartbeat</span>
          {isLoading ? (
            <span className="text-gray-400 dark:text-gray-500">Loading...</span>
          ) : !heartbeat ? (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200">
              Unavailable
            </span>
          ) : (
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeClass(heartbeat.status)}`}>
              {heartbeat.status.charAt(0).toUpperCase() + heartbeat.status.slice(1)}
            </span>
          )}
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-gray-600 dark:text-gray-400">Trading Status</span>
          {isLoading ? (
            <span className="text-gray-400 dark:text-gray-500">Loading...</span>
          ) : !heartbeat ? (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200">
              Disabled
            </span>
          ) : (
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              heartbeat.response.tradingEnabled 
                ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                : 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
            }`}>
              {heartbeat.response.tradingEnabled ? 'Enabled' : 'Disabled'}
            </span>
          )}
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-gray-600 dark:text-gray-400">Agents Online</span>
          <span className="text-gray-900 dark:text-white font-medium">
            {isLoading ? '...' : `${agentsOnline}/${totalAgents}`}
          </span>
        </div>
        
        {heartbeat && heartbeat.response.message && (
          <div className="pt-2 mt-2 border-t border-gray-200 dark:border-gray-700">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {heartbeat.response.message}
            </p>
          </div>
        )}
      </div>
    </Card>
  );
};

export default SystemStatusCard; 