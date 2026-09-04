# Speedport 7 für Home Assistant

Inoffizielle Home-Assistant-Integration für den Telekom [Speedport 7](https://www.telekom.de/hilfe/geraete-zubehoer/router/speedport-7)
(Arcadyan `DT-HGW01A-ARC`). Liest die lokale Status-API des Routers auf Port 80
aus — ohne Login, rein lesend.

[![Repository in HACS hinzufügen](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Eibelucas&repository=homeassistant-speedport7&category=integration)

## Funktionen

- WLAN ein/aus
- Internetverbindung (WAN-Up/Down)
- DSL/Faser-Uplink
- LAN-Ports
- Telefonie
- **Ausfallschutz aktiv** — abgeleitet aus Internet-Up bei gleichzeitig
  DSL/Faser-Down (Notfall-LTE greift)
- Öffentliche WAN-IP
- SSID des Haupt-WLANs
- Letzter Neustart des Routers
- Uptime
- Installierte Firmware
- Letzter erfolgreicher Abruf

Alle Werte sind **Statusinformationen**. Die Speedport-7-API ist ausschließlich
lesend — WLAN an/aus schalten, Gäste-WLAN oder andere Einstellungen bleiben
Aufgabe der MeinMagenta-App.

## Installation über HACS

1. Öffne HACS und wähle **Integrationen**.
2. Öffne das Menü und wähle **Benutzerdefinierte Repositories**.
3. Trage die URL dieses Repositorys ein und wähle die Kategorie **Integration**.
4. Installiere **Speedport 7**.
5. Starte Home Assistant neu.
6. Öffne **Einstellungen > Geräte & Dienste > Integration hinzufügen**.
7. Suche nach **Speedport 7** und trage die Adresse deines Routers ein
   (Standard: `speedport.ip`, alternativ die lokale IP, z.B. `192.168.3.1`).

## Technischer Hintergrund

Der Speedport 7 stellt im lokalen Netz eine unauthentifizierte JSON-API bereit:

- `http://<router>/api/getRouterStatus` — WLAN, Internet, DSL/Faser, Telefonie,
  WAN-IP, SSID
- `http://<router>/api/getDeviceInfo` — Seriennummer, Firmware, Uptime, letzter
  Neustart

Diese Integration fragt ausschließlich diese Endpunkte ab und verändert nichts
am Router.

## Datenschutz

Es werden keine Zugangsdaten benötigt oder gespeichert. Der Router wird nur
über das lokale Netz angefragt; es werden keinerlei Daten an Cloud-Dienste
übertragen.

## Hinweise

Diese Integration ist weder von der Telekom noch von Arcadyan entwickelt oder
unterstützt. Änderungen an der Router-Firmware können einzelne Funktionen
beeinträchtigen. Da der Speedport 7 nur über die MeinMagenta-App konfiguriert
werden kann, kann sich die lokale API jederzeit ändern oder verschwinden.

## KI-Nutzung und Haftungsausschluss

Der Quellcode dieser Integration wurde ausschließlich mithilfe künstlicher
Intelligenz erstellt und nicht professionell geprüft oder offiziell
zertifiziert. Die Nutzung erfolgt vollständig auf eigene Gefahr.

Der Anbieter dieses Repositorys übernimmt, soweit gesetzlich zulässig, keine
Haftung für direkte oder indirekte Schäden. Das gilt insbesondere für:

- Falsche, unvollständige oder verspätete Angaben in Home Assistant
- Ausfälle des Routers oder der lokalen Status-API
- Verlust von Daten oder Zugang zum Router

Vor der Nutzung sind die Bedingungen der Telekom und des Speedport 7 zu
beachten. Statusangaben sollten bei Bedarf zusätzlich im offiziellen
Router-Zugang der MeinMagenta-App kontrolliert werden.

## Bekannte Einschränkungen

- Keine Steuerfunktionen — die API des Speedport 7 ist nur lesend.
- Keine Geräteliste — der Router stellt verbundene Clients nicht über die
  lokale API bereit.
- Die `lastRebootTimeStamp`-Angabe fehlt auf manchen Firmware-Ständen; dann
  zeigt `Letzter Neustart` `unbekannt` an.

Änderungen sind im [Changelog](CHANGELOG.md) dokumentiert.