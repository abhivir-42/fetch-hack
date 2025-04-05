import React from 'react';
import Card from '../common/Card';
import { Agent } from '../../types/agents';

interface AgentStatusListProps {
  agents: Agent[];
  isLoading: boolean;
}

const AgentStatusList: React.FC<AgentStatusListProps> = ({ agents, isLoading }) => {
  // Format date to readable string
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString();
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {isLoading ? (
        <div className="col-span-full text-center py-4 text-gray-500 dark:text-gray-400">
          Loading agent status...
        </div>
      ) : agents.length === 0 ? (
        <div className="col-span-full text-center py-4 text-gray-500 dark:text-gray-400">
          No agents available
        </div>
      ) : (
        agents.map((agent) => (
          <Card key={agent.id} className="h-full">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                  {agent.name}
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                  {agent.description}
                </p>
              </div>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                agent.status === 'online' 
                  ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                  : agent.status === 'error'
                    ? 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
              }`}>
                {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
              </span>
            </div>
            {agent.lastActive && (
              <div className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                Last active: {formatDate(agent.lastActive)}
              </div>
            )}
          </Card>
        ))
      )}
    </div>
  );
};

export default AgentStatusList; 