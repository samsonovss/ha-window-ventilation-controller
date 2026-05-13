"""Selects for PID Window Controller."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN, PROFILE_AUTO, PROFILE_SUMMER, PROFILE_WINTER
from . import RuntimeData


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> None:
    runtime: RuntimeData = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([PidWindowProfileSelect(runtime.controller, entry.entry_id)])


class PidWindowProfileSelect(SelectEntity):
    _attr_entity_category = EntityCategory.CONFIG
    _attr_options = [PROFILE_AUTO, PROFILE_WINTER, PROFILE_SUMMER]
    _attr_has_entity_name = True

    def __init__(self, controller, entry_id: str) -> None:
        self._controller = controller
        self._attr_device_info = controller.device_info
        self._attr_name = "PID Profile Mode"
        self._attr_unique_id = f"{entry_id}_profile_mode"
        self._remove_listener = controller.register_listener(self._handle_update)

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self._remove_listener)

    @callback
    def _handle_update(self) -> None:
        self.async_write_ha_state()

    @property
    def current_option(self) -> str | None:
        return self._controller.profile_mode

    async def async_select_option(self, option: str) -> None:
        await self._controller.async_set_profile_mode(option)
