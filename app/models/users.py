from typing import TYPE_CHECKING, List
from pydantic.types import EmailStr
from sqlalchemy import Boolean, Column, Integer, String
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .report_model import Report


class UserPost(SQLModel):
    full_name: str = Field(default='Usuário Teste', description='Create an user name', min_length=2, max_length=226)
    email: EmailStr = Field(default='teste@teste.com', description='user mail')
    reports: List["Report"] = Relationship(back_populates="Report")


class UserPatch(SQLModel):
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)


class User(UserPost, UserPatch, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)


class UserWithReports(User):
    # Response for GET User with reports
    reports: List[Report] = []
