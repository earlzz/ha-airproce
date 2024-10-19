# ha-airproce
Custom Home Assistant integration for AirProce air purifiers.

## Install / Update

1. Open HACS, open the menu on the top-right corner, and click "Custom repositories"
2. Fill in `https://github.com/jackjinke/ha-airproce` for "Repositories" and `Integrations` for "Type", click "ADD"
3. In HACS, search for "AirProce air purifiers" (or click [this link](https://my.home-assistant.io/redirect/hacs_repository/?owner=jackjinke&repository=ha-airproce))
4. Install the integration
5. Restart Home Assistant (Settings -> System -> Power icon at top-right corner -> Restart Home Assistant)
6. Setup integration (Settings -> Device & Services -> Add integration (bottom-right) -> AirProce)

## Development

Run `pip install homeassistant` to install dependencies.