from typing import List, Optional, Union
from fastapi import APIRouter, HTTPException, Query, Depends
from models.report_model import Report, ReportPost, ReportRead
from services import report_service
from sqlmodel import Session
from infrastructure.database import engine, get_session
from services.report_service import ReportService


router = APIRouter(
    tags=["report"]
)


@router.get(
    '/api/reports', 
    name="all reports",
    response_model=List[Report])
async def reports_get(
    *,
    session: Session = Depends(get_session),
    page: Optional[int] = Query(default=0, ge=0),
    page_size: Optional[int] = Query(default=10, lte=100),
    ) -> List[Report]:
    report_service = ReportService(session)
    return report_service.get_reports(page, page_size)


@router.get(
    '/api/reports/{report_id}',
    name="get report by ID",
    response_model=Report
)
async def report_search(
    *,
    session: Session = Depends(get_session),
    report_id: int = Query(default=1, ge=1, description='Report ID'),
):
    report_service = ReportService(session)
    report = await report_service.get_report(
        id=report_id
    )
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get(
    '/api/reports/',
    name="get reports by city",
    response_model=Report
)
async def report_search(
    *,
    session: Session = Depends(get_session),
    city: str = Query(default=None, description='Get reports from city'),
    first_result: bool = Query(default=True, description='First result or all results')
):

    if not city:
        raise HTTPException(status_code=404, detail="City cant be None")
    report_service = ReportService(session)
    report = await report_service.get_report(
        city=city,
        first_result=first_result
    )
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post(
    '/api/reports', 
    name="create new report",
    status_code=201,
    response_model=Report
    )
async def reports_post(*, session: Session = Depends(get_session),report: ReportPost) -> Report:
    
    report_service = ReportService(session)
    return report_service.add_report(report)
