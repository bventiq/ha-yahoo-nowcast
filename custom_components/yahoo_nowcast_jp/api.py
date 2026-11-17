"""Yahoo! Weather API client."""
import aiohttp
import json
import math
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

REQUIRED_SPAN_MINUTES = 60
STEP_MINUTES = 10
MAX_DATA_AGE_MINUTES = 20
JST = timezone(timedelta(hours=9))


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
                    text = await response.text()
                    raise Exception(f"API request failed with status {response.status}: {text}")
                
                data = await response.json()
                return self._parse_forecast_data(data)
    
    def _parse_forecast_data(self, data: Dict) -> Dict:
        """Parse the API response to extract forecast data."""
        try:
            features = data.get('Feature')
            if not features:
                raise ValueError("missing Feature")
            weather_data = features[0]['Property']['WeatherList']['Weather']
            if not weather_data:
                raise ValueError("empty Weather list")

            now = datetime.now(JST)
            forecasts = []

            for weather in weather_data:
                # Date is "YYYYMMDDHHMM" in JST
                forecast_dt = datetime.strptime(
                    str(weather['Date']), '%Y%m%d%H%M'
                ).replace(tzinfo=JST)
                intensity = float(weather['Rainfall'])
                if not math.isfinite(intensity) or intensity < 0:
                    raise ValueError(f"invalid Rainfall: {intensity}")
                delta_min = (forecast_dt - now).total_seconds() / 60
                # Elapsed entries are negative/zero; future ones round up so
                # that a not-yet-reached time never counts as "now".
                minutes = math.ceil(delta_min) if delta_min > 0 else 0
                is_past = delta_min <= 0

                forecasts.append({
                    'time': forecast_dt.strftime('%H:%M'),
                    'datetime': forecast_dt.isoformat(),
                    'time_minutes': minutes,
                    '_past': is_past,
                    'intensity': intensity,
                })

            times = [datetime.fromisoformat(f['datetime']) for f in forecasts]
            steps = {(t2 - t1).total_seconds() / 60 for t1, t2 in zip(times, times[1:])}
            if steps != {STEP_MINUTES}:
                raise ValueError(f"unexpected forecast intervals: {sorted(steps)}")
            span = (times[-1] - times[0]).total_seconds() / 60
            if span < REQUIRED_SPAN_MINUTES:
                raise ValueError(
                    f"forecast covers only {span:.0f} min (need {REQUIRED_SPAN_MINUTES})"
                )
            age = (now - times[0]).total_seconds() / 60
            if age > MAX_DATA_AGE_MINUTES:
                raise ValueError(f"forecast data is stale ({age:.0f} min old)")

            # Drop already-elapsed entries except the latest one, which
            # represents the current state (time_minutes = 0).
            future = [f for f in forecasts if not f['_past']]
            past = [f for f in forecasts if f['_past']]
            if not past:
                raise ValueError("no current observation (all entries are in the future)")
            forecasts = [past[-1]] + future
            for f in forecasts:
                del f['_past']

            return {
                'forecasts': forecasts,
                'last_updated': now.isoformat(),
                'coverage_minutes': max(0, math.floor((times[-1] - now).total_seconds() / 60)),
                'current_intensity': forecasts[0]['intensity'],
            }

        except (KeyError, IndexError, TypeError, ValueError) as e:
            raise Exception(f"Failed to parse API response: {e}")
