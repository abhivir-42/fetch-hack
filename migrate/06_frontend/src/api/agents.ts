import { Agent } from '../types/agents';
import { HeartbeatData } from '../types/api';

// Mock agent data to avoid API rate limiting
const mockAgents: Agent[] = [
  {
    id: 'main-agent',
    name: 'Main Agent',
    type: 'main',
    description: 'Coordinates all agent activities',
    status: 'online',
    lastActive: new Date().toISOString(),
    metadata: { priority: 'high' }
  },
  {
    id: 'heartbeat-agent',
    name: 'Heartbeat Agent',
    type: 'heartbeat',
    description: 'Monitors system health',
    status: 'online',
    lastActive: new Date().toISOString()
  },
  {
    id: 'market-agent',
    name: 'Market Agent',
    type: 'market',
    description: 'Analyzes market conditions',
    status: 'online',
    lastActive: new Date().toISOString()
  },
  {
    id: 'swap-agent',
    name: 'Swap Agent',
    type: 'swap',
    description: 'Executes token swaps',
    status: 'online',
    lastActive: new Date().toISOString()
  },
  {
    id: 'news-agent',
    name: 'News Agent',
    type: 'news',
    description: 'Monitors crypto news',
    status: 'online',
    lastActive: new Date().toISOString()
  },
  {
    id: 'analysis-agent',
    name: 'Analysis Agent',
    type: 'analysis',
    description: 'Performs technical analysis',
    status: 'online',
    lastActive: new Date().toISOString()
  },
  {
    id: 'topup-agent',
    name: 'Topup Agent',
    type: 'topup',
    description: 'Manages wallet funding',
    status: 'online',
    lastActive: new Date().toISOString()
  },
  {
    id: 'reward-agent',
    name: 'Reward Agent',
    type: 'reward',
    description: 'Handles staking rewards',
    status: 'online',
    lastActive: new Date().toISOString()
  }
];

// Mock heartbeat data
const mockHeartbeat: HeartbeatData = {
  timestamp: new Date().toISOString(),
  status: 'healthy',
  response: {
    tradingEnabled: true,
    message: 'System operational'
  }
};

export const agentsApi = {
  /**
   * Get all agent statuses
   */
  getAgents: async (): Promise<Agent[]> => {
    try {
      console.log('Using mock agent data to avoid API rate limits');
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 300));
      
      return mockAgents;
    } catch (error) {
      console.error('Error fetching agents:', error);
      throw new Error('Failed to fetch agent data. Please try again.');
    }
  },
  
  /**
   * Get system heartbeat
   */
  getHeartbeat: async (): Promise<HeartbeatData> => {
    try {
      console.log('Using mock heartbeat data to avoid API rate limits');
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 200));
      
      // Generate a new timestamp each time
      return {
        ...mockHeartbeat,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error fetching heartbeat:', error);
      throw new Error('Failed to fetch heartbeat data. Please try again.');
    }
  },
  
  /**
   * Get agent logs
   */
  getAgentLogs: async (agentId: string): Promise<string[]> => {
    try {
      console.log(`Using mock log data for agent ${agentId}`);
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 400));
      
      // Generate mock logs
      return [
        `[${new Date().toISOString()}] Agent ${agentId} initialized`,
        `[${new Date(Date.now() - 60000).toISOString()}] Connection established`,
        `[${new Date(Date.now() - 120000).toISOString()}] Processing data`,
        `[${new Date(Date.now() - 180000).toISOString()}] Task completed successfully`
      ];
    } catch (error) {
      console.error(`Error fetching logs for agent ${agentId}:`, error);
      throw new Error(`Failed to fetch logs for agent ${agentId}. Please try again.`);
    }
  }
}; 