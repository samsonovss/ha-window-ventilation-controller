"""Cover proxy for PID Window Controller."""

from __future__ import annotations

from homeassistant.components.cover import ATTR_POSITION, CoverEntity, CoverEntityFeature
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, callback

from . import RuntimeData
from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> None:
    runtime: RuntimeData = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([PidWindowCover(runtime.controller, entry.entry_id)])


class PidWindowCover(CoverEntity):
    def __init__(self, controller, entry_id: str) -> None:
        self._controller = controller
        self._attr_has_entity_name = True
        self._attr_device_info = controller.device_info
        self._attr_translation_key = "window"
        self._attr_unique_id = f"{entry_id}_window"
        self._remove_listener = controller.register_listener(self._handle_update)

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self._remove_listener)

    @callback
    def _handle_update(self) -> None:
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        state = self.hass.states.get(self._controller.cover_entity)
        return state is not None and state.state not in {STATE_UNKNOWN, STATE_UNAVAILABLE, "none"}

    @property
    def supported_features(self) -> CoverEntityFeature:
        features = CoverEntityFeature.SET_POSITION | CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE
        state = self.hass.states.get(self._controller.cover_entity)
        if state is None:
            return features

        target_features = int(state.attributes.get("supported_features", 0))
        if target_features & int(CoverEntityFeature.STOP):
            features |= CoverEntityFeature.STOP
        return features

    @property
    def current_cover_position(self) -> int | None:
        position = self._controller.state.cover_position
        return None if position is None else round(position)

    @property
    def is_closed(self) -> bool | None:
        position = self.current_cover_position
        if position is None:
            return None
        return position <= self._controller.min_position

    async def async_open_cover(self, **kwargs) -> None:
        await self._controller.async_set_cover_position(float(self._controller.max_position))

    async def async_close_cover(self, **kwargs) -> None:
        await self._controller.async_set_cover_position(float(self._controller.min_position))

    async def async_set_cover_position(self, **kwargs) -> None:
        await self._controller.async_set_cover_position(float(kwargs[ATTR_POSITION]))

    async def async_stop_cover(self, **kwargs) -> None:
        await self.hass.services.async_call(
            "cover",
            "stop_cover",
            {"entity_id": self._controller.cover_entity},
            blocking=False,
        )
