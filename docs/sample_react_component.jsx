import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Row, Col, Card, Badge, Button, Alert, Table } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const API_BASE_URL = 'http://localhost:5000/api';

// Custom hook for fetching data from the API
const useApiData = (endpoint, interval = 5000) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}${endpoint}`);
        setData(response.data);
        setError(null);
      } catch (err) {
        setError(err.message || 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const timer = setInterval(fetchData, interval);

    return () => clearInterval(timer);
  }, [endpoint, interval]);

  return { data, loading, error };
};

// Agent Status Component
const AgentStatus = () => {
  const { data: status, loading, error } = useApiData('/status', 10000);

  if (loading) return <p>Loading agent status...</p>;
  if (error) return <Alert variant="danger">Error: {error}</Alert>;

  return (
    <Card className="mb-4">
      <Card.Header>Agent Status</Card.Header>
      <Card.Body>
        <Row>
          {status && Object.entries(status).map(([agent, isRunning]) => (
            <Col key={agent} xs={6} md={4} className="mb-2">
              <Badge bg={isRunning ? 'success' : 'danger'} className="p-2 me-2">
                {agent.replace('_agent', '').replace('_', ' ')}
                {isRunning ? ' ✓' : ' ✗'}
              </Badge>
            </Col>
          ))}
        </Row>
      </Card.Body>
    </Card>
  );
};

// Market Data Component
const MarketData = () => {
  const { data, loading, error } = useApiData('/market-data', 30000);

  if (loading) return <p>Loading market data...</p>;
  if (error) return <Alert variant="danger">Error: {error}</Alert>;

  return (
    <Card className="mb-4">
      <Card.Header>Cryptocurrency Market Data</Card.Header>
      <Card.Body>
        {data && (
          <>
            <h3>{data.name} ({data.symbol})</h3>
            <Table striped bordered hover>
              <tbody>
                <tr>
                  <td>Current Price</td>
                  <td>${data.current_price.toLocaleString()}</td>
                </tr>
                <tr>
                  <td>Market Cap</td>
                  <td>${data.market_cap.toLocaleString()}</td>
                </tr>
                <tr>
                  <td>24h Volume</td>
                  <td>${data.total_volume.toLocaleString()}</td>
                </tr>
                <tr>
                  <td>24h Change</td>
                  <td className={data.price_change_24h >= 0 ? 'text-success' : 'text-danger'}>
                    {data.price_change_24h.toFixed(2)}%
                  </td>
                </tr>
              </tbody>
            </Table>
          </>
        )}
      </Card.Body>
    </Card>
  );
};

// Sentiment Analysis Component
const SentimentAnalysis = () => {
  const { data, loading, error } = useApiData('/sentiment-analysis', 60000);

  if (loading) return <p>Loading sentiment data...</p>;
  if (error) return <Alert variant="danger">Error: {error}</Alert>;

  const getFearGreedColor = (classification) => {
    switch (classification) {
      case 'Extreme Fear': return 'danger';
      case 'Fear': return 'warning';
      case 'Neutral': return 'info';
      case 'Greed': return 'primary';
      case 'Extreme Greed': return 'success';
      default: return 'secondary';
    }
  };

  return (
    <Card className="mb-4">
      <Card.Header>Market Sentiment</Card.Header>
      <Card.Body>
        {data && data.data && data.data.length > 0 && (
          <>
            <h3>Fear & Greed Index</h3>
            <div className="d-flex align-items-center mb-3">
              <div className="me-3">
                <Badge 
                  bg={getFearGreedColor(data.data[0].value_classification)} 
                  style={{ fontSize: '2rem', padding: '1rem' }}
                >
                  {data.data[0].value}
                </Badge>
              </div>
              <div>
                <h4>{data.data[0].value_classification}</h4>
                <p className="text-muted">
                  Updated: {new Date(parseInt(data.data[0].timestamp) * 1000).toLocaleString()}
                </p>
              </div>
            </div>
          </>
        )}
      </Card.Body>
    </Card>
  );
};

// Crypto News Component
const CryptoNews = () => {
  const { data, loading, error } = useApiData('/news', 300000);

  if (loading) return <p>Loading news...</p>;
  if (error) return <Alert variant="danger">Error: {error}</Alert>;

  return (
    <Card className="mb-4">
      <Card.Header>Latest Crypto News</Card.Header>
      <Card.Body>
        {data && data.articles && data.articles.map((article, index) => (
          <Card key={index} className="mb-3">
            {article.urlToImage && (
              <Card.Img 
                variant="top" 
                src={article.urlToImage} 
                style={{ maxHeight: '200px', objectFit: 'cover' }} 
              />
            )}
            <Card.Body>
              <Card.Title>{article.title}</Card.Title>
              <Card.Subtitle className="mb-2 text-muted">
                {article.source.name} • {new Date(article.publishedAt).toLocaleDateString()}
              </Card.Subtitle>
              <Card.Text>{article.description}</Card.Text>
              <Button 
                variant="outline-primary" 
                href={article.url} 
                target="_blank" 
                rel="noopener noreferrer"
              >
                Read More
              </Button>
            </Card.Body>
          </Card>
        ))}
      </Card.Body>
    </Card>
  );
};

// Trade Execution Component
const TradeExecutor = () => {
  const [action, setAction] = useState('SELL');
  const [amount, setAmount] = useState(0.1);
  const [status, setStatus] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const executeTrade = async () => {
    setIsLoading(true);
    setStatus(null);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/execute-trade`, { action, amount });
      setStatus({ type: 'success', message: response.data.message });
    } catch (error) {
      setStatus({ 
        type: 'danger', 
        message: error.response?.data?.message || 'Failed to execute trade' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="mb-4">
      <Card.Header>Execute Trade</Card.Header>
      <Card.Body>
        <div className="mb-3">
          <label htmlFor="action" className="form-label">Action</label>
          <select 
            id="action"
            className="form-select" 
            value={action} 
            onChange={(e) => setAction(e.target.value)}
          >
            <option value="BUY">BUY</option>
            <option value="SELL">SELL</option>
          </select>
        </div>
        
        <div className="mb-3">
          <label htmlFor="amount" className="form-label">Amount (ETH)</label>
          <input 
            id="amount"
            type="number" 
            className="form-control" 
            value={amount} 
            onChange={(e) => setAmount(parseFloat(e.target.value))}
            min="0.001"
            step="0.001"
          />
        </div>
        
        <Button 
          variant="primary" 
          onClick={executeTrade} 
          disabled={isLoading}
        >
          {isLoading ? 'Executing...' : 'Execute Trade'}
        </Button>
        
        {status && (
          <Alert variant={status.type} className="mt-3">
            {status.message}
          </Alert>
        )}
      </Card.Body>
    </Card>
  );
};

// Transaction History Component
const TransactionHistory = () => {
  const { data, loading, error } = useApiData('/transactions', 10000);

  if (loading) return <p>Loading transactions...</p>;
  if (error) return <Alert variant="danger">Error: {error}</Alert>;

  return (
    <Card className="mb-4">
      <Card.Header>Transaction History</Card.Header>
      <Card.Body>
        {data && data.length > 0 ? (
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Time</th>
                <th>Action</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {data.map((tx, index) => (
                <tr key={index}>
                  <td>{new Date(tx.timestamp * 1000).toLocaleString()}</td>
                  <td>{tx.message}</td>
                  <td>
                    <Badge bg={
                      tx.status === 'complete' ? 'success' : 
                      tx.status === 'pending' ? 'warning' : 'danger'
                    }>
                      {tx.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        ) : (
          <p>No transactions found</p>
        )}
      </Card.Body>
    </Card>
  );
};

// Agent Controller Component
const AgentController = () => {
  const [isStarting, setIsStarting] = useState(false);
  const [startResult, setStartResult] = useState(null);

  const startAllAgents = async () => {
    setIsStarting(true);
    setStartResult(null);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/start-all`);
      setStartResult({ type: 'success', message: response.data.message });
    } catch (error) {
      setStartResult({ 
        type: 'danger', 
        message: error.response?.data?.message || 'Failed to start agents' 
      });
    } finally {
      setIsStarting(false);
    }
  };

  return (
    <Card className="mb-4">
      <Card.Header>Agent Controller</Card.Header>
      <Card.Body>
        <Button 
          variant="success" 
          onClick={startAllAgents} 
          disabled={isStarting}
        >
          {isStarting ? 'Starting Agents...' : 'Start All Agents'}
        </Button>
        
        {startResult && (
          <Alert variant={startResult.type} className="mt-3">
            {startResult.message}
          </Alert>
        )}
      </Card.Body>
    </Card>
  );
};

// Main Dashboard Component
function Dashboard() {
  return (
    <Container fluid className="p-4">
      <h1 className="mb-4">CryptoReason Dashboard</h1>
      
      <Row>
        <Col>
          <AgentController />
        </Col>
      </Row>
      
      <Row>
        <Col>
          <AgentStatus />
        </Col>
      </Row>
      
      <Row>
        <Col md={6}>
          <MarketData />
        </Col>
        <Col md={6}>
          <SentimentAnalysis />
        </Col>
      </Row>
      
      <Row>
        <Col md={6}>
          <TradeExecutor />
        </Col>
        <Col md={6}>
          <TransactionHistory />
        </Col>
      </Row>
      
      <Row>
        <Col>
          <CryptoNews />
        </Col>
      </Row>
    </Container>
  );
}

export default Dashboard; 