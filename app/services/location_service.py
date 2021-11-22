from typing import Optional

from connectors.openweather_connector import OpenWeatherConnector
from dto.weather_dto import ReportResponseDTO
from infrastructure import weather_cache
from models.validation_error import ValidationError
from utils.logger import Logger


class LocationService:
    def __init__(self, logger: Optional[Logger] = None) -> None:
        self.logger = Logger(class_name=__name__) if logger is None else logger
    
    async def get_report_async(
        self,
        city: str,
        state: Optional[str] = None,
        country: Optional[str] = "BR",
        units: Optional[str] = "metric",
        lang: Optional[str] = "pt_br",
    ) -> dict:
        try:
            self.logger.debug(f"Weather Request for {city}")
            valid_units = {"standard", "metric", "imperial"}
            if units not in valid_units:
                self.logger.warning(f"Invalid unit sent ({units})")
                msg = f"Invalid unit {units}, it must be one of {valid_units}"
                raise ValidationError(status_code=400, error_msg=msg)

            if len(country) != 2:
                raise ValidationError(status_code=400, error_msg="Country must be alpha-2 code")

            search = dict(
                city=city,
                state=state,
                country=country
            )

            forecast = weather_cache.get_weather(city, state, country, units)
            if forecast:
                return self.__generate_response(response=forecast, search=search)

            self.logger.debug(f"No weather cached for {city}, using connector to OpenWeather")
            openweather_connector = OpenWeatherConnector(
                city=city, state=state, country=country, units=units, lang=lang
            )
            report = await openweather_connector.send_async()
            report = report.json()
            report_main = report["main"]

            weather_cache.set_weather(city, state, country, units, report_main)
            return self.__generate_response(response=report_main, search=search)
        except Exception as e:
            raise e

    def __generate_response(self, response: dict, search: dict):
        self.logger.debug(f"Generating weather RESPONSE DTO")
        response.update(search)
        return ReportResponseDTO(**response).dict()
