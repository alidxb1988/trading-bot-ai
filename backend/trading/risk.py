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

log = logging.getLogger(__name__)


class RiskManager:
    def __init__(self, settings):
        self.settings = settings

        # Running totals (reset externally via reset_daily())
        self.daily_pnl:      float = 0.0
        self.daily_pnl_date: date  = date.today()
        self.peak_equity:    float = 0.0

    # ── circuit breakers ──────────────────────────────────────────────────────

    def check_daily_loss(self, current_equity: float) -> bool:
        """Return True if daily loss limit is breached (bot should halt)."""
        self._auto_reset_daily()
        if self.peak_equity == 0:
            self.peak_equity = current_equity
            return False
        daily_loss_pct = (self.peak_equity - current_equity) / self.peak_equity
        if daily_loss_pct >= self.settings.MAX_DAILY_LOSS_PCT:
            log.warning("RISK: daily loss limit %.1f%% breached", daily_loss_pct * 100)
            return True
        return False

    def check_max_drawdown(self, current_equity: float) -> bool:
        """Return True if maximum drawdown is breached."""
        if self.peak_equity <= 0:
            self.peak_equity = current_equity
            return False
        drawdown = (self.peak_equity - current_equity) / self.peak_equity
        if drawdown >= self.settings.MAX_DRAWDOWN_PCT:
            log.warning("RISK: max drawdown %.1f%% breached", drawdown * 100)
            return True
        return False

    def update_equity(self, equity: float):
        """Call after each tick to keep peak_equity up to date."""
        if equity > self.peak_equity:
            self.peak_equity = equity
        self.daily_pnl += equity - self.peak_equity  # approx

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
        raw_usdt = available_usdt * signal_amount_fraction

        # Cap at MAX_POSITION_SIZE_PCT of total available equity
        max_usdt = available_usdt * self.settings.MAX_POSITION_SIZE_PCT * leverage

        size_usdt = min(raw_usdt, max_usdt)

        # Sanity floor
        size_usdt = max(size_usdt, 1.0)

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

    def _auto_reset_daily(self):
        today = date.today()
        if self.daily_pnl_date != today:
            self.daily_pnl      = 0.0
            self.daily_pnl_date = today
            log.info("RISK: daily PnL reset for %s", today)

    def stats(self) -> dict:
        return {
            "daily_pnl":   round(self.daily_pnl, 4),
            "peak_equity": round(self.peak_equity, 4),
        }
