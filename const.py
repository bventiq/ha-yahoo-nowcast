"""Constants for the JMA Precipitation Nowcast integration."""

DOMAIN = "jma_precipitation_nowcast"
CONF_API_KEY = "api_key"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"
CONF_THRESHOLD = "threshold"
CONF_FORECAST_MINUTES = "forecast_minutes"

DEFAULT_THRESHOLD = 0.2
DEFAULT_FORECAST_MINUTES = 30
UPDATE_INTERVAL = 300  # 5 minutes in seconds

# Yahoo! JAPAN Weather API
API_BASE_URL = "https://map.yahooapis.jp/weather/V1/place"
API_TIMEOUT = 10

# Entity names
SENSOR_NAME = "Precipitation Forecast"
BINARY_SENSOR_NAME = "Rain Soon"
TEMPERATURE_SENSOR_NAME = "Temperature"
HUMIDITY_SENSOR_NAME = "Humidity"