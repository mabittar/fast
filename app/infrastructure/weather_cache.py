import datetime
from typing import Optional
from typing import Tuple
from utils.logger import Logger
from collections import OrderedDict

from env_config import settings

__cache = OrderedDict()
lifetime_in_hours = settings.LIFETIME_CACHE_HOURS
logger = Logger()

def get_weather(city: str, state: Optional[str], country: Optional[str], units: str) -> Optional[dict]:
    logger.debug("Check if result is already cached")
    key = __create_key(city, state, country, units)
    data: dict = __cache.get(key)
    if not data:
        return None

    last = data["time"]
    dt = datetime.datetime.now() - last
    if dt / datetime.timedelta(minutes=60) < lifetime_in_hours:
        logger.debug("Returning cached result")
        return data["value"]

    del __cache[key]
    return None


def set_weather(city: str, state: str, country: str, units: str, value: dict):
    key = __create_key(city, state, country, units)
    data: dict = dict(time=datetime.datetime.now(), value=value)
    logger.debug("Creating new cache entry")
    __cache[key] = data
    __clean_out_of_date()


def __create_key(city: str, state: str, country: str, units: str) -> Tuple[str, str, str, str]:
    if not city or not country or not units:
        
        raise Exception("City, country and units are required")

    if not state:
        state = ""

    return city.strip().lower(), state.strip().lower(), country.strip().lower(), units.strip().lower()


def __clean_out_of_date():
    cached_results = list(__cache.keys())
    for key, data in list(__cache.items()):
        dt = datetime.datetime.now() - data.get("time")
        if dt / datetime.timedelta(minutes=60) > lifetime_in_hours:
            del __cache[key]
    if len(cached_results) > 10:
        logger.debug(("Cache is oversized, remove first entry"))
        __cache.popitem(last=False)

