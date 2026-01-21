"""Config flow for Yahoo Nowcast (JP) integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_API_KEY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_THRESHOLD,
    CONF_FORECAST_MINUTES,
    DEFAULT_THRESHOLD,
    DEFAULT_FORECAST_MINUTES,
)
from .api import YahooWeatherAPI

_LOGGER = logging.getLogger(__name__)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_KEY): str,
    vol.Required(CONF_LATITUDE): cv.latitude,
    vol.Required(CONF_LONGITUDE): cv.longitude,
    vol.Optional(CONF_THRESHOLD, default=DEFAULT_THRESHOLD): vol.Coerce(float),
    vol.Optional(CONF_FORECAST_MINUTES, default=DEFAULT_FORECAST_MINUTES): vol.Coerce(int),
})


class ConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for Yahoo Nowcast JP."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.error(f"Unexpected error: {err}")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=info["title"],
                    data=user_input
                )

        # Get default coordinates
        latitude = self.hass.config.latitude
        longitude = self.hass.config.longitude

        # Try to get coordinates from home zone
        try:
            for entity_id in self.hass.states.async_entity_ids("zone"):
                state = self.hass.states.get(entity_id)
                if state and "home" in entity_id.lower():
                    latitude = state.attributes.get("latitude", latitude)
                    longitude = state.attributes.get("longitude", longitude)
                    break
        except Exception:
            pass

        schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Required(CONF_LATITUDE, default=latitude): cv.latitude,
            vol.Required(CONF_LONGITUDE, default=longitude): cv.longitude,
            vol.Optional(CONF_THRESHOLD, default=DEFAULT_THRESHOLD): vol.Coerce(float),
            vol.Optional(CONF_FORECAST_MINUTES, default=DEFAULT_FORECAST_MINUTES): vol.Coerce(int),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors
        )


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""

    api = YahooWeatherAPI(
        api_key=data[CONF_API_KEY],
        latitude=data[CONF_LATITUDE],
        longitude=data[CONF_LONGITUDE],
    )

    try:
        await api.get_precipitation_forecast()
    except Exception as err:
        if "auth" in str(err).lower() or "401" in str(err):
            raise InvalidAuth(f"Invalid API key: {err}") from err
        raise CannotConnect(f"Connection failed: {err}") from err

    title = f"降水予測 ({data[CONF_LATITUDE]:.4f}, {data[CONF_LONGITUDE]:.4f})"
    return {"title": title}