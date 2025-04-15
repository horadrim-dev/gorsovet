from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include, register_converter
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('by-date/', GetSessionEventListView.as_view(), name='events_by_date' ),
] 

