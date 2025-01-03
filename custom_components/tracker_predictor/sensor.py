"""Platform for sensor integration."""

from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta

import async_timeout

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.core import HomeAssistant

from .predict import OctopusTrackerPredict

from .const import DOMAIN, POLLING_INTERVALE, REFRESH, TRACKER_FORMULA, TRACKER_REGION

from .tracker_calc import Octopus_Tracker_Calc

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Config entry example."""

    coordinator = OctopusTrackerPredictionCoordinator(
        hass, entry.data.get(TRACKER_REGION), entry.data.get(TRACKER_FORMULA)
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([OctopusTrackerPrediction(coordinator)])


class OctopusTrackerPredictionCoordinator(DataUpdateCoordinator):
    """Octopus Tracker Prediction Coordinator"""

    description: str = None
    friendly_name: str = None
    sensor_name: str = None

    def __init__(self, hass: HomeAssistant, region, formula):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(minutes=REFRESH),
        )

        self.region = region
        self.formula = formula

        self.my_api = OctopusTrackerPredict(hass)
        self.octo_tracker_calc = Octopus_Tracker_Calc()

        self.last_data_refresh = None

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        # chek whether we should refresh the data of not
        if (
            self.last_data_refresh is None
            or (
                self.last_data_refresh is not None
                and (time.time() - self.last_data_refresh) > POLLING_INTERVALE * 60
            )
            # or (
            #     self.data["next_train_scheduled"] is not None
            #     and datetime.now(self.data["next_train_scheduled"].tzinfo)
            #     >= self.data["next_train_scheduled"]
            #     - timedelta(minutes=HIGH_FREQUENCY_REFRESH)
            #     and not self.data["next_train_expected"] == "Cancelled"
            # )
        ):
            # try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with async_timeout.timeout(30):
                data = await self.my_api.async_get_data(self.hass)
                for i in range(0, len(data["data"]), 1):
                    data["data"][i]["octopus_price"] = self.octo_tracker_calc.calc(
                        self.region, self.formula, data["data"][i]["price_prediction"]
                    )

                self.last_data_refresh = time.time()
            # except aiohttp.ClientError as err:
            #    raise UpdateFailed(f"Error communicating with API: {err}") from err

            if self.sensor_name is None:
                self.sensor_name = f"octo_tracker_14_predic_{self.octo_tracker_calc.get_formula_name_by_key(self.formula)}_{self.octo_tracker_calc.get_region_name_by_key(self.region)}"

            # if self.description is None:
            #     self.description = (
            #         f"Departing/Arriving trains schedule at {data['station']} station"
            #     )

            if self.friendly_name is None:
                self.friendly_name = f"Octopus Tracker 14 Day Prediction For {self.octo_tracker_calc.get_formula_name_by_key(self.formula)} in {self.octo_tracker_calc.get_region_name_by_key(self.region)}"

            data["name"] = self.sensor_name
            # data["description"] = self.description
            # data["friendly_name"] = self.friendly_name
        else:
            data = self.data

        return data


class OctopusTrackerPrediction(CoordinatorEntity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available

    """

    attribution = "This predicts the next 14 tracker prices"

    def __init__(self, coordinator):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.entity_id = f"sensor.{coordinator.data['name'].lower()}"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self.coordinator.data

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        return self.coordinator.data["name"]

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.last_data_refresh
