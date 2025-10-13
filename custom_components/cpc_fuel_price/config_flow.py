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
