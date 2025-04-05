"""
Shared message models for all CryptoFund agents.
"""
from typing import List, Optional
from uagents import Model


# Heartbeat monitoring models
class Heartbeat(Model):
    status: str


# Market data models
class CoinRequest(Model):
    blockchain: str


class CoinResponse(Model):
    name: str
    symbol: str
    current_price: float
    market_cap: float
    total_volume: float
    price_change_24h: float


# Crypto news models
class CryptonewsRequest(Model):
    limit: Optional[int] = 1


class CryptonewsResponse(Model):
    cryptoupdates: str


# Fear & Greed Index models
class FGIRequest(Model):
    limit: Optional[int] = 1


class FearGreedData(Model):
    value: float
    value_classification: str
    timestamp: str


class FGIResponse(Model):
    data: List[FearGreedData]
    status: str
    timestamp: str


# Decision making models
class ASI1Request(Model):
    query: str


class ASI1Response(Model):
    decision: str


# Transaction models
class SwaplandRequest(Model):
    blockchain: str
    signal: str
    amount: float
    private_key: str


class SwaplandResponse(Model):
    status: str


# Payment and reward models
class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str


class TransactionInfo(Model):
    tx_hash: str


class PaymentInquiry(Model):
    ready: str


class PaymentReceived(Model):
    status: str


class RewardRequest(Model):
    status: str


class SwapCompleted(Model):
    status: str
    message: str


# Wallet funding models
class TopupRequest(Model):
    amount: float


class TopupResponse(Model):
    status: str 