import logging
import aiohttp
import async_timeout
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.util import dt as dt_util

from .const import DOMAIN, API_URL, PRODUCTS

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(hours=1)  # 每小時更新

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up CPC Fuel Price sensors from a config entry."""
    coordinator = CPCDataCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    sensors = [CPCSensor(coordinator, p["name"], p["index"]) for p in PRODUCTS]
    async_add_entities(sensors, True)

class CPCDataCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch CPC API data."""

    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name="CPC Fuel Price",
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        """Fetch data from CPC API."""
        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.get(API_URL, ssl=False) as resp:
                        return await resp.json()
        except Exception as e:
            _LOGGER.error("CPC Fuel Price update failed: %s", e)
            return None

class CPCSensor(CoordinatorEntity, SensorEntity):
    """Representation of a CPC Fuel Price sensor."""

    def __init__(self, coordinator, name, index):
        super().__init__(coordinator)
        self._name = name
        self._index = index
        self._attr_name = name
        self._attr_unique_id = f"cpc_fuel_price_{index}"
        self._attr_icon = "mdi:gas-station"
        self._attr_native_unit_of_measurement = "元/公升"
        self._attr_state_class = "measurement"

    @property
    def state(self):
        data = self.coordinator.data
        if not data or len(data) <= self._index:
            return None
        return data[self._index].get("參考牌價_金額")

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        if not data or len(data) <= self._index:
            return {}
        p = data[self._index]
        return {
            "型別名稱": p.get("型別名稱"),
            "產品編號": p.get("產品編號"),
            "產品名稱": p.get("產品名稱"),
            "參考牌價": p.get("參考牌價_金額"),
            "牌價生效日期": p.get("牌價生效日期"),
            "包裝": p.get("包裝"),
            "計價單位": p.get("計價單位"),
        }

