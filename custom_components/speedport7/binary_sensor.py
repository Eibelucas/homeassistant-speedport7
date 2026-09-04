"""Binary sensors for the Speedport 7 integration."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import (
    is_broadband_up,
    is_failover_active,
    is_internet_up,
    is_lan_active,
    is_phone_up,
    is_wifi_on,
)
from .const import DOMAIN
from .coordinator import Speedport7Coordinator
from .entity import Speedport7Entity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Speedport 7 binary sensors."""
    coordinator: Speedport7Coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            SpeedportWifiBinarySensor(coordinator, entry),
            SpeedportInternetBinarySensor(coordinator, entry),
            SpeedportBroadbandBinarySensor(coordinator, entry),
            SpeedportLanBinarySensor(coordinator, entry),
            SpeedportPhoneBinarySensor(coordinator, entry),
            SpeedportFailoverBinarySensor(coordinator, entry),
        ]
    )


class SpeedportWifiBinarySensor(Speedport7Entity, BinarySensorEntity):
    """Whether the main WLAN is enabled."""

    _attr_translation_key = "wlan"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_wlan"

    @property
    def is_on(self) -> bool:
        return is_wifi_on(self.status)


class SpeedportInternetBinarySensor(Speedport7Entity, BinarySensorEntity):
    """Whether the router has an internet connection."""

    _attr_translation_key = "internet"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_internet"

    @property
    def is_on(self) -> bool:
        return is_internet_up(self.status)


class SpeedportBroadbandBinarySensor(Speedport7Entity, BinarySensorEntity):
    """Whether the DSL or fibre uplink is up."""

    _attr_translation_key = "broadband"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_broadband"

    @property
    def is_on(self) -> bool:
        return is_broadband_up(self.status)


class SpeedportLanBinarySensor(Speedport7Entity, BinarySensorEntity):
    """Whether the LAN ports are active."""

    _attr_translation_key = "lan"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_lan"

    @property
    def is_on(self) -> bool:
        return is_lan_active(self.status)


class SpeedportPhoneBinarySensor(Speedport7Entity, BinarySensorEntity):
    """Whether the telephone service is up."""

    _attr_translation_key = "phone"

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_phone"

    @property
    def is_on(self) -> bool:
        return is_phone_up(self.status)


class SpeedportFailoverBinarySensor(Speedport7Entity, BinarySensorEntity):
    """Whether the LTE fallback bridges a broadband outage."""

    _attr_translation_key = "failover"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_failover"

    @property
    def is_on(self) -> bool:
        return is_failover_active(self.status)