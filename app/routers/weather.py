from fastapi.exceptions import HTTPException
from models.validation_error import ValidationError
from typing import Optional
from fastapi import APIRouter, Response
from models.locations_model import Location
from fastapi import Depends
from services.location_service import LocationService

router = APIRouter(
    tags=["weather"]
)


@router.get('/api/weather/{city}')
async def weather(
    loc: Location = Depends(),
    units: Optional[str] = "metric"
    ) -> dict:
    try:
        return await LocationService.get_report_async(
            city=loc.city,
            state=loc.state,
            country=loc.country,
            units=units
        )
    except ValidationError as ve:
        return Response(content=ve.error_msg, status_code=ve.status_code)

    except HTTPException as http_error:
        return Response(content=http_error.error_msg, status_code=http_error.status_code)
