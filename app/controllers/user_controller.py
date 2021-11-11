

from typing import Optional

from sqlmodel.sql.expression import select
from infrastructure.database import get_session
from models.users import User, UserCreate


class UserController:
    def __init__(self, session=None):
        self.session = session if session is not None else get_session()

    def get_by_email(self, *, email: str) -> Optional[User]:
        return self.session.exec(select(User, email)).first()

    def create(self, *, obj_in: UserCreate):
        model = 
