import logging
from .device import device_info, device_name
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import UnitOfTemperature, PERCENTAGE, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from .const import DOMAIN, DATA_KEY_API, DATA_KEY_GROUPS, DATA_KEY_COORDINATOR


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    groups = hass.data[DOMAIN][entry.entry_id][DATA_KEY_GROUPS]
    coordinator = hass.data[DOMAIN][entry.entry_id][DATA_KEY_COORDINATOR]

    # Create sensor entities based on the available data
    sensors = []
    for group in groups:
        for device in group['devices']:
            sensors.extend([
                AirPurifierPm25Sensor(
                    device=device,
                    coordinator=coordinator
                ),
                AirPurifierPm10Sensor(
                    device=device,
                    coordinator=coordinator
                ),
                AirPurifierVocSensor(
                    device=device,
                    coordinator=coordinator
                ),
            ])

    async_add_entities(sensors, update_before_add=True)


class AirPurifierTempSensor(CoordinatorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = 'mdi:thermometer'

    def __init__(self, device: any, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        self.device = device
        self._device_id = device['id']

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.device['uuid']}-temp"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{device_name(self.device)} - Temperature"

    @property
    def device_info(self):
       return device_info(self.device)

    @property
    def state(self):
        """Return the current temperature."""
        return int(self.coordinator.data[self._device_id]['status']['temperature']) / 10


class AirPurifierHumiditySensor(CoordinatorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_icon = 'mdi:water-percent'

    def __init__(self, device: any, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        self.device = device
        self._device_id = device['id']

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.device['uuid']}-humidity"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{device_name(self.device)} - Humidity"

    @property
    def device_info(self):
       return device_info(self.device)

    @property
    def state(self):
        """Return the current temperature."""
        return int(self.coordinator.data[self._device_id]['status']['humidity']) / 10


class AirPurifierPm25Sensor(CoordinatorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.PM25
    _attr_native_unit_of_measurement = CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    _attr_icon = 'mdi:chart-scatter-plot'

    def __init__(self, device: any, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        self.device = device
        self._device_id = device['id']

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.device['uuid']}-pm25"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{device_name(self.device)} - PM2.5"

    @property
    def device_info(self):
       return device_info(self.device)

    @property
    def state(self):
        """Return the current temperature."""
        return int(self.coordinator.data[self._device_id]['status']['pm25'])


class AirPurifierPm10Sensor(CoordinatorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.PM10
    _attr_native_unit_of_measurement = CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    _attr_icon = 'mdi:chart-scatter-plot-hexbin'

    def __init__(self, device: any, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        self.device = device
        self._device_id = device['id']

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.device['uuid']}-pm10"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{device_name(self.device)} - PM10"

    @property
    def device_info(self):
       return device_info(self.device)

    @property
    def state(self):
        """Return the current temperature."""
        return int(self.coordinator.data[self._device_id]['status']['pm10'])


class AirPurifierVocSensor(CoordinatorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS
    _attr_native_unit_of_measurement = CONCENTRATION_MILLIGRAMS_PER_CUBIC_METER
    _attr_icon = 'mdi:molecule'

    def __init__(self, device: any, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        self.device = device
        self._device_id = device['id']

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.device['uuid']}-voc"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{device_name(self.device)} - VOC"

    @property
    def device_info(self):
       return device_info(self.device)

    @property
    def state(self):
        """Return the current temperature."""
        return int(self.coordinator.data[self._device_id]['status']['voc']) / 1000
