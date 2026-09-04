"""Client for the Speedport 7 local status API."""

from __future__ import annotations

import asyncio
from datetime import datetime

import aiohttp


class Speedport7ConnectionError(RuntimeError):
    """Raised when the router cannot be reached."""


class Speedport7Client:
    """Query the read-only status endpoints of a Speedport 7."""

    def __init__(self, session: aiohttp.ClientSession, host: str) -> None:
        self._session = session
        self._base = f"http://{host}"

    async def async_get_router_status(self) -> dict:
        """Return the router status payload."""
        return await self._async_get_json("api/getRouterStatus")

    async def async_get_device_info(self) -> dict:
        """Return the device information payload."""
        return await self._async_get_json("api/getDeviceInfo")

    async def _async_get_json(self, path: str) -> dict:
        """Fetch one status endpoint and parse its JSON payload."""
        try:
            async with self._session.get(
                f"{self._base}/{path}",
                headers={"Accept": "application/json"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                resp.raise_for_status()
                return await resp.json(content_type=None)
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            raise Speedport7ConnectionError(
                "Speedport 7 ist nicht erreichbar"
            ) from err


def is_wifi_on(status: dict) -> bool:
    """Whether the main WLAN is enabled."""
    return status.get("wifiStatus") == "true"


def is_internet_up(status: dict) -> bool:
    """Whether the internet connection is up."""
    return status.get("internetStatus") == "Up"


def is_broadband_up(status: dict) -> bool:
    """Whether the DSL or fibre uplink is up."""
    return status.get("broadbandStatus") == "Up"


def is_lan_active(status: dict) -> bool:
    """Whether the LAN ports are active."""
    return status.get("lanStatus") == "true"


def is_phone_up(status: dict) -> bool:
    """Whether the telephone service is up."""
    return status.get("phoneStatus") == "Up"


def is_failover_active(status: dict) -> bool:
    """Whether the LTE fallback currently bridges a broadband outage."""
    return is_internet_up(status) and not is_broadband_up(status)


def parse_reboot_timestamp(value: str | None) -> datetime | None:
    """Convert a router timestamp like '28.08.2026, 21:40' to a datetime."""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%d.%m.%Y, %H:%M")
    except ValueError:
        return None