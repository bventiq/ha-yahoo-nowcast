"""Binary sensor platform for JMA Precipitation Nowcast."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, BINARY_SENSOR_NAME, CONF_THRESHOLD, CONF_FORECAST_MINUTES

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    async_add_entities([
        RainSoonBinarySensor(coordinator, config_entry)
    ])

class RainSoonBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a rain soon binary sensor."""
    
    def __init__(self, coordinator, config_entry):
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = BINARY_SENSOR_NAME
        self._attr_unique_id = f"{config_entry.entry_id}_rain_soon"
        self._attr_device_class = BinarySensorDeviceClass.MOISTURE
        
    @property
    def is_on(self):
        """Return true if rain is expected soon."""
        if not self.coordinator.data:
            return False
            
        threshold = self._config_entry.data.get(CONF_THRESHOLD, 0.2)
        forecast_minutes = self._config_entry.data.get(CONF_FORECAST_MINUTES, 30)
        
        forecasts = self.coordinator.data.get('forecasts', [])
        
        for forecast in forecasts:
            if forecast['time_minutes'] <= forecast_minutes:
                if forecast['intensity'] >= threshold:
                    return True
        
        return False
    
    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        if self.is_on:
            return "mdi:weather-pouring"
        return "mdi:weather-sunny"
    
    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
            
        threshold = self._config_entry.data.get(CONF_THRESHOLD, 0.2)
        forecast_minutes = self._config_entry.data.get(CONF_FORECAST_MINUTES, 30)
        
        forecasts = self.coordinator.data.get('forecasts', [])
        
        # 雨が降り始めるまでの時間と最大強度を計算
        raining_in_minutes = None
        max_intensity = 0
        
        for forecast in forecasts:
            if forecast['time_minutes'] <= forecast_minutes:
                if forecast['intensity'] >= threshold:
                    if raining_in_minutes is None:
                        raining_in_minutes = forecast['time_minutes']
                    max_intensity = max(max_intensity, forecast['intensity'])
        
        return {
            'raining_in_minutes': raining_in_minutes,
            'max_intensity': max_intensity,
            'threshold': threshold,
            'forecast_minutes': forecast_minutes,
        }