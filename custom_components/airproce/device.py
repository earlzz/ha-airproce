from .const import DOMAIN

def device_name(device: any) -> str:
    return f"{device['model']}-{device['id']}"

def device_info(device: any):
    return {
            "identifiers": {(DOMAIN, device['uuid'])},  # Unique identifier for this device
            "name": device_name(device),
            "manufacturer": "AirProce",
            "model": device['model'],
            "sw_version": device['fm']
        }