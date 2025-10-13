from __future__ import annotations
from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """YAML不需設定，直接啟用整合。"""
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform("sensor", DOMAIN, {}, config)
    )
    return True
