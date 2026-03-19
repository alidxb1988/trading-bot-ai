"""
Gomale Backtesting Engine
──────────────────────────
Runs a pure-Python simulation of the Gomale strategy against synthetic
historical OHLCV data.  No live exchange connection is required.

The price model mirrors the React dashboard's generateHistoricalData():
  • SOL: startPrice=100, volatility=5 %, dailyTrend=+0.15 %
  • ETH: startPrice=2000, volatility=4 %, dailyTrend=+0.10 %

Usage:
    from backend.backtesting.engine import run_backtest
    result = run_backtest("SOL", config)
    result = run_backtest("ETH", config)
"""
import math
import random
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


# ── Data structures ────────────────────────────────────────────────────────────

@dataclass
class TradeRecord:
    date:       str
    type:       str      # "BUY" | "SELL"
    price:      float
    size:       float
    pnl:        float    # % profit/loss of the closed trade (0 for BUY entries)
    confidence: int


@dataclass
class EquityPoint:
    date:     str
    equity:   float
    buy_hold: float


@dataclass
class MonthlyReturn:
    month:  str
    ret:    float        # percentage


@dataclass
class BacktestMetrics:
    final_balance:  float
    total_return:   float     # %
    win_rate:       float     # %
    wins:           int
    losses:         int
    total_trades:   int
    avg_win:        float     # %
    avg_loss:       float     # %
    profit_factor:  float
    max_drawdown:   float     # %
    sharpe_ratio:   float


@dataclass
class BacktestResult:
    metrics:        BacktestMetrics
    equity_curve:   list[EquityPoint]
    trades:         list[TradeRecord]
    monthly_returns: list[MonthlyReturn]


# ── Synthetic OHLCV generator ──────────────────────────────────────────────────

_SYMBOL_PARAMS = {
    "SOL": {"start_price": 100.0,  "volatility": 0.05, "trend": 0.0015},
    "ETH": {"start_price": 2000.0, "volatility": 0.04, "trend": 0.0010},
}

_TIMEFRAME_MONTHS = {
    "1month":  1,
    "3months": 3,
    "6months": 6,
    "1year":   12,
}


def _generate_historical_data(symbol: str, months: int) -> list[dict]:
    params = _SYMBOL_PARAMS.get(symbol, _SYMBOL_PARAMS["SOL"])
    start_price = params["start_price"]
    volatility  = params["volatility"]
    trend       = params["trend"]

    days  = months * 30
    price = start_price
    today = date.today()
    data  = []

    for i in range(days):
        daily_change = (random.random() - 0.48) * volatility + trend
        price = price * (1 + daily_change)

        day_date = today - timedelta(days=days - i)
        data.append({
            "date":      day_date.isoformat(),
            "open":      price * (1 + (random.random() - 0.5) * 0.02),
            "high":      price * (1 + random.random() * 0.03),
            "low":       price * (1 - random.random() * 0.03),
            "close":     price,
            "volume":    1_000_000 + random.random() * 5_000_000,
            "rsi":       30 + random.random() * 40,
            "sentiment": 40 + random.random() * 30,
            "macd":      (random.random() - 0.5) * 100,
            "adx":       20 + random.random() * 40,
        })

    return data


# ── Signal logic (mirrors GomaleStrategy._get_decision) ───────────────────────

def _get_decision(rsi_val: float, macd_val: float, adx_val: float,
                  sentiment: float, has_position: bool) -> tuple[str, float]:
    if rsi_val < 30 and sentiment > 60 and adx_val > 30:
        return "BUY", 85 + random.random() * 10
    if rsi_val < 35 and sentiment > 50 and macd_val > 0:
        return "BUY", 75 + random.random() * 20
    if rsi_val < 45 and sentiment > 55 and macd_val > 20:
        return "BUY", 65 + random.random() * 15
    if rsi_val > 70 and sentiment < 40:
        return "SELL", 80 + random.random() * 15
    if rsi_val > 65 and has_position:
        return "SELL", 70 + random.random() * 20
    return "HOLD", 50.0


# ── Main backtest runner ───────────────────────────────────────────────────────

def run_backtest(symbol: str, config: dict) -> BacktestResult:
    """
    config keys (all optional):
        starting_capital  float  default 1000
        timeframe         str    default "6months"
        risk_per_trade    float  default 10  (percent)
        confidence_gate   float  default 70  (percent)
    """
    starting_capital = float(config.get("starting_capital", 1000))
    timeframe        = config.get("timeframe", "6months")
    risk_pct         = float(config.get("risk_per_trade", 10)) / 100
    confidence_gate  = float(config.get("confidence_gate", 70))

    months = _TIMEFRAME_MONTHS.get(timeframe, 6)
    data   = _generate_historical_data(symbol, months)

    balance      = starting_capital
    position: Optional[dict] = None
    trades: list[TradeRecord]  = []
    equity_curve: list[EquityPoint] = []
    max_balance  = starting_capital
    max_drawdown = 0.0
    winning_pcts: list[float] = []
    losing_pcts:  list[float] = []

    reference_price = data[20]["close"] if len(data) > 20 else data[0]["close"]

    for i in range(20, len(data)):
        bar  = data[i]
        price = bar["close"]

        signal, confidence = _get_decision(
            bar["rsi"], bar["macd"], bar["adx"], bar["sentiment"],
            has_position=position is not None,
        )

        if signal == "BUY" and position is None and confidence >= confidence_gate:
            risk_amount = balance * risk_pct
            size        = risk_amount / price
            balance    -= risk_amount
            position    = {"entry_price": price, "size": size, "date": bar["date"]}
            trades.append(TradeRecord(
                date=bar["date"], type="BUY", price=price,
                size=size, pnl=0.0, confidence=int(confidence),
            ))

        elif signal == "SELL" and position is not None:
            exit_value  = position["size"] * price
            entry_value = position["size"] * position["entry_price"]
            pnl_pct     = (exit_value - entry_value) / entry_value * 100
            balance    += exit_value
            (winning_pcts if pnl_pct > 0 else losing_pcts).append(pnl_pct)
            trades.append(TradeRecord(
                date=bar["date"], type="SELL", price=price,
                size=position["size"], pnl=round(pnl_pct, 4),
                confidence=int(confidence),
            ))
            position = None

        # Equity snapshot
        current_equity = balance + (position["size"] * price if position else 0)
        if current_equity > max_balance:
            max_balance = current_equity
        drawdown = (max_balance - current_equity) / max_balance * 100
        if drawdown > max_drawdown:
            max_drawdown = drawdown

        buy_hold = starting_capital * (price / reference_price)
        equity_curve.append(EquityPoint(
            date=bar["date"],
            equity=round(current_equity, 4),
            buy_hold=round(buy_hold, 4),
        ))

    # Close any residual open position at the last price
    if position:
        final_price = data[-1]["close"]
        balance += position["size"] * final_price

    # ── Metrics ───────────────────────────────────────────────────────────────
    total_return = (balance - starting_capital) / starting_capital * 100
    wins         = len(winning_pcts)
    losses       = len(losing_pcts)
    total_trades = len(trades)
    win_rate     = wins / (wins + losses) * 100 if (wins + losses) > 0 else 0.0
    avg_win      = sum(winning_pcts) / wins if wins > 0 else 0.0
    avg_loss     = sum(losing_pcts) / losses if losses > 0 else 0.0
    gross_profit = sum(abs(p) for p in winning_pcts)
    gross_loss   = sum(abs(p) for p in losing_pcts)
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else gross_profit

    # Simplified Sharpe (annualised, daily equity returns)
    daily_returns = [
        (equity_curve[i].equity - equity_curve[i - 1].equity) / equity_curve[i - 1].equity
        for i in range(1, len(equity_curve))
        if equity_curve[i - 1].equity > 0
    ]
    sharpe = 0.0
    if daily_returns:
        avg_r = sum(daily_returns) / len(daily_returns)
        std_r = math.sqrt(sum((r - avg_r) ** 2 for r in daily_returns) / len(daily_returns))
        sharpe = (avg_r / std_r * math.sqrt(252)) if std_r > 0 else 0.0

    # ── Monthly returns ────────────────────────────────────────────────────────
    monthly_returns: list[MonthlyReturn] = []
    month_buckets: dict[str, list[float]] = {}
    for point in equity_curve:
        month = point.date[:7]
        month_buckets.setdefault(month, []).append(point.equity)

    months_sorted = sorted(month_buckets.keys())
    prev_eq = starting_capital
    for m in months_sorted:
        equities = month_buckets[m]
        end_eq   = equities[-1]
        ret      = (end_eq - prev_eq) / prev_eq * 100 if prev_eq > 0 else 0.0
        monthly_returns.append(MonthlyReturn(month=m, ret=round(ret, 2)))
        prev_eq = end_eq

    metrics = BacktestMetrics(
        final_balance  = round(balance, 2),
        total_return   = round(total_return, 2),
        win_rate       = round(win_rate, 2),
        wins           = wins,
        losses         = losses,
        total_trades   = total_trades,
        avg_win        = round(avg_win, 2),
        avg_loss       = round(avg_loss, 2),
        profit_factor  = round(profit_factor, 2),
        max_drawdown   = round(max_drawdown, 2),
        sharpe_ratio   = round(sharpe, 2),
    )

    return BacktestResult(
        metrics         = metrics,
        equity_curve    = equity_curve,
        trades          = trades,
        monthly_returns = monthly_returns,
    )
