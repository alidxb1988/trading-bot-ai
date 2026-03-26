"""
Abstract base class for all trading strategies.
"""
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

log = logging.getLogger(__name__)


@dataclass
class Signal:
    """A trading signal emitted by a strategy."""
    symbol:      str
    side:        str              # "buy" | "sell" | "close"
    strategy:    str
    confidence:  float            # 0.0 – 1.0
    price:       float
    amount:      float            # quote amount (USDT) to use
    leverage:    int   = 1
    stop_loss:   Optional[float] = None
    take_profit: Optional[float] = None
    meta:        dict  = field(default_factory=dict)
    timestamp:   datetime = field(default_factory=datetime.utcnow)

    @property
    def is_valid(self) -> bool:
        return (
            self.symbol
            and self.side in ("buy", "sell", "close")
            and 0.0 <= self.confidence <= 1.0
            and self.price > 0
            and self.amount > 0
        )


class BaseStrategy(ABC):
    """
    Subclasses must implement `analyze()` which receives a dict of
    {symbol: DataFrame} and returns a list of Signals.
    """

    name: str = "base"

    def __init__(self, config: dict):
        self.config = config
        self.enabled: bool = config.get("enabled", True)
        self.open_positions: dict[str, dict] = {}   # symbol -> position info

    @abstractmethod
    async def analyze(self, market_data: dict) -> list[Signal]:
        """
        Analyse market data and return zero or more trading signals.
        market_data: { "BTC/USDT": DataFrame, ... }
        """

    def log(self, msg: str, *args, level: str = "info"):
        getattr(log, level)(f"[{self.name}] {msg}", *args)
