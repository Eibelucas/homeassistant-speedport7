"""Constants for the Speedport 7 integration."""

DOMAIN = "speedport7"

CONF_HOST = "host"
CONF_UPDATE_INTERVAL = "update_interval"

DEFAULT_UPDATE_INTERVAL = 60
UPDATE_INTERVAL_OPTIONS = [30, 60, 120, 300]

PLATFORMS = ["binary_sensor", "sensor"]