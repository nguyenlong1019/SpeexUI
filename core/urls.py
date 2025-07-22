from django.urls import path, include 
from core.views.index import *
from core.views.api import *


urlpatterns = [
    path('', index_view, name='index_view'),
    path('api/', include([
        path('ss', access_log_api, name='access-log-api'),
    ])),
]
