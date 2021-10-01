from models.validation_error import ValidationError
from connectors.base_async_connector import BaseAsyncConnector
from fastapi import HTTPException
from httpx import Response
from env_config import settings



class OpenWeatherConnector(BaseAsyncConnector):
    def __init__(self, city, state, country, units, lang):
        self.city = city
        self.state = state
        self.country = country
        self.units = units
        self.lang = lang


    async def send_async(self):
        api_key = settings.API_KEY
        if self.state is not None:
            q = f"{self.city},{self.state},{self.country}"
        else:
            q = f"{self.city},{self.country}"
        try: 
            url = f"http://api.openweathermap.org/data/2.5/weather?q={q}&units={self.units}&lang={self.lang}&appid={api_key}"

            resp: Response = await self.request_async(
                method="GET",
                url=url,
                timeout=settings.OPENWEATHER_TIMEOUT
                )

            if resp.status_code != 200:
                raise ValidationError(
                    error_msg=resp.text,
                    status_code=resp.status_code
                )

            return resp

        except HTTPException as e:
            return e
