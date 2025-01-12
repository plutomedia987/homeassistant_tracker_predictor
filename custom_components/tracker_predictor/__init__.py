"""The Octopus Tracker Predictor integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_state_change_event, Event

from .const import (
    DOMAIN,
    PLATFORMS,
    FANN_LIB,
    INTEGRATION_PATH,
    ELECTRIC_ANN,
    GAS_ANN,
)

from ctypes import *

import logging

import os, sys
import pathlib

# libfannLoc = str(list(pathlib.Path("/").glob("**/config/custom_libraries/libfann"))[0])

# if libfannLoc not in sys.path:
#     sys.path.append(libfannLoc)

# from fann2 import libfann

# from .stdout import *

from .fann.ann import ann

_LOGGER = logging.getLogger(__name__)


def setup(hass: HomeAssistant, config):
    """Setup called by HA.

    Include Fann Library
    """
    hass.data.setdefault(DOMAIN, {})

    path = pathlib.Path(__file__).parent.resolve()

    hass.data[DOMAIN][INTEGRATION_PATH] = str(path)

    hass.data[DOMAIN][ELECTRIC_ANN] = ann()
    hass.data[DOMAIN][GAS_ANN] = ann()

    hass.data[DOMAIN][ELECTRIC_ANN].create_from_fann_file(
        hass.data[DOMAIN][INTEGRATION_PATH] + "/electric_trained.net"
    )

    hass.data[DOMAIN][GAS_ANN].create_from_fann_file(
        hass.data[DOMAIN][INTEGRATION_PATH] + "/gas_trained.net"
    )

    # hass.data[DOMAIN][ELECTRIC_ANN].print_network(
    #     hass.data[DOMAIN][INTEGRATION_PATH] + "/electric.print"
    # )
    # hass.data[DOMAIN][GAS_ANN].print_network(
    #     hass.data[DOMAIN][INTEGRATION_PATH] + "/gas.print"
    # )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Octopus Tracker Predictor from a config entry."""

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
