"""Unit tests for the Speedport 7 status parsing helpers."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import types
import unittest

COMPONENT = (
    Path(__file__).parents[1]
    / "custom_components"
    / "speedport7"
)
PACKAGE = "speedport7_api_tests"
package = types.ModuleType(PACKAGE)
package.__path__ = [str(COMPONENT)]
sys.modules[PACKAGE] = package

for module_name in ("const", "api"):
    spec = importlib.util.spec_from_file_location(
        f"{PACKAGE}.{module_name}", COMPONENT / f"{module_name}.py"
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"{PACKAGE}.{module_name}"] = module
    spec.loader.exec_module(module)  # type: ignore[attr-defined]

from speedport7_api_tests.api import (  # noqa: E402
    is_broadband_up,
    is_failover_active,
    is_internet_up,
    is_lan_active,
    is_phone_up,
    is_wifi_on,
    parse_reboot_timestamp,
)

STATUS_UP = {
    "wifiStatus": "true",
    "internetStatus": "Up",
    "broadbandStatus": "Up",
    "lanStatus": "true",
    "phoneStatus": "Up",
}

STATUS_DOWN = {
    "wifiStatus": "false",
    "internetStatus": "Down",
    "broadbandStatus": "Down",
    "lanStatus": "false",
    "phoneStatus": "-",
}


class TestStatusHelpers(unittest.TestCase):
    """Test the boolean status mappings."""

    def test_wifi_on(self) -> None:
        self.assertTrue(is_wifi_on(STATUS_UP))
        self.assertFalse(is_wifi_on(STATUS_DOWN))
        self.assertFalse(is_wifi_on({}))

    def test_internet_up(self) -> None:
        self.assertTrue(is_internet_up(STATUS_UP))
        self.assertFalse(is_internet_up(STATUS_DOWN))
        self.assertFalse(is_internet_up({}))

    def test_broadband_up(self) -> None:
        self.assertTrue(is_broadband_up(STATUS_UP))
        self.assertFalse(is_broadband_up(STATUS_DOWN))
        self.assertFalse(is_broadband_up({}))

    def test_lan_active(self) -> None:
        self.assertTrue(is_lan_active(STATUS_UP))
        self.assertFalse(is_lan_active(STATUS_DOWN))
        self.assertFalse(is_lan_active({}))

    def test_phone_up(self) -> None:
        self.assertTrue(is_phone_up(STATUS_UP))
        self.assertFalse(is_phone_up(STATUS_DOWN))
        self.assertFalse(is_phone_up({}))

    def test_failover_not_active_when_broadband_up(self) -> None:
        self.assertFalse(is_failover_active(STATUS_UP))

    def test_failover_active_during_broadband_outage(self) -> None:
        status = {**STATUS_DOWN, "internetStatus": "Up"}
        self.assertTrue(is_failover_active(status))

    def test_failover_inactive_when_everything_down(self) -> None:
        self.assertFalse(is_failover_active(STATUS_DOWN))


class TestRebootTimestamp(unittest.TestCase):
    """Test the router timestamp parser."""

    def test_parses_german_format(self) -> None:
        parsed = parse_reboot_timestamp("28.08.2026, 21:40")
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.year, 2026)
        self.assertEqual(parsed.month, 8)
        self.assertEqual(parsed.day, 28)
        self.assertEqual(parsed.hour, 21)
        self.assertEqual(parsed.minute, 40)

    def test_missing_or_invalid_value(self) -> None:
        self.assertIsNone(parse_reboot_timestamp(None))
        self.assertIsNone(parse_reboot_timestamp(""))
        self.assertIsNone(parse_reboot_timestamp("-"))


if __name__ == "__main__":
    unittest.main()