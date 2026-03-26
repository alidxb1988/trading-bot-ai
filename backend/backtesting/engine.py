"""
Gomale Backtesting Engine
──────────────────────────
Runs a pure-Python simulation of the Gomale strategy against synthetic
historical OHLCV data.  No live exchange connection is required.

Multi-source signal weighting:
  • Technical (RSI / MACD / ADX)  → 40 %
  • News / Perplexity sentiment    → 30 %
  • Polymarket prediction odds     → 30 %

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
    date:                 str
    type:                 str      # "BUY" | "SELL"
    price:                float
    size:                 float
    pnl:                  float    # % profit/loss of the closed trade (0 for BUY entries)
    confidence:           int      # composite confidence %
    claude_confidence:    int      # technical-only confidence %
    news_sentiment:       float    # 0-100 — news/perplexity score
    polymarket_sentiment: float    # 0-100 — prediction market probability
    polymarket_score:     float    # 0-100 — weighted polymarket contribution
    signal_source:        str      # "technical" | "news" | "polymarket" | "combined"


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
    final_balance:     float
    total_return:      float     # %
    win_rate:          float     # %
    wins:              int
    losses:            int
    total_trades:      int
    avg_win:           float     # %
    avg_loss:          float     # %
    profit_factor:     float
    max_drawdown:      float     # %
    sharpe_ratio:      float
    polymarket_trades: int       # trades where polymarket signal was dominant


@dataclass
class BacktestResult:
    metrics:          BacktestMetrics
    equity_curve:     list[EquityPoint]
    trades:           list[TradeRecord]
    monthly_returns:  list[MonthlyReturn]
    signal_breakdown: list[dict]   # [{source, count, pct}]


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

# Baseline Polymarket priors per symbol (bullish probability)
_POLYMARKET_BASE = {"SOL": 0.62, "ETH": 0.58}


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


# ── Sentiment helpers ──────────────────────────────────────────────────────────

def _get_news_sentiment(symbol: str, use_news: bool) -> dict:
    """
    Simulate Perplexity/news sentiment for a symbol.
    Returns score (0-100) and a headline snippet.
    """
    if not use_news:
        return {"score": 50.0, "active": False, "headline": "News disabled"}

    score = 35 + random.random() * 40        # 35-75 range
    bullish = score > 55
    headlines = {
        "SOL": [
            "Solana DeFi TVL hits all-time high amid developer activity",
            "SOL ecosystem sees surge in NFT minting volumes",
            "Solana validators report network stability improvements",
            "SOL price faces resistance at key technical level",
        ],
        "ETH": [
            "Ethereum staking ratio continues steady climb post-Merge",
            "ETH L2 rollup activity breaks weekly record",
            "Ethereum spot ETF inflows accelerate through Q1",
            "ETH gas fees spike as mempool congestion rises",
        ],
    }
    pool = headlines.get(symbol, headlines["SOL"])
    headline = pool[int(random.random() * len(pool))]
    return {"score": round(score, 1), "active": True, "headline": headline,
            "bullish": bullish}


def _get_polymarket_sentiment(symbol: str, use_polymarket: bool) -> dict:
    """
    Simulate Polymarket prediction-market odds for a symbol.
    Returns probability (0-100) of bullish outcome.
    """
    if not use_polymarket:
        return {"probability": 50.0, "active": False, "market": "Polymarket disabled",
                "yes_price": 0.50, "no_price": 0.50, "volume": 0}

    base = _POLYMARKET_BASE.get(symbol, 0.55)
    # Walk the probability slightly each call to simulate market movement
    prob = max(0.20, min(0.90, base + (random.random() - 0.48) * 0.15))
    markets = {
        "SOL": "Will SOL reach $150 by end of quarter?",
        "ETH": "Will ETH outperform BTC over the next 30 days?",
    }
    volume = int(50_000 + random.random() * 200_000)
    return {
        "probability": round(prob * 100, 1),
        "active": True,
        "market": markets.get(symbol, f"{symbol} price prediction"),
        "yes_price": round(prob, 3),
        "no_price":  round(1 - prob, 3),
        "volume":    volume,
    }


# ── Multi-source signal logic ─────────────────────────────────────────────────

def _get_decision(
    rsi_val: float, macd_val: float, adx_val: float,
    sentiment: float, has_position: bool,
    news: dict, poly: dict,
    use_claude: bool, use_news: bool, use_polymarket: bool,
) -> tuple[str, float, float, float, float, str]:
    """
    Returns (action, composite_confidence, claude_conf, news_score, poly_score, source).
    Weights: technical 40%, news 30%, polymarket 30%.
    """
    # ── Technical signal (Gomale 5-tier) ─────────────────────────────────────
    if use_claude:
        if rsi_val < 30 and sentiment > 60 and adx_val > 30:
            tech_action, tech_conf = "BUY",  85 + random.random() * 10
        elif rsi_val < 35 and sentiment > 50 and macd_val > 0:
            tech_action, tech_conf = "BUY",  75 + random.random() * 20
        elif rsi_val < 45 and sentiment > 55 and macd_val > 20:
            tech_action, tech_conf = "BUY",  65 + random.random() * 15
        elif rsi_val > 70 and sentiment < 40:
            tech_action, tech_conf = "SELL", 80 + random.random() * 15
        elif rsi_val > 65 and has_position:
            tech_action, tech_conf = "SELL", 70 + random.random() * 20
        else:
            tech_action, tech_conf = "HOLD", 50.0
    else:
        tech_action, tech_conf = "HOLD", 50.0

    # ── News signal ──────────────────────────────────────────────────────────
    news_score = news.get("score", 50.0)
    if use_news and news.get("active"):
        if news_score >= 65:
            news_action = "BUY"
        elif news_score <= 38:
            news_action = "SELL"
        else:
            news_action = "HOLD"
    else:
        news_action, news_score = "HOLD", 50.0

    # ── Polymarket signal ─────────────────────────────────────────────────────
    poly_prob = poly.get("probability", 50.0)
    if use_polymarket and poly.get("active"):
        if poly_prob >= 65:
            poly_action = "BUY"
        elif poly_prob <= 38:
            poly_action = "SELL"
        else:
            poly_action = "HOLD"
        poly_score = poly_prob
    else:
        poly_action, poly_score = "HOLD", 50.0

    # ── Weighted composite ────────────────────────────────────────────────────
    # Convert to numeric: BUY=+1, HOLD=0, SELL=-1
    def _to_num(action): return 1 if action == "BUY" else (-1 if action == "SELL" else 0)

    w_tech = 0.40 if use_claude      else 0.0
    w_news = 0.30 if use_news        else 0.0
    w_poly = 0.30 if use_polymarket  else 0.0
    total_w = w_tech + w_news + w_poly or 1.0  # avoid /0

    composite = (
        _to_num(tech_action) * w_tech +
        _to_num(news_action) * w_news +
        _to_num(poly_action) * w_poly
    ) / total_w

    if composite > 0.2:
        final_action = "BUY"
    elif composite < -0.2:
        final_action = "SELL"
    else:
        final_action = "HOLD"

    # ── Dominant source ───────────────────────────────────────────────────────
    contributions = {
        "technical":  abs(_to_num(tech_action)) * w_tech,
        "news":       abs(_to_num(news_action)) * w_news,
        "polymarket": abs(_to_num(poly_action)) * w_poly,
    }
    dominant = max(contributions, key=contributions.get)
    if all(v == 0 for v in contributions.values()):
        dominant = "technical"

    # Composite confidence: weighted blend of individual confidences
    comp_conf = (
        tech_conf * w_tech / total_w +
        news_score * w_news / total_w +
        poly_score * w_poly / total_w
    )

    return final_action, round(comp_conf, 1), round(tech_conf, 1), round(news_score, 1), round(poly_score, 1), dominant


# ── Main backtest runner ───────────────────────────────────────────────────────

def run_backtest(symbol: str, config: dict) -> BacktestResult:
    """
    config keys (all optional):
        starting_capital  float  default 1000
        timeframe         str    default "6months"
        risk_per_trade    float  default 10  (percent)
        confidence_gate   float  default 70  (percent)
        use_claude        bool   default True
        use_news          bool   default True
        use_polymarket    bool   default True
    """
    starting_capital = float(config.get("starting_capital", 1000))
    timeframe        = config.get("timeframe", "6months")
    risk_pct         = float(config.get("risk_per_trade", 10)) / 100
    confidence_gate  = float(config.get("confidence_gate", 70))
    use_claude       = bool(config.get("use_claude", True))
    use_news         = bool(config.get("use_news", True))
    use_polymarket   = bool(config.get("use_polymarket", True))

    months = _TIMEFRAME_MONTHS.get(timeframe, 6)
    data   = _generate_historical_data(symbol, months)

    balance      = starting_capital
    position: Optional[dict] = None
    trades: list[TradeRecord]    = []
    equity_curve: list[EquityPoint] = []
    max_balance  = starting_capital
    max_drawdown = 0.0
    winning_pcts: list[float] = []
    losing_pcts:  list[float] = []

    # Signal source tracking
    source_counts: dict[str, int] = {"technical": 0, "news": 0, "polymarket": 0, "combined": 0}
    polymarket_trade_count = 0

    reference_price = data[20]["close"] if len(data) > 20 else data[0]["close"]

    for i in range(20, len(data)):
        bar   = data[i]
        price = bar["close"]

        news = _get_news_sentiment(symbol, use_news)
        poly = _get_polymarket_sentiment(symbol, use_polymarket)

        signal, comp_conf, claude_conf, news_score, poly_score, source = _get_decision(
            bar["rsi"], bar["macd"], bar["adx"], bar["sentiment"],
            has_position=position is not None,
            news=news, poly=poly,
            use_claude=use_claude,
            use_news=use_news,
            use_polymarket=use_polymarket,
        )

        if signal == "BUY" and position is None and comp_conf >= confidence_gate:
            risk_amount = balance * risk_pct
            size        = risk_amount / price
            balance    -= risk_amount
            position    = {"entry_price": price, "size": size, "date": bar["date"],
                           "source": source}
            source_counts[source] = source_counts.get(source, 0) + 1
            if source == "polymarket":
                polymarket_trade_count += 1
            trades.append(TradeRecord(
                date=bar["date"], type="BUY", price=price,
                size=size, pnl=0.0,
                confidence=int(comp_conf),
                claude_confidence=int(claude_conf),
                news_sentiment=news_score,
                polymarket_sentiment=poly.get("probability", 50.0),
                polymarket_score=poly_score,
                signal_source=source,
            ))

        elif signal == "SELL" and position is not None:
            exit_value  = position["size"] * price
            entry_value = position["size"] * position["entry_price"]
            pnl_pct     = (exit_value - entry_value) / entry_value * 100
            balance    += exit_value
            (winning_pcts if pnl_pct > 0 else losing_pcts).append(pnl_pct)
            source_counts[source] = source_counts.get(source, 0) + 1
            trades.append(TradeRecord(
                date=bar["date"], type="SELL", price=price,
                size=position["size"], pnl=round(pnl_pct, 4),
                confidence=int(comp_conf),
                claude_confidence=int(claude_conf),
                news_sentiment=news_score,
                polymarket_sentiment=poly.get("probability", 50.0),
                polymarket_score=poly_score,
                signal_source=source,
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

    # ── Signal breakdown ──────────────────────────────────────────────────────
    total_sig = sum(source_counts.values()) or 1
    signal_breakdown = [
        {"source": src, "count": cnt, "pct": round(cnt / total_sig * 100, 1)}
        for src, cnt in source_counts.items()
        if cnt > 0
    ]

    metrics = BacktestMetrics(
        final_balance      = round(balance, 2),
        total_return       = round(total_return, 2),
        win_rate           = round(win_rate, 2),
        wins               = wins,
        losses             = losses,
        total_trades       = total_trades,
        avg_win            = round(avg_win, 2),
        avg_loss           = round(avg_loss, 2),
        profit_factor      = round(profit_factor, 2),
        max_drawdown       = round(max_drawdown, 2),
        sharpe_ratio       = round(sharpe, 2),
        polymarket_trades  = polymarket_trade_count,
    )

    return BacktestResult(
        metrics          = metrics,
        equity_curve     = equity_curve,
        trades           = trades,
        monthly_returns  = monthly_returns,
        signal_breakdown = signal_breakdown,
    )
