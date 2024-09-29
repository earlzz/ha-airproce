import logging
from datetime import timedelta
from .api import AirPorceApi
from .const import DOMAIN, CONFIG_KEY_TOKEN, DATA_KEY_API, DATA_KEY_GROUPS, DATA_KEY_COORDINATOR
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up from a config entry."""
    # Read the token from the entry's data
    # Initialize your API client with the provided token
    api = AirPorceApi(token=entry.data[CONFIG_KEY_TOKEN])
    
    # Fetch the groups
    response = await hass.async_add_executor_job(api.list_groups)
    if response is None or response.get('data') is None:
        return False
    
    groups = response.get('data')

    device_id_list = [
        device['id']
        for group in groups
        for device in group['devices']
    ]

    async def async_get_devices_status():
        return await hass.async_add_executor_job(api.get_devices_status, device_id_list)

    coordinator = DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name="airporce_devices_status",
        update_method=async_get_devices_status,
        update_interval=timedelta(seconds=60),  # Update frequency
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        DATA_KEY_API: api,
        DATA_KEY_GROUPS: groups,
        DATA_KEY_COORDINATOR: coordinator
    }

    # Forward the setup to your platform(s)
    await hass.config_entries.async_forward_entry_setups(entry, ['fan', 'sensor'])

    return True

async def async_unload_entry(hass, entry):
    """Handle unloading of an entry."""
    api = hass.data[DOMAIN][entry.entry_id][DATA_KEY_API]
    await hass.async_add_executor_job(api.user_logout)
    return True
