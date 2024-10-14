from .const import DOMAIN


def device_info(device: any):
    return {
            "identifiers": {(DOMAIN, device['uuid'])},  # Unique identifier for this device
            "name": f"{device['model']}-{device['id']}",
            "manufacturer": "AirProce",
            "model": device['model'],
            "sw_version": device['fm']
        }