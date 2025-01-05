"""The Octopus Tracker Predictor integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS, FANN_LIB, INTEGRATION_PATH, ANN

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
    # hass.data[DOMAIN][FANN_LIB] = CDLL(str(path) + "/libfann/libfloatfann.so.2.2.0")

    # filename = create_string_buffer(
    #     bytes(hass.data[DOMAIN][INTEGRATION_PATH] + "/trained.net", "utf-8")
    # )

    # hass.data[DOMAIN][FANN_LIB].fann_create_from_file.argtypes = [c_char_p]
    # hass.data[DOMAIN][FANN_LIB].fann_create_from_file.returntype = c_void_p

    # with capture_c_stdout():
    # hass.data[DOMAIN][ANN] = hass.data[DOMAIN][FANN_LIB].fann_create_from_file(filename)
    # hass.data[DOMAIN][FANN_LIB] = libfann.neural_net()
    # createdAnn = hass.data[DOMAIN][FANN_LIB].create_from_file(
    #     hass.data[DOMAIN][INTEGRATION_PATH] + "/trained.net"
    # )

    # print("Created ANN: ", createdAnn)

    neural_net = ann()

    hass.data[DOMAIN][ANN] = neural_net

    # neural_net.create_standard(3, (3, 3, 3))
    neural_net.create_from_fann_file(
        hass.data[DOMAIN][INTEGRATION_PATH] + "/trained.net"
    )

    # neural_net.print_network(hass.data[DOMAIN][INTEGRATION_PATH] + "/network.txt")

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
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        # hass.data[DOMAIN].pop(entry.entry_id)

        hass.data[DOMAIN][FANN_LIB].fann_destroy(hass.data[DOMAIN][ANN])

    return unload_ok
