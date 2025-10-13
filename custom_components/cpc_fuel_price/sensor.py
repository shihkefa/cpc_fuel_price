import logging
import aiohttp
import async_timeout
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN, API_URL

_LOGGER = logging.getLogger(__name__)

PRODUCTS = [
    {"name": "CPC Product 98 Prices", "index": 0},
    {"name": "CPC Product 95 Prices", "index": 1},
    {"name": "CPC Product 92 Prices", "index": 2},
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up CPC Fuel Price sensors from a config entry."""
    sensors = [CPCFuelPriceSensor(p["name"], p["index"]) for p in PRODUCTS]
    async_add_entities(sensors, True)

class CPCFuelPriceSensor(SensorEntity):
    """Representation of a CPC Fuel Price Sensor."""

    def __init__(self, name, index):
        self._name = name
        self._index = index
        self._state = None
        self._attrs = {}

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return f"cpc_fuel_price_{self._index}"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attrs

    async def async_update(self):
        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.get(API_URL, ssl=False) as resp:
                        data = await resp.json()

            if data and len(data) > self._index:
                item = data[self._index]
                self._state = item.get("參考牌價_金額")
                self._attrs = {
                    "型別名稱": item.get("型別名稱"),
                    "產品編號": item.get("產品編號"),
                    "產品名稱": item.get("產品名稱"),
                    "參考牌價": item.get("參考牌價"),
                    "牌價生效日期": item.get("牌價生效日期"),
                }

        except Exception as e:
            _LOGGER.error("Failed to update CPC Fuel Price sensor: %s", e)
