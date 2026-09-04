"""Config flow for the Speedport 7 integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import voluptuous as vol

from .api import Speedport7Client, Speedport7ConnectionError
from .const import (
    CONF_HOST,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    UPDATE_INTERVAL_OPTIONS,
)


class Speedport7ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the Speedport 7 configuration flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Collect the router address and verify the status API."""
        errors: dict[str, str] = {}
        if user_input is not None:
            host = user_input[CONF_HOST]
            session = async_create_clientsession(self.hass, auto_cleanup=False)
            client = Speedport7Client(session, host)
            try:
                await client.async_get_router_status()
                device = await client.async_get_device_info()
            except Speedport7ConnectionError:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"
            else:
                serial = device.get("serialNum") or host
                await self.async_set_unique_id(serial)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="Speedport 7", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default="speedport.ip"): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    def async_get_options_flow(config_entry) -> OptionsFlow:
        """Return the options flow."""
        return Speedport7OptionsFlow()


class Speedport7OptionsFlow(OptionsFlow):
    """Configure the polling interval."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage integration options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.options.get(
            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
        )
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_UPDATE_INTERVAL, default=str(current)
                ): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[str(value) for value in UPDATE_INTERVAL_OPTIONS],
                        translation_key="update_interval",
                    )
                )
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)