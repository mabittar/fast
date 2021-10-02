from .health import router as health
from .home import router as home
from .weather import router as weather
from .report import router as report

routers_list = [health, home, weather, report]
