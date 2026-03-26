"""
Exchange manager — wraps CCXT to provide a unified async interface
for Bybit, Binance, KuCoin, and OKX.
"""
import asyncio
import logging
from typing import Optional

import ccxt.async_support as ccxt

from backend.config import settings

log = logging.getLogger(__name__)


EXCHANGE_CLASSES = {
    "bybit":   ccxt.bybit,
    "binance": ccxt.binance,
    "kucoin":  ccxt.kucoin,
    "okx":     ccxt.okx,
}


def _build_exchange(name: str, api_key: str = "", api_secret: str = "",
                    passphrase: str = "", testnet: bool = True) -> ccxt.Exchange:
    """Instantiate a CCXT exchange with the right options."""
    cls = EXCHANGE_CLASSES.get(name)
    if cls is None:
        raise ValueError(f"Unsupported exchange: {name}")

    params: dict = {
        "apiKey":     api_key,
        "secret":     api_secret,
        "enableRateLimit": True,
        "options":    {"defaultType": "future"},
    }

    if passphrase:
        params["password"] = passphrase

    exchange = cls(params)

    if testnet:
        if name == "bybit":
            exchange.set_sandbox_mode(True)
        elif name == "binance":
            exchange.set_sandbox_mode(True)

    return exchange


class ExchangeManager:
    """
    Singleton-ish manager that holds one CCXT connection per exchange.
    All public methods are async.
    """

    def __init__(self):
        self._exchanges: dict[str, ccxt.Exchange] = {}

    # ── lifecycle ─────────────────────────────────────────────────────────────

    async def connect(self, name: str, api_key: str, api_secret: str,
                      passphrase: str = "", testnet: bool = True) -> bool:
        """Open (or replace) a connection to `name`."""
        try:
            ex = _build_exchange(name, api_key, api_secret, passphrase, testnet)
            await ex.load_markets()
            self._exchanges[name] = ex
            log.info("Connected to %s (testnet=%s)", name, testnet)
            return True
        except Exception as exc:
            log.error("Failed to connect to %s: %s", name, exc)
            return False

    async def connect_from_config(self) -> dict[str, bool]:
        """Connect all exchanges configured in settings."""
        results: dict[str, bool] = {}

        pairs = [
            ("bybit",   settings.BYBIT_API_KEY,    settings.BYBIT_API_SECRET,    "",                          settings.BYBIT_TESTNET),
            ("binance", settings.BINANCE_API_KEY,  settings.BINANCE_API_SECRET,  "",                          settings.BINANCE_TESTNET),
            ("kucoin",  settings.KUCOIN_API_KEY,   settings.KUCOIN_API_SECRET,   settings.KUCOIN_API_PASSPHRASE, False),
            ("okx",     settings.OKX_API_KEY,      settings.OKX_API_SECRET,      settings.OKX_API_PASSPHRASE,   False),
        ]

        for name, key, secret, passphrase, testnet in pairs:
            if key and secret:
                results[name] = await self.connect(name, key, secret, passphrase, testnet)

        return results

    async def close_all(self):
        for name, ex in self._exchanges.items():
            try:
                await ex.close()
            except Exception:
                pass
        self._exchanges.clear()

    def get(self, name: str) -> Optional[ccxt.Exchange]:
        return self._exchanges.get(name)

    def active_exchange(self) -> Optional[ccxt.Exchange]:
        return self._exchanges.get(settings.ACTIVE_EXCHANGE)

    def is_connected(self, name: str) -> bool:
        return name in self._exchanges

    # ── market data ──────────────────────────────────────────────────────────

    async def fetch_ohlcv(self, symbol: str, timeframe: str = "1m",
                          limit: int = 200, exchange: str = None) -> list:
        """Return list of [ts, open, high, low, close, volume]."""
        ex = self._get_ex(exchange)
        try:
            return await ex.fetch_ohlcv(symbol, timeframe, limit=limit)
        except Exception as exc:
            log.error("fetch_ohlcv %s %s: %s", symbol, timeframe, exc)
            return []

    async def fetch_ticker(self, symbol: str, exchange: str = None) -> dict:
        ex = self._get_ex(exchange)
        try:
            return await ex.fetch_ticker(symbol)
        except Exception as exc:
            log.error("fetch_ticker %s: %s", symbol, exc)
            return {}

    async def fetch_order_book(self, symbol: str, limit: int = 20,
                               exchange: str = None) -> dict:
        ex = self._get_ex(exchange)
        try:
            return await ex.fetch_order_book(symbol, limit=limit)
        except Exception as exc:
            log.error("fetch_order_book %s: %s", symbol, exc)
            return {}

    # ── account ───────────────────────────────────────────────────────────────

    async def fetch_balance(self, exchange: str = None) -> dict:
        ex = self._get_ex(exchange)
        try:
            bal = await ex.fetch_balance()
            return {
                "total":  bal.get("total",  {}),
                "free":   bal.get("free",   {}),
                "used":   bal.get("used",   {}),
                "usdt":   bal.get("total",  {}).get("USDT", 0),
            }
        except Exception as exc:
            log.error("fetch_balance: %s", exc)
            return {"total": {}, "free": {}, "used": {}, "usdt": 0}

    async def fetch_positions(self, exchange: str = None) -> list:
        ex = self._get_ex(exchange)
        try:
            positions = await ex.fetch_positions()
            return [p for p in positions if float(p.get("contracts", 0)) != 0]
        except Exception as exc:
            log.error("fetch_positions: %s", exc)
            return []

    # ── order management ─────────────────────────────────────────────────────

    async def create_market_order(self, symbol: str, side: str, amount: float,
                                  params: dict = None, exchange: str = None) -> dict:
        ex = self._get_ex(exchange)
        try:
            order = await ex.create_market_order(symbol, side, amount, params=params or {})
            log.info("Market order placed: %s %s %s @ market", side, amount, symbol)
            return order
        except Exception as exc:
            log.error("create_market_order %s %s %s: %s", symbol, side, amount, exc)
            raise

    async def create_limit_order(self, symbol: str, side: str, amount: float,
                                 price: float, params: dict = None,
                                 exchange: str = None) -> dict:
        ex = self._get_ex(exchange)
        try:
            order = await ex.create_limit_order(symbol, side, amount, price, params=params or {})
            log.info("Limit order placed: %s %s %s @ %s", side, amount, symbol, price)
            return order
        except Exception as exc:
            log.error("create_limit_order %s %s %s @ %s: %s", symbol, side, amount, price, exc)
            raise

    async def cancel_order(self, order_id: str, symbol: str,
                           exchange: str = None) -> dict:
        ex = self._get_ex(exchange)
        try:
            return await ex.cancel_order(order_id, symbol)
        except Exception as exc:
            log.error("cancel_order %s %s: %s", order_id, symbol, exc)
            raise

    async def fetch_order(self, order_id: str, symbol: str,
                          exchange: str = None) -> dict:
        ex = self._get_ex(exchange)
        try:
            return await ex.fetch_order(order_id, symbol)
        except Exception as exc:
            log.error("fetch_order %s: %s", order_id, exc)
            return {}

    async def set_leverage(self, symbol: str, leverage: int,
                           exchange: str = None):
        ex = self._get_ex(exchange)
        try:
            await ex.set_leverage(leverage, symbol)
        except Exception as exc:
            log.warning("set_leverage %s x%s: %s", symbol, leverage, exc)

    # ── private helpers ───────────────────────────────────────────────────────

    def _get_ex(self, name: str = None) -> ccxt.Exchange:
        name = name or settings.ACTIVE_EXCHANGE
        ex = self._exchanges.get(name)
        if ex is None:
            raise RuntimeError(
                f"Exchange '{name}' is not connected. "
                "Connect via POST /api/exchange/connect or set API keys in .env"
            )
        return ex


# Global singleton
exchange_manager = ExchangeManager()
