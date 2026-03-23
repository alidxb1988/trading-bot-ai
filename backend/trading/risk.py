"""
Risk Management
────────────────
• Per-trade position sizing (Kelly-fraction / fixed-risk)
• Portfolio-level drawdown & daily-loss circuit-breakers
• Max single-position size cap
• Exposure limits per strategy
"""
import logging
from datetime import datetime, date
from typing import Optional

log = logging.getLogger(__name__)


class RiskManager:
    def __init__(self, settings):
        self.settings = settings

        # Running totals (reset externally via reset_daily())
        self.daily_pnl:       float          = 0.0
        self.daily_pnl_date:  date           = date.today()
        self.peak_equity:     float          = 0.0
        self._day_open_equity: Optional[float] = None   # equity at start of trading day
        self._prev_equity:     Optional[float] = None   # equity at previous tick

    # ── circuit breakers ──────────────────────────────────────────────────────

    def check_daily_loss(self, current_equity: float) -> bool:
        """Return True if daily loss limit is breached (bot should halt)."""
        self._auto_reset_daily(current_equity)
        if self._day_open_equity is None or self._day_open_equity == 0:
            return False
        daily_loss_pct = (self._day_open_equity - current_equity) / self._day_open_equity
        if daily_loss_pct >= self.settings.MAX_DAILY_LOSS_PCT:
            log.warning("RISK: daily loss limit %.1f%% breached", daily_loss_pct * 100)
            return True
        return False

    def check_max_drawdown(self, current_equity: float) -> bool:
        """Return True if maximum drawdown from peak is breached."""
        if self.peak_equity <= 0:
            self.peak_equity = current_equity
            return False
        drawdown = (self.peak_equity - current_equity) / self.peak_equity
        if drawdown >= self.settings.MAX_DRAWDOWN_PCT:
            log.warning("RISK: max drawdown %.1f%% breached", drawdown * 100)
            return True
        return False

    def update_equity(self, equity: float):
        """
        Call after each tick to:
        - Keep peak_equity up to date.
        - Accumulate daily_pnl as the sum of tick-to-tick equity deltas.
        """
        # Update all-time peak
        if equity > self.peak_equity:
            self.peak_equity = equity

        # Accumulate daily PnL as sum of tick deltas (not relative to peak)
        if self._prev_equity is not None:
            self.daily_pnl += equity - self._prev_equity

        self._prev_equity = equity

    # ── position sizing ───────────────────────────────────────────────────────

    def position_size_usdt(self, signal_amount_fraction: float,
                           available_usdt: float,
                           price: float,
                           atr: float = 0.0,
                           leverage: int = 1) -> float:
        """
        Compute the USDT order size for a signal.

        signal_amount_fraction: the fraction of available capital the strategy
                                 wants to use (e.g. 0.40 for HFT).
        """
        # Cap fraction at 1.0 to prevent oversized orders from DCA accumulation
        fraction = min(signal_amount_fraction, 1.0)
        raw_usdt = available_usdt * fraction

        # Cap at MAX_POSITION_SIZE_PCT of total available equity (with leverage)
        max_usdt = available_usdt * self.settings.MAX_POSITION_SIZE_PCT * leverage

        size_usdt = min(raw_usdt, max_usdt)

        # Minimum order floor (most exchanges require ≥ 5 USDT)
        size_usdt = max(size_usdt, 5.0)

        log.debug("position_size: %.2f USDT (raw=%.2f, cap=%.2f)",
                  size_usdt, raw_usdt, max_usdt)
        return round(size_usdt, 2)

    def compute_quantity(self, usdt_amount: float, price: float,
                         leverage: int = 1) -> float:
        """Convert USDT notional to asset quantity."""
        if price <= 0:
            return 0.0
        return round((usdt_amount * leverage) / price, 8)

    # ── helpers ───────────────────────────────────────────────────────────────

    def record_trade_pnl(self, pnl: float):
        self._auto_reset_daily()
        self.daily_pnl += pnl

    def _auto_reset_daily(self, current_equity: Optional[float] = None):
        today = date.today()
        if self.daily_pnl_date != today:
            self.daily_pnl       = 0.0
            self.daily_pnl_date  = today
            # Reset the day-open reference so daily loss check is fresh
            self._day_open_equity = current_equity
            self._prev_equity     = current_equity
            log.info("RISK: daily PnL reset for %s", today)
        elif self._day_open_equity is None and current_equity is not None:
            self._day_open_equity = current_equity

    def stats(self) -> dict:
        return {
            "daily_pnl":   round(self.daily_pnl, 4),
            "peak_equity": round(self.peak_equity, 4),
        }
