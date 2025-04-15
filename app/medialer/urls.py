from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path, include

from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    # path('', MediaView.as_view(), name='index'),
    path('', MediaFilterView.as_view(), name='index'),
    path('photo-materials', PluginPictureListView.as_view(), name='photo_materials'),
    #path('albums/<int:pk>', AlbumDetailView.as_view(), name='album'),
] 

