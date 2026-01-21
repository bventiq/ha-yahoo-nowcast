"""Sensor platform for Yahoo Nowcast (JP)."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_NAME, TEMPERATURE_SENSOR_NAME, HUMIDITY_SENSOR_NAME

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    async_add_entities([
        PrecipitationForecastSensor(coordinator, config_entry),
        TemperatureSensor(coordinator, config_entry),
        HumiditySensor(coordinator, config_entry),
    ])

class PrecipitationForecastSensor(CoordinatorEntity, SensorEntity):
    """Representation of a precipitation forecast sensor."""
    
    def __init__(self, coordinator, config_entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = SENSOR_NAME
        self._attr_unique_id = f"{config_entry.entry_id}_precipitation_forecast"
        
    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get('current_intensity', 0)
        return 0
    
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "mm/h"
    
    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        if self.state and float(self.state) > 0:
            return "mdi:weather-rainy"
        return "mdi:weather-cloudy"
    
    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
            
        return {
            'forecasts': self.coordinator.data.get('forecasts', []),
            'last_updated': self.coordinator.data.get('last_updated'),
            'latitude': self._config_entry.data.get('latitude'),
            'longitude': self._config_entry.data.get('longitude'),
        }


class TemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a temperature sensor."""
    
    def __init__(self, coordinator, config_entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = TEMPERATURE_SENSOR_NAME
        self._attr_unique_id = f"{config_entry.entry_id}_temperature"
        
    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get('temperature')
        return None
    
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "°C"
    
    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:thermometer"
    
    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
            
        return {
            'last_updated': self.coordinator.data.get('last_updated'),
        }


class HumiditySensor(CoordinatorEntity, SensorEntity):
    """Representation of a humidity sensor."""
    
    def __init__(self, coordinator, config_entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = HUMIDITY_SENSOR_NAME
        self._attr_unique_id = f"{config_entry.entry_id}_humidity"
        
    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get('humidity')
        return None
    
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "%"
    
    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:water-percent"
    
    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
            
        return {
            'last_updated': self.coordinator.data.get('last_updated'),
        }