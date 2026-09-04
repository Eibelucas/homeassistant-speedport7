"""Shared entity helpers for the Speedport 7 integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import Speedport7Coordinator


class Speedport7Entity(CoordinatorEntity[Speedport7Coordinator]):
    """Base Speedport 7 entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        device = self.device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device.get("serialNum") or entry.entry_id)},
            name="Speedport 7",
            manufacturer="Arcadyan",
            model=device.get("device_name") or "Speedport 7 Typ A",
            sw_version=device.get("swVersion"),
            serial_number=device.get("serialNum"),
            configuration_url=f"http://{entry.data[CONF_HOST]}",
        )

    @property
    def status(self) -> dict:
        """Current router status payload."""
        return self.coordinator.data.get("status", {}) if self.coordinator.data else {}

    @property
    def device(self) -> dict:
        """Current device information payload."""
        return self.coordinator.data.get("device", {}) if self.coordinator.data else {}