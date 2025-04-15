from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include

from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', DocumentListView.as_view(), name='index'),
    path('<int:id>', DocumentDetailView.as_view(), name='detail'),
    path('download/<int:id>/', document_download, name='document_download' ),
] 

