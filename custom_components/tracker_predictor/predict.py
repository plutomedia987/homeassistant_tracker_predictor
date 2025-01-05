"""Octopus Tracker Prediction based on Wind, Solar and Demand forcasts"""

from .const import DOMAIN, FANN_LIB, ANN

# from ctypes import *

from homeassistant.core import HomeAssistant, State

from datetime import time, datetime, date, timedelta, tzinfo

import string

import pytz

# from .stdout import *

from .fann.ann import ann


class OctopusTrackerPredict:
    def __init__(self, hass):
        """Initialise the neural network."""

        self.fann: ann = hass.data[DOMAIN][ANN]

        self.MAX_WIND = 30000
        self.MIN_WIND = 0
        self.MAX_SOLAR = 15000
        self.MIN_SOLAR = 0
        self.MAX_DEMAND = 60000
        self.MIN_DEMAND = 10000
        self.MAX_PRICE = 100
        self.MIN_PRICE = -20

    async def async_get_data(self, hass: HomeAssistant):
        """Called by HA to update the sensor."""

        wind_sensor = hass.states.get("sensor.national_grid_wind_forecast_fourteen_day")

        solar_sensor = hass.states.get(
            "sensor.national_grid_embedded_solar_forecast_fourteen_day"
        )
        demand_sensor = hass.states.get(
            "sensor.national_grid_grid_demand_fourteen_day_forecast"
        )

        base = datetime.combine(date.today(), time.min, pytz.UTC)
        date_list = [base + timedelta(days=x) for x in range(1, 14, 1)]

        inputs = []
        for dateVal in date_list:
            wind = self.getData(wind_sensor, dateVal, "generation")
            solar = self.getData(solar_sensor, dateVal, "generation")
            demand = self.getData(demand_sensor, dateVal, "national_demand")

            prediction = self.denormalise_price(
                list(
                    self.fann.run(
                        tuple(
                            self.normalise_wind(wind)
                            + self.normalise_solar(solar)
                            + self.normalise_demand(demand)
                        )
                    )
                )
            )

            inputs.append(
                {
                    "date": dateVal,
                    "wind": wind,
                    "solar": solar,
                    "demand": demand,
                    "price_prediction": prediction,
                }
            )

        return {"data": inputs}

    def getData(self, sensor: State, dateVal: datetime, retKey: string):
        """Get the correct data from the national grid sensor based on date/time."""

        timeHigh = dateVal + timedelta(hours=22)

        return [
            x[retKey]
            for x in sensor.attributes["forecast"]
            if x["start_time"] >= dateVal and x["start_time"] <= timeHigh
        ]

    def normalise_wind(self, arr: list):
        """Normalise the wind value between max and min wind constants."""

        return [((x - self.MIN_WIND) / (self.MAX_WIND - self.MIN_WIND)) for x in arr]

    def normalise_solar(self, arr: list):
        """Normalise the solar value between max and min solar constants."""

        return [((x - self.MIN_SOLAR) / (self.MAX_SOLAR - self.MIN_SOLAR)) for x in arr]

    def normalise_demand(self, arr: list):
        """Normalise the demand value between max and min demand constants."""

        return [
            ((x - self.MIN_DEMAND) / (self.MAX_DEMAND - self.MIN_DEMAND)) for x in arr
        ]

    def denormalise_price(self, prediction: list):
        """Denormalise the price prediction value between max and min price constants."""

        return ((prediction[0] + 1) / 2) * (
            self.MAX_PRICE - self.MIN_PRICE
        ) + self.MIN_PRICE
