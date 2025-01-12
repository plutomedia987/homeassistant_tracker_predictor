"""Octopus Tracker Prediction based on Wind, Solar and Demand forcasts"""

from .const import DOMAIN, ELECTRIC_ANN, GAS_ANN

# from ctypes import *

from homeassistant.core import HomeAssistant, State
from homeassistant.helpers import event

from datetime import time, datetime, date, timedelta, tzinfo

import string

import pytz

# from .stdout import *

from .fann.ann import ann

from homeassistant.components.weather import WeatherEntityFeature


class OctopusTrackerPredict:
    def __init__(self, hass):
        """Initialise the neural network."""

        self.electric_ann: ann = hass.data[DOMAIN][ELECTRIC_ANN]
        self.gas_ann: ann = hass.data[DOMAIN][GAS_ANN]

        self.MAX_WIND = 30000
        self.MIN_WIND = 0
        self.MAX_SOLAR = 15000
        self.MIN_SOLAR = 0
        self.MAX_DEMAND = 60000
        self.MIN_DEMAND = 10000
        self.MAX_ELECTRIC_PRICE = 100
        self.MIN_ELECTRIC_PRICE = -20
        self.MAX_GAS_PRICE = 20
        self.MIN_GAS_PRICE = -20
        self.MAX_TEMP = 50
        self.MIN_TEMP = -20

    async def async_get_data(self, hass: HomeAssistant):
        """Called by HA to update the sensor."""

        wind_sensor = hass.states.get("sensor.national_grid_wind_forecast_fourteen_day")

        solar_sensor = hass.states.get(
            "sensor.national_grid_embedded_solar_forecast_fourteen_day"
        )
        demand_sensor = hass.states.get(
            "sensor.national_grid_grid_demand_fourteen_day_forecast"
        )

        # forcast_sensor = hass.states.get("weather.get_forecast")
        # hass.bus.async_fire("weather.get_forecasts")

        # print(forcast_sensor)

        daily_forecast = await hass.services.async_call(
            "weather",
            "get_forecasts",
            {"type": "daily", "entity_id": "weather.forecast_home"},
            blocking=True,
            return_response=True,
        )

        base = datetime.combine(date.today(), time.min, pytz.UTC)
        date_list = [base + timedelta(days=x) for x in range(1, 14, 1)]

        electric = []
        for dateVal in date_list:
            wind = self.getData(wind_sensor, dateVal, "generation")
            solar = self.getData(solar_sensor, dateVal, "generation")
            demand = self.getData(demand_sensor, dateVal, "national_demand")
            # prediction = 0
            prediction = self.denormalise_electric_price(
                list(
                    self.electric_ann.run(
                        tuple(
                            self.normalise_wind(wind)
                            + self.normalise_solar(solar)
                            + self.normalise_demand(demand)
                        )
                    )
                )
            )

            electric.append(
                {
                    "date": dateVal,
                    # "wind": wind,
                    # "solar": solar,
                    # "demand": demand,
                    "price_prediction": prediction,
                }
            )

        gas = []

        gas_inputs = [
            x["temperature"]
            for x in daily_forecast["weather.forecast_home"]["forecast"]
        ]

        # Trained for one too many. Bodge for now
        gas_inputs.append(sum(gas_inputs) / len(gas_inputs))
        # gas_inputs = self.normalise_temperature(gas_inputs)

        # print(gas_inputs)
        # print(self.normalise_temperature(gas_inputs))
        # print(self.gas_ann.run(self.normalise_temperature(gas_inputs)))

        prediction = self.denormalise_gas_price(
            list(self.gas_ann.run(self.normalise_temperature(gas_inputs)))
        )

        print(prediction)

        gas = [
            {"date": base + timedelta(days=i), "price_prediction": prediction[i]}
            for i in range(0, len(prediction) - 1, 1)
        ]

        return {"electric_data": electric, "gas_data": gas}

    def getData(self, sensor: State, dateVal: datetime, retKey: string) -> list:
        """Get the correct data from the national grid sensor based on date/time."""

        timeHigh = dateVal + timedelta(hours=22)

        return [
            x[retKey]
            for x in sensor.attributes["forecast"]
            if x["start_time"] >= dateVal and x["start_time"] <= timeHigh
        ]

    def normalise_wind(self, arr: list) -> list:
        """Normalise the wind value between max and min wind constants."""

        return [((x - self.MIN_WIND) / (self.MAX_WIND - self.MIN_WIND)) for x in arr]

    def normalise_solar(self, arr: list) -> list:
        """Normalise the solar value between max and min solar constants."""

        return [((x - self.MIN_SOLAR) / (self.MAX_SOLAR - self.MIN_SOLAR)) for x in arr]

    def normalise_demand(self, arr: list) -> list:
        """Normalise the demand value between max and min demand constants."""

        return [
            ((x - self.MIN_DEMAND) / (self.MAX_DEMAND - self.MIN_DEMAND)) for x in arr
        ]

    def denormalise_electric_price(self, prediction: list) -> float:
        """Denormalise the price prediction value between max and min price constants."""

        return ((prediction[0] + 1) / 2) * (
            self.MAX_ELECTRIC_PRICE - self.MIN_ELECTRIC_PRICE
        ) + self.MIN_ELECTRIC_PRICE

    def denormalise_gas_price(self, predictions: list) -> list:
        """Denormalise the price prediction value between max and min price constants."""

        return [
            ((x + 1) / 2) * (self.MAX_GAS_PRICE - self.MIN_GAS_PRICE)
            + self.MIN_GAS_PRICE
            for x in predictions
        ]

    def normalise_temperature(self, arr: list) -> list:
        """Normalise the demand value between max and min demand constants."""

        return [
            ((((x - self.MIN_TEMP) / (self.MAX_TEMP - self.MIN_TEMP)) * 2) - 1)
            for x in arr
        ]
