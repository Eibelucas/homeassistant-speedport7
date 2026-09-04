"""Data coordinator for the Speedport 7 integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import Speedport7Client, Speedport7ConnectionError
from .const import CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class Speedport7Coordinator(DataUpdateCoordinator[dict]):
    """Coordinate the router status updates."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, client: Speedport7Client
    ) -> None:
        update_interval = int(
            entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
        )
        super().__init__(
            hass,
            logger=_LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )
        self.client = client
        self.last_successful_update: datetime | None = None

    async def _async_update_data(self) -> dict:
        """Fetch router status, device information, and diagnostics."""
        try:
            status = await self.client.async_get_router_status()
            device = await self.client.async_get_device_info()
            tdg = await self.client.async_get_tdg_content()
        except Speedport7ConnectionError as err:
            raise UpdateFailed("Speedport 7 ist nicht erreichbar") from err
        self.last_successful_update = dt_util.utcnow()
        return {"status": status, "device": device, "tdg": tdg}
