#!/usr/bin/python3
"""sharing app_views Blueprint"""

from flask import Blueprint
from api.v1.views.index import configure_views
# app_views = Blueprint('app_views', __name__)
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
configure_views(app_views)
