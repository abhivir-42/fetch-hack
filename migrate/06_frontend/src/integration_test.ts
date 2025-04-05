/**
 * CryptoFund Integration Tests
 * 
 * This file contains tests to verify the integration between frontend API services and UI components.
 * Run these tests to ensure data flows correctly from services to the frontend.
 */

import { agentsApi } from './api/agents';
import { marketApi } from './api/market';
import { walletApi } from './api/wallet';

// Mock console.log for testing
const originalLog = console.log;
const logs: string[] = [];
console.log = (...args) => {
  logs.push(args.join(' '));
  originalLog(...args);
};

/**
 * Test agent service API
 */
async function testAgentsApi() {
  try {
    console.log('🧪 Testing Agents API');
    
    // Test getting all agents
    const agents = await agentsApi.getAgents();
    console.log(`✅ Retrieved ${agents.length} agents`);
    
    if (agents.length === 0) {
      console.log('❌ No agents returned - API may be misconfigured');
      return false;
    }
    
    // Test agent status
    const firstAgentId = agents[0].id;
    const agentStatus = await agentsApi.getAgentStatus(firstAgentId);
    console.log(`✅ Agent status for ${firstAgentId}: ${agentStatus.status}`);
    
    // Test heartbeat
    const heartbeat = await agentsApi.getHeartbeat();
    console.log(`✅ Heartbeat status: ${heartbeat.status}`);
    console.log(`✅ Trading enabled: ${heartbeat.response.tradingEnabled}`);
    
    return true;
  } catch (error) {
    console.log(`❌ Agents API test failed: ${error}`);
    return false;
  }
}

/**
 * Test market data API
 */
async function testMarketApi() {
  try {
    console.log('🧪 Testing Market API');
    
    // Test getting market data
    const marketData = await marketApi.getMarketData();
    console.log(`✅ Retrieved ${marketData.length} market data entries`);
    
    if (marketData.length === 0) {
      console.log('❌ No market data returned - API may be misconfigured');
      return false;
    }
    
    // Test price history
    const symbol = marketData[0].symbol;
    const priceHistory = await marketApi.getPriceHistory(symbol, '24h');
    console.log(`✅ Retrieved ${priceHistory.length} price history points for ${symbol}`);
    
    return true;
  } catch (error) {
    console.log(`❌ Market API test failed: ${error}`);
    return false;
  }
}

/**
 * Test wallet API
 */
async function testWalletApi() {
  try {
    console.log('🧪 Testing Wallet API');
    
    // Test wallet connection
    const connection = await walletApi.connectWallet({ network: 'ethereum' });
    console.log(`✅ Connected to wallet: ${connection.address}`);
    
    if (!connection.isConnected) {
      console.log('❌ Wallet not connected - API may be misconfigured');
      return false;
    }
    
    // Test getting balance
    const balance = await walletApi.getBalance(connection.address, connection.network);
    console.log(`✅ Wallet balance: ${balance.balance}`);
    
    // Test disconnecting wallet
    await walletApi.disconnectWallet();
    console.log('✅ Wallet disconnected');
    
    return true;
  } catch (error) {
    console.log(`❌ Wallet API test failed: ${error}`);
    return false;
  }
}

/**
 * Run all integration tests
 */
async function runIntegrationTests() {
  console.log('📋 Starting CryptoFund Integration Tests');
  console.log('=======================================');
  
  const agentsResult = await testAgentsApi();
  console.log('---------------------------------------');
  
  const marketResult = await testMarketApi();
  console.log('---------------------------------------');
  
  const walletResult = await testWalletApi();
  console.log('---------------------------------------');
  
  console.log('📋 Integration Test Results:');
  console.log(`Agents API: ${agentsResult ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`Market API: ${marketResult ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`Wallet API: ${walletResult ? '✅ PASS' : '❌ FAIL'}`);
  
  const overall = agentsResult && marketResult && walletResult;
  console.log(`Overall: ${overall ? '✅ PASS' : '❌ FAIL'}`);
  
  return {
    agents: agentsResult,
    market: marketResult,
    wallet: walletResult,
    overall
  };
}

// Run tests immediately when this file is executed
runIntegrationTests()
  .then(results => {
    if (results.overall) {
      console.log('🎉 All integration tests passed!');
    } else {
      console.log('❌ Some integration tests failed. Please check the logs above.');
    }
  })
  .catch(error => {
    console.log('💥 Fatal error running integration tests:', error);
  });

// Export test functions for use in other files
export { runIntegrationTests, testAgentsApi, testMarketApi, testWalletApi }; 