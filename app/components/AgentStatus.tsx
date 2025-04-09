import { useEffect, useState } from 'react';
import { getAgentStatus } from '../lib/api';
import { AgentStatus as AgentStatusType } from '../lib/types';

export default function AgentStatus() {
  const [agentStatus, setAgentStatus] = useState<AgentStatusType>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgentStatus = async () => {
      try {
        setLoading(true);
        const status = await getAgentStatus();
        setAgentStatus(status);
        setError(null);
      } catch (err) {
        setError('Failed to fetch agent status');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAgentStatus();
    const intervalId = setInterval(fetchAgentStatus, 10000); // Update every 10 seconds

    return () => clearInterval(intervalId);
  }, []);

  if (loading) {
    return (
      <div className="card p-4">
        <h2 className="text-lg font-semibold mb-3">Agent Status</h2>
        <div className="flex justify-center py-4">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card p-4">
        <h2 className="text-lg font-semibold mb-3">Agent Status</h2>
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  // Display friendly names for agents
  const agentNames: Record<string, string> = {
    main_agent: 'Main Agent',
    heartbeat_agent: 'Heartbeat Agent',
    coin_info_agent: 'Coin Info Agent',
    fgi_agent: 'Fear & Greed Index Agent',
    crypto_news_agent: 'Crypto News Agent',
    llm_agent: 'LLM Agent',
    reward_agent: 'Reward Agent',
    topup_agent: 'Topup Agent',
    swapfinder_agent: 'Swap Finder Agent',
    swap_eth_to_usdc: 'ETH to USDC Swap Agent',
    swap_usdc_to_eth: 'USDC to ETH Swap Agent',
  };

  return (
    <div className="card p-4">
      <h2 className="text-lg font-semibold mb-3">Agent Status</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {Object.entries(agentStatus).map(([agentId, status]) => (
          <div key={agentId} className="flex items-center space-x-2">
            <span
              className={`w-3 h-3 rounded-full ${
                status ? 'bg-green-500' : 'bg-red-500'
              }`}
            ></span>
            <span className="text-sm">
              {agentNames[agentId] || agentId}: {status ? 'Running' : 'Stopped'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
} 