# Changelog

## 0.1.0 - 2026-09-04

### Hinzugefügt

- Erste öffentliche HACS-Version.
- Status der lokalen Speedport-7-API: WLAN, Internet, DSL/Faser, LAN,
  Telefonie, WAN-IP, SSID, letzter Neustart, Uptime, Firmware.
- Abgeleiteter Sensor `Ausfallschutz (LTE aktiv)`.
- Konfigurationsablauf mit Router-Adresse und wählbarem Abrufintervall.
## [0.1.1] - 2026-09-04

- Fix: Binary sensors crashed setup because the integration declared a `binary_sensor` platform that did not exist. The six binary sensors now live in their own `binary_sensor.py`, the base entity in `entity.py`.
