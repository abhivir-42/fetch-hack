# CryptoFund User Flow Specification

## 1. User Flow Diagram

```
┌─────────────────┐    ┌────────────────┐    ┌────────────────────┐    ┌────────────────┐
│                 │    │                │    │                    │    │                │
│  Authentication ├───►│ Wallet Connect ├───►│ Investment Strategy ├───►│   Execution   │
│                 │    │    & Topup     │    │   Configuration     │    │                │
└─────────────────┘    └────────────────┘    └────────────────────┘    └───────┬────────┘
                                                                               │
                         ┌────────────────────────────────────────────────────┘
                         ▼
┌─────────────────┐    ┌────────────────┐
│                 │    │                │
│ Results Display │◄───┤ Agent Activity │
│                 │    │                │
└─────────────────┘    └────────────────┘
```

## 2. Authentication Flow

### User Inputs
- Email address
- Password
- Optional: 2FA verification code

### Backend Operations
- Validate credentials against user database
- Generate JWT token for session management
- Log user activity

### Responses
- Success: Redirect to dashboard with token stored in localStorage
- Error: Display validation errors or authentication failures

### Error Handling
- Invalid credentials: Clear password field, display error message
- Network issues: Retry mechanism with exponential backoff
- Session timeout: Redirect to login with message

## 3. Wallet Connection & Topup Flow

### User Inputs
- Wallet connection confirmation (via MetaMask popup)
- Network selection (Ethereum/Bitcoin/Base/Polygon)
- Amount in USD for topup
- MetaMask private key (when required, entered in a secure input field)

### Security Handling for Private Keys
- Private key input masked by default
- Client-side encryption before transmission
- Keys never stored in plaintext
- Transmitted only over HTTPS with additional payload encryption
- Option to use hardware wallet instead

### Backend Operations
- Request wallet connection via browser wallet API
- `topup-agent` processes fund additions
- Verify transaction confirmation on blockchain

### Responses
- Connection success: Display wallet address and balance
- Topup initiated: Show transaction pending state
- Topup complete: Update balance and show confirmation

### Loading States
- Animated connection indicator during wallet API connection
- Progress bar for transaction confirmation
- Real-time balance updates via WebSocket

## 4. Investment Strategy Configuration

### User Inputs
- Investor type selection:
  * Long-term (HODLer)
  * Short-term (Trader)
  * Speculative (High-risk)

- Risk strategy selection:
  * Conservative (80% stable coins, 20% volatile)
  * Balanced (50% stable, 50% volatile)
  * Aggressive (20% stable, 80% volatile)
  * Speculative (100% high-risk assets)

- Network preference priority:
  * Primary network (Bitcoin/Ethereum/Base/Polygon)
  * Secondary network options

### Backend Operations
- Strategy parameters sent to `main-agent`
- `reason-agent` analyzes market conditions against strategy
- Portfolio allocation calculation based on risk preferences

### Responses
- Strategy confirmation screen with visual allocation breakdown
- Risk assessment summary with potential gain/loss scenarios
- Recommended asset allocation visualization

## 5. Execution Flow

### User Inputs
- Final confirmation of investment strategy
- Optional: Reasoning review for Buy/Sell/Hold actions
- Schedule settings (one-time or recurring investment)

### Backend Operations
- `main-agent` coordinates execution plan
- `swap-agent` handles token exchange operations
- `coin-agent` provides real-time price data
- `fgi-agent` provides market sentiment analysis

### Transaction Flow
1. User confirms execution
2. Funds moved from wallet to smart contract
3. Smart contract executes trades based on strategy
4. Confirmation transactions recorded on blockchain
5. User portfolio updated with new positions

### Loading States
- Multi-stage execution progress indicator
- Real-time transaction status updates
- Animated visualization of portfolio transformation

## 6. Results Visualization & Monitoring

### Display Components
- Portfolio composition pie chart
- Performance metrics (24h, 7d, 30d, YTD)
- Transaction history with status indicators
- Asset price charts with trend indicators

### Real-time Updates
- WebSocket connection for live price updates
- Push notifications for significant price movements
- Transaction status changes reflected immediately

### User Controls
- Manual refresh option
- Timeframe selection for performance metrics
- Export functionality for transaction history

## 7. Error Handling & Edge Cases

### Network Connectivity Issues
- Offline detection with automatic retry
- Background synchronization when connection restored
- Cache critical data for offline viewing

### Transaction Failures
- Detailed error messages with suggested resolutions
- Automatic refund process for failed transactions
- Manual retry option with adjusted gas fees

### Security Incidents
- Suspicious activity detection with immediate notification
- Account freeze option for suspected compromise
- Step-by-step recovery guidance

## 8. Agent Interaction Flow

```
┌─────────────┐     Market Data     ┌─────────────┐
│             │──────────────────►  │             │
│  User Input │                     │ Coin Agent  │
│             │ ◄─────────────────  │             │
└──────┬──────┘    Price Updates    └─────────────┘
       │
       ▼
┌─────────────┐     Strategy        ┌─────────────┐
│             │──────────────────►  │             │
│ Main Agent  │                     │ Reason Agent│
│             │ ◄─────────────────  │             │
└──────┬──────┘    Analysis         └─────────────┘
       │
       ▼
┌─────────────┐     Transaction     ┌─────────────┐
│             │──────────────────►  │             │
│ Swap Agent  │                     │ Topup Agent │
│             │ ◄─────────────────  │             │
└──────┬──────┘    Confirmation     └─────────────┘
       │
       ▼
┌─────────────┐
│             │
│ User Display│
│             │
└─────────────┘
```

## 9. Agent Responsibilities

### Main Agent
- Coordinates all agent activities
- Maintains user session state
- Triggers appropriate agent based on user input

### Coin Agent
- Fetches real-time cryptocurrency prices from CoinGecko
- Monitors price changes for user-selected assets
- Provides historical price data for analysis

### Reason Agent
- Analyzes market trends and sentiment
- Generates Buy/Sell/Hold recommendations
- Justifies recommendations with natural language reasoning

### Swap Agent
- Executes token exchanges across selected networks
- Optimizes for lowest fees and slippage
- Confirms successful transactions

### Topup Agent
- Handles wallet funding operations
- Verifies deposit confirmations
- Updates user balance after successful deposits

## 10. Complete User Journey Example

1. **User logs in** with email/password
2. **Dashboard loads** showing market overview with live Bitcoin price (currently $66,923.45)
3. **User connects MetaMask wallet** on Ethereum network
4. **User adds funds** - $1,000 via topup function
5. **User configures investment strategy**:
   - Investor type: Short-term trader
   - Risk strategy: Balanced (50/50)
   - Network: Primary Ethereum, Secondary Polygon
6. **System analyzes market** using Reason Agent:
   - Current Bitcoin Fear & Greed index: 65 (Greed)
   - ETH gas fees: 25 gwei (moderate)
   - Recent news sentiment: Positive
7. **System recommends portfolio**:
   - 40% ETH ($400)
   - 25% BTC ($250)
   - 20% SOL ($200)
   - 15% AVAX ($150)
8. **User reviews and confirms** strategy
9. **Execution begins**:
   - Swap Agent initiates transactions
   - Progress indicators show completion status
   - Transaction hashes displayed for verification
10. **Portfolio dashboard updates** with new positions
11. **Real-time monitoring begins** with 30-second refresh interval 