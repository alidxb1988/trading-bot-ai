"""
Central configuration management for the trading bot.
Reads from environment variables / .env file.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────────────────────────
    APP_NAME: str = "Trading Bot AI"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SECRET_KEY: str = Field(default="changeme-use-a-real-secret", env="SECRET_KEY")

    # ── Database ─────────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./trading_bot.db"

    # ── Exchange API Keys ─────────────────────────────────────────────────────
    BYBIT_API_KEY: Optional[str] = None
    BYBIT_API_SECRET: Optional[str] = None
    BYBIT_TESTNET: bool = True

    BINANCE_API_KEY: Optional[str] = None
    BINANCE_API_SECRET: Optional[str] = None
    BINANCE_TESTNET: bool = True

    KUCOIN_API_KEY: Optional[str] = None
    KUCOIN_API_SECRET: Optional[str] = None
    KUCOIN_API_PASSPHRASE: Optional[str] = None

    OKX_API_KEY: Optional[str] = None
    OKX_API_SECRET: Optional[str] = None
    OKX_API_PASSPHRASE: Optional[str] = None

    # ── Active exchange ───────────────────────────────────────────────────────
    ACTIVE_EXCHANGE: str = "bybit"   # bybit | binance | kucoin | okx

    # ── Trading defaults ──────────────────────────────────────────────────────
    TRADING_MODE: str = "paper"      # paper | live
    BASE_CURRENCY: str = "USDT"
    MAX_OPEN_TRADES: int = 5
    RISK_PER_TRADE: float = 0.02     # 2 % of available balance
    DEFAULT_LEVERAGE: int = 5
    STOP_LOSS_PCT: float = 0.05      # 5 %
    TAKE_PROFIT_PCT: float = 0.10    # 10 %

    # ── Strategy toggles ──────────────────────────────────────────────────────
    ENABLE_HFT: bool = True
    ENABLE_AI_MULTI: bool = True
    ENABLE_ZERO_LOSS: bool = True
    ENABLE_GRID: bool = False
    ENABLE_GOMALE: bool = True

    # ── HFT / Scalping ────────────────────────────────────────────────────────
    HFT_TIMEFRAME: str = "3m"
    HFT_PAIRS: list[str] = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT"]
    HFT_CAPITAL_PCT: float = 0.40
    HFT_LEVERAGE: int = 5
    HFT_MICRO_ORDERS: int = 3
    HFT_PROFIT_TRANSFER: float = 0.30   # move 30 % of profit to reserve

    # ── AI Multi-Strategy ─────────────────────────────────────────────────────
    AI_TIMEFRAME: str = "15m"
    AI_PAIRS: list[str] = ["BTC/USDT", "ETH/USDT", "ADA/USDT", "XRP/USDT", "DOT/USDT"]
    AI_CAPITAL_PCT: float = 0.35
    AI_LEVERAGE: int = 3
    AI_CONFIDENCE_THRESHOLD: float = 0.75
    AI_AUTO_REINVEST: bool = True

    # ── Zero-Loss / DCA ───────────────────────────────────────────────────────
    DCA_TIMEFRAME: str = "1h"
    DCA_PAIRS: list[str] = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"]
    DCA_CAPITAL_PCT: float = 0.25
    DCA_DIP_THRESHOLD: float = 0.12     # buy on 12 % dip
    DCA_PROFIT_TARGET: float = 0.15     # exit at 15 % profit
    DCA_XAUT_PAIRS: list[str] = ["XAUT/USDT"]
    DCA_XAUT_DIP_THRESHOLD: float = 0.08

    # ── Gomale Trading ────────────────────────────────────────────────────────
    GOMALE_TIMEFRAME: str = "15m"
    GOMALE_PAIRS: list[str] = ["SOL/USDT", "ETH/USDT"]
    GOMALE_CAPITAL_PCT: float = 0.25
    GOMALE_LEVERAGE: int = 2
    GOMALE_CONFIDENCE_THRESHOLD: float = 0.70
    GOMALE_RISK_PER_TRADE: float = 0.10   # 10 % of capital per trade

    # ── Grid Trading ─────────────────────────────────────────────────────────
    GRID_PAIRS: list[str] = ["BTC/USDT", "ETH/USDT"]
    GRID_CAPITAL_PCT: float = 0.20
    GRID_LEVELS: int = 10
    GRID_SPACING_PCT: float = 0.01      # 1 % between grid levels

    # ── Risk management ───────────────────────────────────────────────────────
    MAX_DRAWDOWN_PCT: float = 0.20      # halt bot if portfolio drops 20 %
    MAX_DAILY_LOSS_PCT: float = 0.05    # halt bot if daily loss exceeds 5 %
    MAX_POSITION_SIZE_PCT: float = 0.10 # no single position > 10 % of portfolio

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
