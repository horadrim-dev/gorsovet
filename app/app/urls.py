"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path, re_path, include
from cms.sitemaps import CMSSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.i18n import JavaScriptCatalog
from django.conf import settings
from django.conf.urls.static import static

js_info_dict = {
    'packages': ('recurrence', ),
}


urlpatterns = [
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), js_info_dict),
    # re_path(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path('search/', include('haystack.urls')),
    path('core/', include('core.system_urls')),
    path("prometheus/", include("django_prometheus.urls")),
    path('admin/', admin.site.urls),
    # path('', include('structure.system_urls')),
    path('', include('cms.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


