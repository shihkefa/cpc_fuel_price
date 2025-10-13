from __future__ import annotations
import aiohttp
import async_timeout
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN, API_URL, PRODUCT_INDEX

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = 3600  # 每小時更新

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """啟動時自動建立三個感測器實體。"""
    coordinator = CPCDataCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    entities = [
        CPCSensor(coordinator, fuel_type, index)
        for fuel_type, index in PRODUCT_INDEX.items()
    ]
    async_add_entities(entities, True)


class CPCDataCoordinator(DataUpdateCoordinator):
    """負責抓取 CPC API 資料"""

    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name="CPC Fuel Price",
            update_interval=dt_util.timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.get(API_URL, ssl=False) as resp:
                        return await resp.json()
        except Exception as e:
            _LOGGER.error("CPC油價更新失敗: %s", e)
            return None


class CPCSensor(CoordinatorEntity, SensorEntity):
    """CPC 油價感測器"""

    def __init__(self, coordinator, fuel_type: str, index: int):
        super().__init__(coordinator)
        self._fuel_type = fuel_type
        self._index = index
        self._attr_name = f"CPC {fuel_type} 無鉛汽油"
        self._attr_unique_id = f"cpc_{fuel_type}_price"
        self._attr_icon = "mdi:gas-station"

    @property
    def native_unit_of_measurement(self):
        return "元/公升"

    @property
    def state(self):
        data = self.coordinator.data
        if not data:
            return None
        return data[self._index].get("參考牌價_金額")

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        if not data:
            return {}
        p = data[self._index]
        return {
            "型別名稱": p.get("型別名稱"),
            "產品名稱": p.get("產品名稱"),
            "產品編號": p.get("產品編號"),
            "牌價生效日期": p.get("牌價生效日期"),
            "包裝": p.get("包裝"),
            "計價單位": p.get("計價單位"),
        }
