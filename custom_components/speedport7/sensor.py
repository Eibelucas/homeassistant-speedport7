"""Sensors for the Speedport 7 integration."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import (
    is_broadband_up,
    is_failover_active,
    is_internet_up,
    is_lan_active,
    is_phone_up,
    is_wifi_on,
    parse_reboot_timestamp,
)
from .const import DOMAIN
from .coordinator import Speedport7Coordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Speedport 7 entities."""
    coordinator: Speedport7Coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            SpeedportWifiBinarySensor(coordinator, entry),
            SpeedportInternetBinarySensor(coordinator, entry),
            SpeedportBroadbandBinarySensor(coordinator, entry),
            SpeedportLanBinarySensor(coordinator, entry),
            SpeedportPhoneBinarySensor(coordinator, entry),
            SpeedportFailoverBinarySensor(coordinator, entry),
            SpeedportWanIpSensor(coordinator, entry),
            SpeedportSsidSensor(coordinator, entry),
            SpeedportLastRebootSensor(coordinator, entry),
            SpeedportUptimeSensor(coordinator, entry),
            SpeedportFirmwareSensor(coordinator, entry),
            SpeedportLastSuccessfulUpdateSensor(coordinator, entry),
        ]
    )


class Speedport7Entity(CoordinatorEntity[Speedport7Coordinator]):
    """Base Speedport 7 entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: Speedport7Coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry
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
        return parse_reboot_timestamp(self.device.get("lastRebootTimeStamp"))


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