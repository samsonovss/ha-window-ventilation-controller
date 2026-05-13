"""Buttons for PID Window Controller."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from . import RuntimeData


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> None:
    runtime: RuntimeData = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([PidWindowAutotuneButton(runtime.controller, entry.entry_id)])


class PidWindowAutotuneButton(ButtonEntity):
    _attr_has_entity_name = True

    def __init__(self, controller, entry_id: str) -> None:
        self._controller = controller
        self._attr_device_info = controller.device_info
        self._entry_id = entry_id
        self._attr_name = "PID Window Autotune"
        self._attr_unique_id = f"{entry_id}_autotune"

    @property
    def available(self) -> bool:
        return self._controller.state.current_temp is not None

    async def async_press(self) -> None:
        await self._controller.async_autotune()
