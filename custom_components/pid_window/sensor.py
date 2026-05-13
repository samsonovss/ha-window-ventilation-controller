"""Sensors for PID Window Controller."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN
from . import RuntimeData


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> None:
    runtime: RuntimeData = hass.data[DOMAIN][entry.entry_id]
    controller = runtime.controller
    sensors = [
        PidWindowSensor(controller, entry.entry_id, "current_temp", "Current temperature", UnitOfTemperature.CELSIUS),
        PidWindowSensor(controller, entry.entry_id, "outdoor_temp", "Outdoor temperature", UnitOfTemperature.CELSIUS),
        PidWindowSensor(controller, entry.entry_id, "cover_position", "Cover position", "%"),
        PidWindowSensor(controller, entry.entry_id, "pid_output", "PID output", "%"),
        PidWindowSensor(controller, entry.entry_id, "error", "Temperature error", UnitOfTemperature.CELSIUS),
        PidWindowSensor(controller, entry.entry_id, "status", "Controller status", None, is_text=True),
    ]
    async_add_entities(sensors)


class PidWindowSensor(SensorEntity):
    def __init__(self, controller, entry_id: str, key: str, name: str, unit: str | None, is_text: bool = False) -> None:
        self._controller = controller
        self._key = key
        self._is_text = is_text
        self._attr_name = name
        self._attr_unique_id = f"{entry_id}_{key}"
        self._attr_native_unit_of_measurement = unit
        self._remove_listener = controller.register_listener(self._handle_update)

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self._remove_listener)

    @callback
    def _handle_update(self) -> None:
        self.async_write_ha_state()

    @property
    def native_value(self):
        value = getattr(self._controller.state, self._key)
        if self._is_text:
            return value
        return None if value is None else round(float(value), 1)
