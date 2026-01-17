import asyncio
import time
from dataclasses import dataclass
from typing import Iterable

import ccxt
from loguru import logger
from rich.console import Console
from rich.table import Table


@dataclass(frozen=True)
class ExchangeQuote:
    exchange: str
    bid: float | None
    ask: float | None
    timestamp: float
    latency_ms: float
    status: str
    error: str | None = None


class ExchangeClient:
    def __init__(self, exchange_id: str, symbol: str) -> None:
        self.exchange_id = exchange_id
        self.symbol = symbol
        exchange_class = getattr(ccxt, exchange_id)
        self.client = exchange_class({"enableRateLimit": True})

    async def fetch_quote(self) -> ExchangeQuote:
        started_at = time.perf_counter()
        timestamp = time.time()
        try:
            order_book = await asyncio.to_thread(
                self.client.fetch_order_book, self.symbol
            )
            bid = order_book["bids"][0][0] if order_book.get("bids") else None
            ask = order_book["asks"][0][0] if order_book.get("asks") else None
            latency_ms = (time.perf_counter() - started_at) * 1000
            status = "ok" if bid is not None and ask is not None else "empty"
            return ExchangeQuote(
                exchange=self.exchange_id,
                bid=bid,
                ask=ask,
                timestamp=timestamp,
                latency_ms=latency_ms,
                status=status,
            )
        except Exception as exc:  # noqa: BLE001 - log and keep running
            latency_ms = (time.perf_counter() - started_at) * 1000
            return ExchangeQuote(
                exchange=self.exchange_id,
                bid=None,
                ask=None,
                timestamp=timestamp,
                latency_ms=latency_ms,
                status="error",
                error=str(exc),
            )


class QuoteMonitor:
    def __init__(
        self, clients: Iterable[ExchangeClient], refresh_interval: float
    ) -> None:
        self.clients = list(clients)
        self.refresh_interval = refresh_interval
        self.console = Console()

    async def run(self) -> None:
        logger.info("Starting quote monitor")
        while True:
            quotes = await asyncio.gather(
                *(client.fetch_quote() for client in self.clients)
            )
            self._render(quotes)
            await asyncio.sleep(self.refresh_interval)

    def _render(self, quotes: Iterable[ExchangeQuote]) -> None:
        table = Table(title="USDT/USDC Quotes")
        table.add_column("Exchange")
        table.add_column("Bid", justify="right")
        table.add_column("Ask", justify="right")
        table.add_column("Latency (ms)", justify="right")
        table.add_column("Status")
        table.add_column("Error")

        for quote in quotes:
            table.add_row(
                quote.exchange,
                f"{quote.bid:.6f}" if quote.bid is not None else "-",
                f"{quote.ask:.6f}" if quote.ask is not None else "-",
                f"{quote.latency_ms:.1f}",
                quote.status,
                quote.error or "",
            )

        self.console.clear()
        self.console.print(table)


async def main() -> None:
    symbol = "USDT/USDC"
    exchanges = ["binance", "kraken", "coinbase"]
    clients = [ExchangeClient(exchange_id, symbol) for exchange_id in exchanges]
    monitor = QuoteMonitor(clients, refresh_interval=5.0)
    await monitor.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Quote monitor stopped")
