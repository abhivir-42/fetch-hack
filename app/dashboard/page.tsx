'use client';

import { useEffect, useState } from 'react';
import MainLayout from '../components/MainLayout';
import AgentStatus from '../components/AgentStatus';
import { getMarketData, getSentimentAnalysis, getNews, getTransactions } from '../lib/api';
import { CoinData, SentimentAnalysis, CryptoNews, Transaction } from '../lib/types';

export default function Dashboard() {
  const [marketData, setMarketData] = useState<CoinData | null>(null);
  const [sentiment, setSentiment] = useState<SentimentAnalysis | null>(null);
  const [news, setNews] = useState<CryptoNews | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [marketDataRes, sentimentRes, newsRes, transactionsRes] = await Promise.all([
          getMarketData(),
          getSentimentAnalysis(),
          getNews(),
          getTransactions(),
        ]);

        setMarketData(marketDataRes);
        setSentiment(sentimentRes);
        setNews(newsRes);
        setTransactions(transactionsRes);
        setError(null);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 60000); // Update every minute

    return () => clearInterval(intervalId);
  }, []);

  return (
    <MainLayout>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
        <p className="text-gray-600">
          Monitor market conditions and your trading history.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="card p-4">
          <h2 className="text-sm text-gray-500 uppercase mb-2">Current Price</h2>
          {loading ? (
            <div className="animate-pulse h-6 bg-gray-200 rounded w-24"></div>
          ) : (
            <p className="text-2xl font-bold">${marketData?.current_price.toLocaleString() || 'N/A'}</p>
          )}
          <p className="text-sm text-gray-500 mt-1">{marketData?.name || 'Ethereum'}</p>
        </div>

        <div className="card p-4">
          <h2 className="text-sm text-gray-500 uppercase mb-2">24h Change</h2>
          {loading ? (
            <div className="animate-pulse h-6 bg-gray-200 rounded w-24"></div>
          ) : (
            <p 
              className={`text-2xl font-bold ${
                (marketData?.price_change_24h || 0) >= 0 
                  ? 'text-green-600' 
                  : 'text-red-600'
              }`}
            >
              {marketData?.price_change_24h 
                ? `${marketData.price_change_24h > 0 ? '+' : ''}${marketData.price_change_24h.toFixed(2)}%` 
                : 'N/A'
              }
            </p>
          )}
          <p className="text-sm text-gray-500 mt-1">Last 24 hours</p>
        </div>

        <div className="card p-4">
          <h2 className="text-sm text-gray-500 uppercase mb-2">Market Cap</h2>
          {loading ? (
            <div className="animate-pulse h-6 bg-gray-200 rounded w-24"></div>
          ) : (
            <p className="text-2xl font-bold">
              ${marketData?.market_cap 
                ? (marketData.market_cap / 1000000000).toFixed(2) + 'B' 
                : 'N/A'
              }
            </p>
          )}
          <p className="text-sm text-gray-500 mt-1">USD</p>
        </div>

        <div className="card p-4">
          <h2 className="text-sm text-gray-500 uppercase mb-2">Fear & Greed Index</h2>
          {loading ? (
            <div className="animate-pulse h-6 bg-gray-200 rounded w-24"></div>
          ) : (
            <div className="flex items-end">
              <p className="text-2xl font-bold">{sentiment?.data[0]?.value || 'N/A'}</p>
              <p className="text-sm text-gray-500 ml-2 mb-1">/ 100</p>
            </div>
          )}
          <p className="text-sm mt-1">
            {sentiment?.data[0]?.value_classification || 'Unknown'}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="md:col-span-2">
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Recent News</h2>
            {loading ? (
              <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="animate-pulse">
                    <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                  </div>
                ))}
              </div>
            ) : news?.articles && news.articles.length > 0 ? (
              <div className="space-y-4">
                {news.articles.slice(0, 3).map((article, idx) => (
                  <div key={idx} className="border-b pb-4 last:border-b-0 last:pb-0">
                    <h3 className="font-medium mb-1">{article.title}</h3>
                    <p className="text-sm text-gray-500">{article.description}</p>
                    <div className="mt-2 flex justify-between text-xs text-gray-400">
                      <span>{article.source.name}</span>
                      <span>{new Date(article.publishedAt).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No recent news available</p>
            )}
          </div>
        </div>

        <div className="md:col-span-1">
          <AgentStatus />
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Transaction History</h2>
        {loading ? (
          <div className="animate-pulse space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-10 bg-gray-200 rounded"></div>
            ))}
          </div>
        ) : transactions.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left pb-3 font-medium text-gray-500">Action</th>
                  <th className="text-left pb-3 font-medium text-gray-500">Amount</th>
                  <th className="text-left pb-3 font-medium text-gray-500">Status</th>
                  <th className="text-left pb-3 font-medium text-gray-500">Time</th>
                </tr>
              </thead>
              <tbody>
                {transactions.map((tx, idx) => (
                  <tr key={idx} className="border-b last:border-b-0">
                    <td className="py-3">
                      {tx.message?.includes('SELL') || tx.message?.includes('ethusdc') 
                        ? 'SELL' 
                        : tx.message?.includes('BUY') || tx.message?.includes('usdceth')
                          ? 'BUY'
                          : 'TRADE'
                      }
                    </td>
                    <td className="py-3">{tx.amount || 'N/A'}</td>
                    <td className="py-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        tx.status === 'success' ? 'bg-green-100 text-green-800' :
                        tx.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {tx.status}
                      </span>
                    </td>
                    <td className="py-3 text-sm text-gray-500">
                      {tx.timestamp ? new Date(tx.timestamp * 1000).toLocaleString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-gray-500">No transactions found</p>
        )}
      </div>
    </MainLayout>
  );
} 