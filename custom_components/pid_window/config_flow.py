"""Config flow for PID Window Controller."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_COVER_ENTITY,
    CONF_OUTDOOR_SENSOR,
    CONF_TEMP_SENSOR,
    DEFAULT_NAME,
    DOMAIN,
)


def _options_schema(data: dict | None = None) -> dict:
    data = data or {}
    return {
        vol.Required(CONF_TEMP_SENSOR, default=data.get(CONF_TEMP_SENSOR, "")): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        ),
        vol.Optional(CONF_OUTDOOR_SENSOR, default=data.get(CONF_OUTDOOR_SENSOR, "")): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="sensor")
        ),
        vol.Required(CONF_COVER_ENTITY, default=data.get(CONF_COVER_ENTITY, "")): selector.EntitySelector(
            selector.EntitySelectorConfig(domain="cover")
        ),
    }


def _schema(data: dict | None = None) -> vol.Schema:
    return vol.Schema(_options_schema(data))


def _config_options_schema(data: dict | None = None) -> vol.Schema:
    return vol.Schema(_options_schema(data))


class PidWindowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 7

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=DEFAULT_NAME, data=user_input)
        return self.async_show_form(step_id="user", data_schema=_schema(), errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PidWindowOptionsFlow()


class PidWindowOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=_config_options_schema({**self.config_entry.data, **self.config_entry.options}),
        )
