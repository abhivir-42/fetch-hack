import React, { useState, useEffect } from 'react';
import { Agent } from '../../types/agents';

interface AgentActivityProps {
  agents: Agent[];
  isLoading: boolean;
  error?: string;
}

const AgentActivityChart: React.FC<AgentActivityProps> = ({ agents, isLoading, error }) => {
  const [selectedTimeRange, setSelectedTimeRange] = useState<'hour' | 'day' | 'week'>('hour');
  
  // This would be replaced with real data from an API endpoint in a production app
  const generateMockActivityData = (timeRange: 'hour' | 'day' | 'week') => {
    // Each agent gets a row, each time slot gets a column
    // For each agent, we randomly mark some activities
    const timeSlots = timeRange === 'hour' ? 12 : timeRange === 'day' ? 24 : 7;
    
    return agents.map(agent => {
      const activity = Array(timeSlots).fill(0).map(() => {
        // Simulate different activity levels based on agent type
        const activityChance = agent.type === 'main' || agent.type === 'heartbeat' ? 0.9 : 
                              agent.type === 'market' || agent.type === 'news' ? 0.7 : 0.5;
        return Math.random() < activityChance ? 1 : 0;
      });
      
      return {
        id: agent.id,
        name: agent.id, // Using id as name for simplicity
        activity
      };
    });
  };

  const [activityData, setActivityData] = useState<Array<{ id: string; name: string; activity: number[] }>>([]);

  useEffect(() => {
    if (!isLoading && agents.length > 0) {
      setActivityData(generateMockActivityData(selectedTimeRange));
    }
  }, [agents, isLoading, selectedTimeRange]);

  const getTimeLabels = () => {
    if (selectedTimeRange === 'hour') {
      return Array(12).fill(0).map((_, i) => `${i * 5}m`);
    } else if (selectedTimeRange === 'day') {
      return Array(24).fill(0).map((_, i) => `${i}h`);
    } else {
      return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 animate-pulse">
        <div className="h-40 bg-gray-200 dark:bg-gray-700 rounded"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        <p className="text-red-500 dark:text-red-400">Error: {error}</p>
      </div>
    );
  }

  if (!agents.length) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        <p className="text-gray-500 dark:text-gray-400">No agent data available</p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">Agent Activity</h3>
        <div className="flex space-x-2">
          <button
            onClick={() => setSelectedTimeRange('hour')}
            className={`px-3 py-1 text-sm rounded-md ${
              selectedTimeRange === 'hour'
                ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-400'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
            }`}
          >
            Hour
          </button>
          <button
            onClick={() => setSelectedTimeRange('day')}
            className={`px-3 py-1 text-sm rounded-md ${
              selectedTimeRange === 'day'
                ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-400'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
            }`}
          >
            Day
          </button>
          <button
            onClick={() => setSelectedTimeRange('week')}
            className={`px-3 py-1 text-sm rounded-md ${
              selectedTimeRange === 'week'
                ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-400'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
            }`}
          >
            Week
          </button>
        </div>
      </div>

      <div className="overflow-x-auto">
        <div className="min-w-full">
          {/* Time labels */}
          <div className="flex mb-1">
            <div className="w-24 flex-shrink-0"></div>
            <div className="flex-1 flex">
              {getTimeLabels().map((label, i) => (
                <div key={i} className="flex-1 text-xs text-center text-gray-500 dark:text-gray-400">
                  {label}
                </div>
              ))}
            </div>
          </div>

          {/* Agent rows */}
          {activityData.map((agent) => (
            <div key={agent.id} className="flex mb-2">
              <div className="w-24 flex-shrink-0 pr-2 text-sm text-gray-600 dark:text-gray-300 truncate">
                {agent.name}
              </div>
              <div className="flex-1 flex">
                {agent.activity.map((active, i) => (
                  <div key={i} className="flex-1 flex items-center justify-center">
                    <div
                      className={`h-5 w-5 rounded-full ${
                        active
                          ? 'bg-green-500 dark:bg-green-600'
                          : 'bg-gray-200 dark:bg-gray-700'
                      }`}
                    ></div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AgentActivityChart; 