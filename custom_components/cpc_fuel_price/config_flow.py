from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

class CPCFuelPriceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for CPC Fuel Price."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(title="CPC Fuel Price", data={})
        return self.async_show_form(step_id="user", data_schema=None)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CPCFuelPriceOptionsFlow(config_entry)

class CPCFuelPriceOptionsFlow(config_entries.OptionsFlow):
    """Options flow for CPC Fuel Price."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data={})
        return self.async_show_form(step_id="init", data_schema=None)
