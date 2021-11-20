from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field


class ReportResponseDTO(BaseModel):
    city: str
    state: Optional[str]
    country: Optional[str]
    temp: Optional[float]
    feels_like: Optional[float]
    temp_min: Optional[float]
    temp_max: Optional[float] 
    pressure: Optional[float] 
    humidity: Optional[float]
