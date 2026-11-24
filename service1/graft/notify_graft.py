"""Graftcode contract of service1, hosted by Graftcode Gateway (gg) in its own process.

Replaces the RabbitMQ "notify_user" queue consumer as the transport; the business
logic is the unchanged ../logic.py notify_user handler.
"""
import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
from logic import notify_user as _notify_user  # noqa: E402  (existing service1 logic)


class NotifyService:
    @staticmethod
    def notify_user(payload_json: str) -> bool:
        # Same JSON body the API used to publish to the "notify_user" queue.
        _notify_user(None, None, None, payload_json.encode())
        return True
