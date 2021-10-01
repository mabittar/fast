from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class ReportPost(SQLModel):
    description: str = Field(
        description="Natural Event to be Reported", min_length=1, max_length=226)
    city: str = Field(description="Enter the city name to get weather now")
    state: Optional[str] = Field(
        min_length=2, max_length=2, description="State must be Alpha-2 code")
    country: Optional[str] = Field(
        default="BR", min_length=2, max_length=2, description="Country must be Alpha-2 code")


class Report(ReportPost, table=True):
    id: int = Field(default=None, primary_key=True)
    uuid: str = Field(description="unique id for report")
    created_at: datetime = None


class ReportRead(Report):
    pass
