"""CPC Fuel Price Integration"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "cpc_fuel_price"

async def async_setup(hass: HomeAssistant, config: dict):
    """YAML setup not used."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up CPC Fuel Price from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload CPC Fuel Price entry."""
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
