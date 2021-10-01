from models.validation_error import ValidationError
from connectors.openweather_connector import OpenWeatherConnector
from typing import Optional
from infrastructure import weather_cache

class LocationService:
    async def get_report_async(
        city: str,
        state: Optional[str] = None,
        country: Optional[str] = "BR",
        units: Optional[str] = "metric",
        lang: Optional[str] = "pt_br"
    ) -> dict:
        try:
            valid_units = {'standard', 'metric', 'imperial'}
            if units not in valid_units:
                msg = f"Invalid unit {units}, it must be one of {valid_units}"
                raise ValidationError(status_code=400, error_msg=msg)

            if len(country) != 2:
                raise ValidationError(status_code=400, error_msg='Country must be alpha-2 code')

            forecast = weather_cache.get_weather(city, state, country, units)
            if forecast:
                return forecast

            openweather_connector = OpenWeatherConnector(
                city=city, state=state, country=country, units=units, lang="pt_br")
            report = await openweather_connector.send_async()
            report = report.json()
            report_main = report["main"]

            weather_cache.set_weather(city, state, country, units, report_main)
            return report_main
        except Exception as e:
            raise e
