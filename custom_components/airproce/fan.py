import logging

from .device import device_info
from .api import AirProceApi
from .const import DOMAIN, DATA_KEY_API, DATA_KEY_GROUPS, DATA_KEY_COORDINATOR
from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up fans for each device from a config entry."""
    # Retrieve data from `hass.data`
    api = hass.data[DOMAIN][entry.entry_id][DATA_KEY_API]
    groups = hass.data[DOMAIN][entry.entry_id][DATA_KEY_GROUPS]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_KEY_COORDINATOR]
    
    # Create a list of fan entities
    entities = [
        AirPurifierFan(
            device=device,
            api=api,
            coordinator=coordinator
        )
        for group in groups
        for device in group['devices']
    ]

    # Add the fan entities
    async_add_entities(entities, update_before_add=True)


class AirPurifierFan(FanEntity, CoordinatorEntity):

    _preset_modes = ["Manual", "Smart", "Sleep"]

    def __init__(self, device: any, api: AirProceApi, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        self.device = device
        self._device_id = device['id']
        self.api = api

    def current_mode_id(self):
        return self.coordinator.data[self._device_id]['control']['mode']

    @property
    def name(self):
        return "Air purifier"

    @property
    def unique_id(self):
        return f"{self.device['uuid']}-fan"

    @property
    def device_info(self):
       return device_info(self.device)

    @property
    def supported_features(self):
        return FanEntityFeature.TURN_ON | FanEntityFeature.TURN_OFF | FanEntityFeature.PRESET_MODE

    @property
    def is_on(self):
        mode_id = self.current_mode_id()
        return not (mode_id >= 10 and mode_id < 20)

    @property
    def preset_modes(self):
        return self._preset_modes

    @property
    def preset_mode(self):
        mode_id = self.current_mode_id()
        if mode_id == 1:
            return 'Manual'
        elif mode_id == 2:
            return 'Smart'
        elif mode_id >= 20 and mode_id < 30:
            return 'Sleep'
        else:
            return None

    async def async_turn_on(self, **kwargs):
        await self.hass.async_add_executor_job(self.api.set_mode, self._device_id, 0)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        await self.hass.async_add_executor_job(self.api.set_mode, self._device_id, 10)
        await self.coordinator.async_request_refresh()

    async def async_set_preset_mode(self, preset_mode: str):
        match preset_mode:
            case 'Manual':
                mode_id = 1
            case 'Smart':
                mode_id = 2
            case 'Sleep':
                mode_id = 20
            case _:
                _LOGGER.error(f"Trying to set an invalid preset mode: {preset_mode}")
                return
        await self.hass.async_add_executor_job(self.api.set_mode, self._device_id, mode_id)
        await self.coordinator.async_request_refresh()
