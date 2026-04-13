---
name: diaw-m08-alphaomega
description: >
  ALPHA-OMEGA: AI-powered cryptocurrency trading and portfolio management module.
  Provides algorithmic trading strategies, risk management, portfolio optimization,
  market analysis, DeFi yield farming, and automated trading bots. For educational
  and authorized trading platform contexts only. Activates on ALPHA-OMEGA, crypto,
  cryptocurrency, trading bot, portfolio, DeFi, blockchain trading, algorithmic trading.
user-invocable: true
context: fork
effort: high
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__ruflo__*
---

# ALPHA-OMEGA: Crypto Trading Module v3.0

> **DISCLAIMER**: This module is for educational purposes and authorized trading
> platform development only. All trading involves risk. Past performance does not
> guarantee future results. Comply with all applicable financial regulations in
> your jurisdiction (UAE SCA, SEC, etc.) before deploying any trading systems.

## Agent Swarm Configuration
- **Topology**: Consensus | **Max Agents**: 5 | **Quality Gate**: 0.98
- **Agents**: Strategy Agent, Risk Agent, Market Analyst, Execution Agent, Portfolio Agent

## Core Capabilities

### Trading Strategy Framework
```python
class TradingStrategy:
    def __init__(self, name, timeframe, risk_level):
        self.name = name          # Strategy identifier
        self.timeframe = timeframe # '1m', '5m', '1h', '4h', '1d'
        self.risk_level = risk_level  # 'conservative', 'moderate', 'aggressive'
        self.max_position_size = 0.02  # 2% of portfolio per trade
        self.stop_loss = 0.02     # 2% stop loss
        self.take_profit = 0.06   # 6% take profit (3:1 R:R)
```

### Pre-Built Strategies
| Strategy | Type | Timeframe | Win Rate (Backtested) |
|----------|------|-----------|----------------------|
| MA Crossover | Trend Following | 4h | ~55-60% |
| RSI Mean Reversion | Counter-trend | 1h | ~58-63% |
| Bollinger Band Squeeze | Volatility | 1d | ~52-57% |
| MACD Divergence | Momentum | 4h | ~54-59% |
| Multi-timeframe Confluence | Combined | 1h+4h+1d | ~60-65% |

### Risk Management System
```
Position Sizing:     Kelly Criterion (half-Kelly for safety)
Portfolio Allocation: Max 20% in any single asset
Correlation Check:   Avoid holding >3 highly correlated assets
Daily Loss Limit:    Auto-pause if -5% daily P&L
Weekly Loss Limit:   Review if -10% weekly P&L
Drawdown Alert:      Reduce size if portfolio -15% from peak
```

### Market Analysis Tools
- Technical indicators: RSI, MACD, Bollinger Bands, ATR, Volume Profile
- On-chain analytics: wallet activity, exchange flows, whale movements
- Sentiment analysis: social media, fear & greed index, funding rates
- Macro analysis: correlation with traditional markets, regulatory news

### DeFi Yield Optimization
- Liquidity pool APY comparison across protocols
- Impermanent loss calculator and risk assessment
- Auto-compounding strategy selection
- Gas fee optimization for Ethereum/Polygon/BSC

### Regulatory Compliance (UAE)
- UAE SCA (Securities and Commodities Authority) guidelines
- CBUAE (Central Bank UAE) virtual asset regulations
- VARA (Virtual Assets Regulatory Authority) Dubai compliance
- KYC/AML requirements for trading platform builders

## Portfolio Dashboard Metrics
| Metric | Target | Alert |
|--------|--------|-------|
| Sharpe Ratio | >1.5 | <1.0 |
| Max Drawdown | <15% | >20% |
| Win Rate | >55% | <50% |
| Avg R:R | >2.5:1 | <2:1 |
| Monthly Return | >5% | <0% |

## Revenue Model
- **Subscription**: $500/mo
- **Performance Fee**: 10-20% of profits above HWM
- **Enterprise License**: $5,000-$20,000/mo for institutional
- **Credits**: 30-100 per strategy deployment

## Example Invocations
- "ALPHA-OMEGA: Build a BTC/ETH portfolio management system with automated rebalancing"
- "Create a trading bot using MA crossover strategy for top 10 altcoins"
- "ALPHA-OMEGA: Analyze my current crypto portfolio risk and suggest optimizations"
