from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Iterable


@dataclass
class QuoteRow:
    exchange: str
    bid: float | None
    ask: float | None
    spread: float | None
    age_s: float
    status: str


@dataclass
class _QuoteState:
    bid: float | None
    ask: float | None
    updated_at: float
    status: str


class MockQuoteEngine:
    def __init__(self, exchanges: Iterable[str]) -> None:
        self._state: dict[str, _QuoteState] = {}
        now = time.time()
        for exchange in exchanges:
            bid, ask = self._generate_price()
            self._state[exchange] = _QuoteState(
                bid=bid,
                ask=ask,
                updated_at=now,
                status="OK",
            )

    def refresh(self, enabled_exchanges: set[str]) -> list[QuoteRow]:
        now = time.time()
        rows: list[QuoteRow] = []
        for exchange, state in self._state.items():
            if exchange in enabled_exchanges:
                state = self._update_state(state, now)
                self._state[exchange] = state
            else:
                state = _QuoteState(
                    bid=state.bid,
                    ask=state.ask,
                    updated_at=state.updated_at,
                    status="STALE",
                )
            age_s = max(0.0, now - state.updated_at)
            spread = None
            if state.bid is not None and state.ask is not None:
                spread = state.ask - state.bid
            rows.append(
                QuoteRow(
                    exchange=exchange,
                    bid=state.bid,
                    ask=state.ask,
                    spread=spread,
                    age_s=age_s,
                    status=state.status,
                )
            )
        return rows

    def _update_state(self, state: _QuoteState, now: float) -> _QuoteState:
        if random.random() < 0.03:
            return _QuoteState(
                bid=None,
                ask=None,
                updated_at=now,
                status="ERROR",
            )
        bid, ask = self._generate_price()
        return _QuoteState(
            bid=bid,
            ask=ask,
            updated_at=now,
            status="OK",
        )

    @staticmethod
    def _generate_price() -> tuple[float, float]:
        base = 1.0 + random.uniform(-0.0005, 0.0005)
        spread = random.uniform(0.00005, 0.0004)
        bid = round(base, 6)
        ask = round(base + spread, 6)
        return bid, ask
