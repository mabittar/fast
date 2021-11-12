from .health import router as health
from .home import router as home
from .report import router as report
from .weather import router as weather

routers_list = [health, home, weather, report]
