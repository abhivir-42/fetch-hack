from uagents import Model
from typing import List, Optional, Dict

# --- Sentiment Agent Models ---

class FGIRequest(Model):
    # No parameters needed for the latest FGI
    pass

class FearGreedData(Model):
    value: float
    value_classification: str
    timestamp: str # ISO Format timestamp string

class FGIResponse(Model):
    success: bool
    data: Optional[FearGreedData] = None # Only one data point for the latest FGI
    error: Optional[str] = None

# --- Market Data Agent Models ---

class MarketDataRequest(Model):
    # CoinGecko IDs (e.g., 'bitcoin', 'ethereum')
    coin_ids: List[str]

class CoinData(Model):
    id: str # CoinGecko ID
    symbol: str
    name: str
    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    total_volume: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None

class MarketDataResponse(Model):
    success: bool
    # Dictionary mapping coin_id to its data
    data: Optional[Dict[str, CoinData]] = None
    error: Optional[str] = None

# --- General Error Model ---

class ErrorResponse(Model):
    error: str 