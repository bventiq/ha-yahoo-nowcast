"""Yahoo! Weather API client."""
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class YahooWeatherAPI:
    """Yahoo! Weather API client."""
    
    def __init__(self, api_key: str, latitude: float, longitude: float, timeout: int = 10):
        """Initialize the API client."""
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.timeout = timeout
        self.base_url = "https://map.yahooapis.jp/weather/V1/place"
        
    async def get_precipitation_forecast(self) -> Dict:
        """Get precipitation forecast data."""
        params = {
            'coordinates': f"{self.longitude},{self.latitude}",
            'appid': self.api_key,
            'output': 'json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base_url,
                params=params,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                if response.status != 200:
                    raise Exception(f"API request failed with status {response.status}")
                
                data = await response.json()
                return self._parse_forecast_data(data)
    
    def _parse_forecast_data(self, data: Dict) -> Dict:
        """Parse the API response to extract forecast data."""
        try:
            feature = data.get('Feature', [{}])[0]
            weather_data = feature.get('Property', {}).get('WeatherList', {}).get('Weather', [])
            weather_info = feature.get('Property', {}).get('Weather', [])
            
            forecasts = []
            current_time = datetime.now()
            
            for i, weather in enumerate(weather_data[:6]):  # 最大6時間分
                forecast_time = current_time + timedelta(minutes=i * 10)
                intensity = float(weather.get('Rainfall', 0))
                
                forecasts.append({
                    'time': forecast_time.strftime('%H:%M'),
                    'time_minutes': i * 10,
                    'intensity': intensity
                })
            
            # 現在の気温と湿度を抽出
            current_temp = None
            current_humidity = None
            
            if weather_info:
                current_weather = weather_info[0]
                current_temp = float(current_weather.get('Temperature', 0)) if current_weather.get('Temperature') else None
                current_humidity = int(current_weather.get('Humidity', 0)) if current_weather.get('Humidity') else None
            
            return {
                'forecasts': forecasts,
                'last_updated': current_time.isoformat(),
                'current_intensity': forecasts[0]['intensity'] if forecasts else 0,
                'temperature': current_temp,
                'humidity': current_humidity
            }
            
        except (KeyError, IndexError, ValueError) as e:
            raise Exception(f"Failed to parse API response: {e}")