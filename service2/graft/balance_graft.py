"""Graftcode contract of service2, hosted by Graftcode Gateway (gg) in its own process.

Replaces the RabbitMQ "changebalance_orders" queue consumer as the transport; the
business logic is the unchanged ../logic.py change_balance handler.
"""
import asyncio as _asyncio
import contextlib as _contextlib
import os as _os
import sys as _sys
from types import SimpleNamespace as _SimpleNamespace

_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from logic import change_balance as _change_balance  # noqa: E402  (existing service2 logic)


class BalanceService:
    @staticmethod
    def change_balance(payload_json: str) -> bool:
        # Same JSON body the API used to publish to the "changebalance_orders" queue;
        # there is no broker message to ack, so process() is a no-op context.
        message = _SimpleNamespace(body=payload_json.encode(), process=_contextlib.nullcontext)
        _asyncio.run(_change_balance(message))
        return True
