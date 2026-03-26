"""
Grid Trading Strategy
──────────────────────
Places buy orders below current price and sell orders above it at
evenly-spaced grid levels.  Profits from oscillation within the range.

Lifecycle:
1. On strategy start, compute grid levels around current price.
2. Place limit buy orders at each level below price.
3. When a buy fills, place a sell at the next grid level above it.
4. When a sell fills, place a buy at the next grid level below it.
5. Re-grid if price escapes the range by > 2 × spacing.
"""
import logging
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

from backend.strategies.base import BaseStrategy, Signal
from backend.indicators.technical import ohlcv_to_df, atr

log = logging.getLogger(__name__)


@dataclass
class GridLevel:
    price:      float
    side:       str        # "buy" | "sell"
    order_id:   str = ""
    filled:     bool = False


class GridTradingStrategy(BaseStrategy):
    name = "grid"

    def __init__(self, config: dict):
        super().__init__(config)
        self.pairs       = config.get("pairs",        ["BTC/USDT", "ETH/USDT"])
        self.capital_pct = config.get("capital_pct",  0.20)
        self.n_levels    = config.get("grid_levels",  10)
        self.spacing_pct = config.get("spacing_pct",  0.01)   # 1 % per level
        self.atr_mode    = config.get("atr_mode",     True)    # auto-space via ATR

        # { symbol: [GridLevel, ...] }
        self._grids: dict[str, list[GridLevel]] = {}
        self._anchor: dict[str, float] = {}   # price at which grid was initialised

    # ── main entry ────────────────────────────────────────────────────────────

    async def analyze(self, market_data: dict) -> list[Signal]:
        signals: list[Signal] = []
        for symbol, raw_ohlcv in market_data.items():
            if symbol not in self.pairs:
                continue
            if not raw_ohlcv or len(raw_ohlcv) < 20:
                continue
            try:
                sigs = self._evaluate(symbol, raw_ohlcv)
                signals.extend(sigs)
            except Exception as exc:
                log.error("[grid] %s error: %s", symbol, exc)
        return signals

    def mark_filled(self, symbol: str, order_id: str):
        """Engine calls this when an order is confirmed filled."""
        if symbol not in self._grids:
            return
        for level in self._grids[symbol]:
            if level.order_id == order_id:
                level.filled = True
                log.info("[grid] %s level %.4f %s filled", symbol, level.price, level.side)

    # ── per-symbol logic ──────────────────────────────────────────────────────

    def _evaluate(self, symbol: str, raw_ohlcv: list) -> list[Signal]:
        df    = ohlcv_to_df(raw_ohlcv)
        price = float(df["close"].iloc[-1])

        # First time or price escaped range → initialise grid
        if symbol not in self._grids or self._needs_regrid(symbol, price, df):
            return self._init_grid(symbol, price, df)

        # Check for filled levels that need a counter-order
        return self._check_fills(symbol, price)

    def _init_grid(self, symbol: str, price: float,
                   df: pd.DataFrame) -> list[Signal]:
        if self.atr_mode:
            atr_val = float(atr(df, 14).iloc[-1])
            spacing = atr_val * 0.5   # half an ATR per level
        else:
            spacing = price * self.spacing_pct

        levels: list[GridLevel] = []
        signals: list[Signal]   = []

        half = self.n_levels // 2
        # Buy levels below price
        for i in range(1, half + 1):
            lvl_price = price - i * spacing
            gl = GridLevel(price=lvl_price, side="buy")
            levels.append(gl)
            signals.append(self._grid_signal(symbol, "buy", lvl_price,
                                             is_grid_init=True))

        # Sell levels above price
        for i in range(1, half + 1):
            lvl_price = price + i * spacing
            gl = GridLevel(price=lvl_price, side="sell")
            levels.append(gl)
            signals.append(self._grid_signal(symbol, "sell", lvl_price,
                                             is_grid_init=True))

        self._grids[symbol]  = levels
        self._anchor[symbol] = price
        log.info("[grid] %s grid initialised @ %.4f  spacing=%.4f  levels=%d",
                 symbol, price, spacing, len(levels))
        return signals

    def _check_fills(self, symbol: str, price: float) -> list[Signal]:
        signals: list[Signal] = []
        grid = self._grids[symbol]
        spacing = abs(grid[1].price - grid[0].price) if len(grid) > 1 else 0

        for level in grid:
            if level.filled:
                # Buy filled → place sell one level up
                if level.side == "buy":
                    counter_price = level.price + spacing
                    signals.append(self._grid_signal(symbol, "sell", counter_price))
                # Sell filled → place buy one level down
                else:
                    counter_price = level.price - spacing
                    signals.append(self._grid_signal(symbol, "buy", counter_price))
                level.filled = False  # reset

        return signals

    def _needs_regrid(self, symbol: str, price: float,
                      df: pd.DataFrame) -> bool:
        anchor = self._anchor.get(symbol, price)
        grid   = self._grids.get(symbol, [])
        if not grid:
            return True
        atr_val = float(atr(df, 14).iloc[-1]) if self.atr_mode else anchor * self.spacing_pct
        deviation = abs(price - anchor)
        return deviation > 2 * self.n_levels // 2 * atr_val * 0.5

    def _grid_signal(self, symbol: str, side: str, price: float,
                     is_grid_init: bool = False) -> Signal:
        # Amount per grid level = total capital / number of levels
        amount = self.capital_pct / self.n_levels
        return Signal(
            symbol     = symbol,
            side       = side,
            strategy   = self.name,
            confidence = 0.85 if is_grid_init else 0.90,
            price      = price,
            amount     = amount,
            leverage   = 1,
            meta       = {"order_type": "limit",
                          "grid_price": price,
                          "is_init":    is_grid_init},
        )
