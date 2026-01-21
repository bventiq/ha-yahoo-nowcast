"""The JMA Precipitation Nowcast integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL, API_BASE_URL, API_TIMEOUT
from .api import YahooWeatherAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up JMA Precipitation Nowcast from a config entry."""
    
    # APIクライアントの初期化
    api = YahooWeatherAPI(
        api_key=entry.data["api_key"],
        latitude=entry.data["latitude"],
        longitude=entry.data["longitude"],
        timeout=API_TIMEOUT
    )
    
    # データ更新コーディネーターの作成
    coordinator = JMAPrecipitationCoordinator(hass, api)
    
    # 初回データ取得
    await coordinator.async_config_entry_first_refresh()
    
    # データをhassに保存
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # プラットフォームの設定
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        
    return unload_ok

class JMAPrecipitationCoordinator(DataUpdateCoordinator):
    """Class to manage fetching precipitation data from Yahoo! Weather API."""
    
    def __init__(self, hass: HomeAssistant, api: YahooWeatherAPI) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.api = api
        
    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            return await self.api.get_precipitation_forecast()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err