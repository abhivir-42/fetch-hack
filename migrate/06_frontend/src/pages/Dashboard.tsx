import React from 'react';
import MainLayout from '../layouts/MainLayout';
import MarketOverview from '../components/dashboard/MarketOverview';
import AgentStatusList from '../components/dashboard/AgentStatusList';
import SystemStatusCard from '../components/dashboard/SystemStatusCard';
import PortfolioSummaryCard from '../components/dashboard/PortfolioSummaryCard';
import { useRealTimeMarketData, useRealTimeAgentStatuses, useRealTimeHeartbeat } from '../hooks/useRealTimeData';

const Dashboard: React.FC = () => {
  // Use real-time data hooks with reduced polling frequency (60s instead of 30s)
  // and disable auto-polling to reduce API calls
  const { 
    data: marketData, 
    isLoading: isLoadingMarket, 
    error: marketError,
    refetch: refetchMarket
  } = useRealTimeMarketData(60000, false);
  
  const { 
    data: agents, 
    isLoading: isLoadingAgents, 
    error: agentsError,
    refetch: refetchAgents
  } = useRealTimeAgentStatuses(60000, false);
  
  const { 
    data: heartbeat, 
    isLoading: isLoadingHeartbeat, 
    error: heartbeatError,
    refetch: refetchHeartbeat
  } = useRealTimeHeartbeat(60000, false);

  // Initial data fetch
  React.useEffect(() => {
    // Stagger API calls to avoid hitting rate limits
    const fetchData = async () => {
      await refetchMarket();
      setTimeout(async () => {
        await refetchAgents();
        setTimeout(async () => {
          await refetchHeartbeat();
        }, 500);
      }, 500);
    };
    
    fetchData();
    
    // Optional: Set up a manual refresh every 2 minutes instead of continuous polling
    const intervalId = setInterval(fetchData, 120000);
    return () => clearInterval(intervalId);
  }, [refetchMarket, refetchAgents, refetchHeartbeat]);

  // Portfolio data (would be fetched from API in a real implementation)
  const portfolioData = {
    totalValue: 12345.67,
    weeklyChange: 5.23
  };

  // Combined error message
  const errorMessage = marketError || agentsError || heartbeatError;

  // Manual refresh of all data with staggered calls
  const handleRefreshData = async () => {
    await refetchMarket();
    setTimeout(async () => {
      await refetchAgents();
      setTimeout(async () => {
        await refetchHeartbeat();
      }, 500);
    }, 500);
  };

  return (
    <MainLayout>
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
          <p className="text-gray-600 dark:text-gray-400">Overview of your crypto portfolio and system status</p>
        </div>
        <button 
          onClick={handleRefreshData}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
          aria-label="Refresh dashboard data"
        >
          Refresh
        </button>
      </div>

      {errorMessage && (
        <div className="mb-6 p-4 bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200 rounded-md">
          {errorMessage}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <PortfolioSummaryCard 
          totalValue={portfolioData.totalValue}
          weeklyChange={portfolioData.weeklyChange}
          isLoading={isLoadingMarket}
        />

        <SystemStatusCard
          heartbeat={heartbeat}
          agentsOnline={agents?.filter(a => a.status === 'online').length || 0}
          totalAgents={agents?.length || 0}
          isLoading={isLoadingHeartbeat || isLoadingAgents}
        />
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Market Overview</h2>
        <MarketOverview 
          marketData={marketData || []} 
          isLoading={isLoadingMarket} 
        />
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Agent Status</h2>
        <AgentStatusList 
          agents={agents || []} 
          isLoading={isLoadingAgents} 
        />
      </div>
    </MainLayout>
  );
};

export default Dashboard; 