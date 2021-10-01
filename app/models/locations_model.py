from sqlmodel import Field, SQLModel
from typing import Optional

class Location(SQLModel):
    city: str = Field(description="Enter the city name to get weather now")
    state: Optional[str] = Field(min_length=2, max_length=2, description="State must be Alpha-2 code")
    country: Optional[str] = Field(default="BR", min_length=2, max_length=2, description="Country must be Alpha-2 code")
