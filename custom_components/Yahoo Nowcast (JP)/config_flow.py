"""Config flow for JMA Precipitation Nowcast integration."""
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

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_KEY): str,
    vol.Optional(CONF_LATITUDE): cv.latitude,
    vol.Optional(CONF_LONGITUDE): cv.longitude,
    vol.Optional(CONF_THRESHOLD, default=DEFAULT_THRESHOLD): vol.Coerce(float),
    vol.Optional(CONF_FORECAST_MINUTES, default=DEFAULT_FORECAST_MINUTES): vol.Coerce(int),
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JMA Precipitation Nowcast."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            # 最初のゾーン（通常はhomeゾーン）の座標を取得
            latitude, longitude = await self._get_zone_coordinates()
            
            # ゾーンが見つからない場合はHome Assistantの設定値を使用
            if latitude is None:
                latitude = self.hass.config.latitude
                longitude = self.hass.config.longitude
            
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
                description_placeholders={
                    "latitude": f"{latitude:.6f}",
                    "longitude": f"{longitude:.6f}",
                    "source": "ゾーン設定" if hasattr(self, '_zone_source') else "システム設定"
                }
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def _get_zone_coordinates(self) -> tuple[float | None, float | None]:
        """Get coordinates from the first zone (usually 'home' zone)."""
        try:
            # ゾーンエンティティを取得
            zone_entities = []
            for entity_id in self.hass.states.async_entity_ids('zone'):
                state = self.hass.states.get(entity_id)
                if state and state.attributes:
                    zone_entities.append((entity_id, state))
            
            # ゾーンを優先順位でソート（home > その他のゾーン）
            def zone_priority(zone_item):
                entity_id, state = zone_item
                name = state.attributes.get('friendly_name', '').lower()
                if 'home' in entity_id.lower() or 'home' in name:
                    return 0  # 最優先
                return 1  # その他
            
            zone_entities.sort(key=zone_priority)
            
            # 最初のゾーンの座標を取得
            if zone_entities:
                entity_id, state = zone_entities[0]
                latitude = state.attributes.get('latitude')
                longitude = state.attributes.get('longitude')
                
                if latitude is not None and longitude is not None:
                    self._zone_source = True  # ゾーンから取得したことを記録
                    _LOGGER.info(f"Using coordinates from zone {entity_id}: {latitude}, {longitude}")
                    return float(latitude), float(longitude)
            
            _LOGGER.warning("No valid zone coordinates found, using system default")
            return None, None
            
        except Exception as e:
            _LOGGER.error(f"Error getting zone coordinates: {e}")
            return None, None

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    
    api = YahooWeatherAPI(
        api_key=data[CONF_API_KEY],
        latitude=data[CONF_LATITUDE],
        longitude=data[CONF_LONGITUDE],
    )
    
    try:
        await api.get_precipitation_forecast()
    except Exception as e:
        if "auth" in str(e).lower():
            raise InvalidAuth from e
        raise CannotConnect from e
    
    return {"title": f"降水予測 ({data[CONF_LATITUDE]:.4f}, {data[CONF_LONGITUDE]:.4f})"}

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""