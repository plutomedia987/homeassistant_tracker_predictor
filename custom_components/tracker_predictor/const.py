"""Constants for the Octopus Tracker Predictor integration."""

DOMAIN = "pluto_tracker_predictor"
# DOMAIN_DATA = f"{DOMAIN}_data"
FANN_LIB = "fann_lib"
INTEGRATION_PATH = "int_path"
ANN = "ann"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Refresh frequency for the sensor
REFRESH = 1

# Polling interval (in minutes)
POLLING_INTERVALE = 10

# Increase polling frequency if withing X minutes of next departure or if train is late
HIGH_FREQUENCY_REFRESH = 7

# Tracker Formulae
TRACKER_FORMULA = "tracker_formulae"
TRACKER_REGION = "tracker_region"
