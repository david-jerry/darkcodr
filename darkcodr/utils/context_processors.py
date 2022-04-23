import json
import datetime

from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.db.models.functions import GeometryDistance
from django.contrib.gis.geos import Point
from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject

from darkcodr.utils.logger import LOGGER

User = get_user_model()

dt = datetime.datetime.now()

def context_settings(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        if settings.PRODUCTION:
            ip = request.META.get('REMOTE_ADDR')
        else:
            ip = '8.8.8.8'

    #  Get current location on google map
    g = GeoIP2()
    location = g.city(ip)
    location_country = location["country_name"]
    location_country_code = location["country_code"]
    location_latitude = location["latitude"]
    location_longitude = location["longitude"]
    location_city = location["city"]

    current_loc = Point(location_longitude, location_latitude, srid=4326)

    if dt.hour >= 4 and dt.hour < 12:
        greeting = "Good Morning"
        sleep = False
    elif dt.hour >= 12 and dt.hour < 17:
        greeting = "Good Afternoon"
        sleep = False
    elif dt.hour >= 17 and dt.hour < 22:
        greeting = "Good Evening"
        sleep = False
    elif dt.hour >= 22 and dt.hour < 4:
        greeting = "Good Night"
        sleep = True
    else:
        greeting = "Welcome"
        sleep = False


    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "DEBUG": settings.DEBUG,
        "settings": settings,

        'user_ip': ip,
        "current_loc": current_loc,
        'location_country': location_country,
        'location_country_code': location_country_code,
        'location_latitude': location_latitude,
        'location_longitude': location_longitude,
        'location_city': location_city,

        # Time greeting
        'greeting': greeting,
        'sleep_time': sleep,

        'site': SimpleLazyObject(lambda: get_current_site(request)) if not settings.DEBUG else "localhost:8000",
    }
