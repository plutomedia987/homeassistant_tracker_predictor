"""Config flow for National Rail UK integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import selector

from .const import DOMAIN, TRACKER_FORMULA, TRACKER_REGION

from .tracker_calc_electric import Octopus_Tracker_Calc_Electric

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(TRACKER_FORMULA): selector(
            {
                "select": {
                    "options": Octopus_Tracker_Calc_Electric.get_formulae_selector(),
                }
            }
        ),
        vol.Required(TRACKER_REGION): selector(
            {
                "select": {
                    "options": Octopus_Tracker_Calc_Electric.get_regions_selector(),
                }
            }
        ),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.

    # validate the token by calling a known line

    # try:
    #     my_api = NationalRailClient(data[CONF_TOKEN], "STP", ["ZFD"])
    #     res = await my_api.async_get_data()
    # except NationalRailClientInvalidToken as err:
    #     _LOGGER.exception(err)
    #     raise InvalidToken() from err

    # # validate station input

    # try:
    #     my_api = NationalRailClient(
    #         data[CONF_TOKEN], data[CONF_STATION], data[CONF_DESTINATIONS].split(",")
    #     )
    #     res = await my_api.async_get_data()
    # except NationalRailClientInvalidInput as err:
    #     _LOGGER.exception(err)
    #     raise InvalidInput() from err

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    return {
        "title": f"Tracker Prediction for {data[TRACKER_REGION]} {data[TRACKER_FORMULA]}"
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for National Rail UK."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )
