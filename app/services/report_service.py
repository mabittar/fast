from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from infrastructure.database import get_session
from models import Report
from sqlmodel import select
from utils.logger import Logger


class ReportService:
    def __init__(self, session=None, logger: Optional[Logger] = None,):
        self.session = session if session is not None else get_session()
        self.logger = logger if logger is not None else Logger(class_name=__name__)

    def get_reports(self, page: Optional[int] = 0, page_size: Optional[int] = 10) -> List[Report]:
        self.logger.debug("Getting paginated reports")
        statement = select(Report).offset(page).limit(page_size)
        results = self.session.exec(statement).all()
        self.logger.debug(f"Found {len(results)} result(s)")
        return results

    async def get_report(
        self,
        id: Optional[int] = None,
        city: Optional[str] = None,
        first_result: Optional[bool] = False,
    ):

        if id is not None:
            self.logger.debug(f"Get report with id = {id}")
            results = self.session.exec(select(Report))
            results = self.session.get(Report, id)

        if city is not None:
            self.logger.debug(f"Get report with city = {city}")
            statement = select(Report).where(Report.city == city)
            results = self.session.exec(statement)
            results = results.first() if first_result else results.all()

        self.logger.info(f"Returning {len(results)} result(s) found.")
        return results

    def add_report(self, data) -> Report:
        self.logger.debug(f"Receiving REQUEST to create new report!")
        now = datetime.now()
        uuid = str(uuid4())
        state = data.state if data.state is not None else None
        report = Report(
            city=data.city, country=data.country, state=state, description=data.description, created_at=now, uuid=uuid
        )

        self.session.add(report)
        self.session.commit()
        self.session.refresh(report)
        self.logger.info(f"New report created with id {report.id}")
        return report
