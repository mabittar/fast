from datetime import datetime
from typing import List, Optional
from uuid import uuid4
from infrastructure.database import get_session

from sqlmodel import select
from models import Report

class ReportService():
    def __init__(self, session = None):
        self.session = session if session is not None else get_session()

    def get_reports(
        self,
        page: Optional[int] = 0,
        page_size: Optional[int] = 10
        ) -> List[Report]:
        statement = select(Report).offset(page).limit(page_size)
        results = self.session.exec(statement).all()
        return results

    async def get_report(
        self, 
        id: Optional[int] = None,
        city: Optional[str] = None,
        first_result: Optional[bool] = False,
    ):

        if id is not None:
            results = self.session.exec(select(Report))
            results = self.session.get(Report, id)

        if city is not None:
            statement = select(Report).where(Report.city == city)
            results = self.session.exec(statement)
            results = results.first() if first_result else results.all()

        return results


    def add_report(self, data) -> Report:
        now = datetime.now()
        uuid = str(uuid4())
        state = data.state if data.state is not None else None
        report = Report(
            city=data.city,
            country=data.country,
            state=state, 
            description=data.description,
            created_at=now,
            uuid=uuid
            )

        self.session.add(report)
        self.session.commit()
        self.session.refresh(report)
        return report
