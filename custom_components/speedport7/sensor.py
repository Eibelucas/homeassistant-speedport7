"""Sensors for the Speedport 7 integration."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .api import parse_reboot_timestamp
from .const import DOMAIN
from .coordinator import Speedport7Coordinator
from .entity import Speedport7Entity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Speedport 7 sensors."""
    coordinator: Speedport7Coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            SpeedportWanIpSensor(coordinator, entry),
            SpeedportSsidSensor(coordinator, entry),
            SpeedportLastRebootSensor(coordinator, entry),
            SpeedportUptimeSensor(coordinator, entry),
            SpeedportFirmwareSensor(coordinator, entry),
            SpeedportLastSuccessfulUpdateSensor(coordinator, entry),
        ]
    )


class SpeedportWanIpSensor(Speedport7Entity, SensorEntity):
    """Public WAN IP address of the router."""

    _attr_translation_key = "wan_ip"
    _attr_icon = "mdi:ip-network"

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_wan_ip"

    @property
    def native_value(self) -> str | None:
        return self.status.get("ipAdd")


class SpeedportSsidSensor(Speedport7Entity, SensorEntity):
    """Main WLAN SSID."""

    _attr_translation_key = "ssid"
    _attr_icon = "mdi:wifi"

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_ssid"

    @property
    def native_value(self) -> str | None:
        return self.status.get("wifi_ssid")


class SpeedportLastRebootSensor(Speedport7Entity, SensorEntity):
    """Timestamp of the last router restart."""

    _attr_translation_key = "last_reboot"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:restart"

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_last_reboot"

    @property
    def native_value(self) -> datetime | None:
        if value := parse_reboot_timestamp(self.device.get("lastRebootTimeStamp")):
            return value.replace(tzinfo=dt_util.DEFAULT_TIME_ZONE)
        return None


class SpeedportUptimeSensor(Speedport7Entity, SensorEntity):
    """Router uptime as reported by the device."""

    _attr_translation_key = "uptime"
    _attr_icon = "mdi:timer-outline"

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_uptime"

    @property
    def native_value(self) -> str | None:
        return self.device.get("uptime")


class SpeedportFirmwareSensor(Speedport7Entity, SensorEntity):
    """Installed router firmware version."""

    _attr_translation_key = "firmware"
    _attr_icon = "mdi:router-network"

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_firmware"

    @property
    def native_value(self) -> str | None:
        return self.device.get("swVersion")


class SpeedportLastSuccessfulUpdateSensor(Speedport7Entity, SensorEntity):
    """Timestamp of the last successful status refresh."""

    _attr_translation_key = "last_successful_update"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:cloud-check"

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_last_successful_update"

    @property
    def native_value(self) -> datetime | None:
        return self.coordinator.last_successful_update