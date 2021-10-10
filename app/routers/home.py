from typing import List
from fastapi import APIRouter, Depends
from fastapi import responses
from sqlmodel import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from infrastructure.database import get_session
from models.report_model import Report
from services.report_service import ReportService

templates = Jinja2Templates("templates")
router = APIRouter(
    tags=["home"],
)


@router.get(
    "/", 
    include_in_schema=False)
async def index(request: Request,
          session: Session = Depends(get_session),):

    reports: List[Report] = ReportService(session).get_reports(page=0, page_size=10)
    data = {"request": request, "reports": reports}
    return templates.TemplateResponse("home/index.html", data)


@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    return responses.RedirectResponse(url="/static/img/favicon.ico")
