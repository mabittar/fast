
from fastapi import APIRouter, responses
from starlette.requests import Request
from starlette.templating import Jinja2Templates


templates = Jinja2Templates('templates')
router = APIRouter(tags=["home"],)


@router.get('/')
def index(request: Request):
    return templates.TemplateResponse('home/index.html', {'request': request})


@router.get('/favicon.ico')
def favicon():
    return responses.RedirectResponse(url='/static/img/favicon.ico')
