from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import PermissionDenied
from django_filters.views import FilterView
from django.views.generic import TemplateView
from cms.models.pluginmodel import CMSPlugin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from . import models
from django.views.generic.list import MultipleObjectMixin
from django_filters.views import FilterView
from .filtersets import MediaFilterSet

# NEWS_FILTER_STATES = ("visible", "hidden")
PAGINATE_BY_CHOICES = ('5', '10', '20')

class MediaView(TemplateView):
    template_name = 'medialer/media.html'
    # model = Post
    # paginate_by = 12
    # filterset_class = MediaFilterSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_pictures'] = models.PluginPicture.objects.all()[:8]
        context['non_cat_pictures'] = models.AlbumPicture.objects.filter(album=None)[:8]
        context['albums'] = models.Album.objects.all()
        # context['news_filter_state'] = self.get_filter_state()
        # assert False, context
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)

        # # seting news list layout to cookie
        # response.set_cookie('news_list_layout', 
        #                     self.get_news_list_layout(),
        #                     path=reverse("news:index"),
        #                     max_age=3600*24*7)
        # # seting news filter state to cookie
        # response.set_cookie('news_filter_state', 
        #                     self.get_filter_state(),
        #                     path=reverse("news:index"),
        #                     max_age=3600*24*7)
        return response
    

class AlbumDetailView(MultipleObjectMixin, DetailView):
    template_name = 'medialer/album_detail.html'
    model = models.Album
    paginate_by = 1

    # def get_queryset(self):
        # return models.AlbumPicture.objects.all()

    def get_context_data(self, **kwargs):
        object_list = self.object.get_object_list()
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = "Альбом \"{}\"".format(self.object)
        # context['added_breadcrumbs'] = [{'url':self.object.get_absolute_url, 'title':self.object.title}]
        return context
    

class PluginPictureListView(ListView):
    template_name = 'medialer/pluginpicture.list.html'
    model = models.PluginPicture
    paginate_by = PAGINATE_BY_CHOICES[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['page_title'] = "Фотоматериалы"
        return context

class MediaFilterView(FilterView):
    template_name = 'medialer/gallery.html'
    filterset_class = MediaFilterSet
    paginate_by = PAGINATE_BY_CHOICES[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['PAGINATE_BY_CHOICES'] = PAGINATE_BY_CHOICES
        context['active_paginate_by'] = self.get_paginate_by(self.queryset)

        if hasattr(context['filter'].form, 'cleaned_data'):
            album = context['filter'].form.cleaned_data['album']
            if album: # album was choosed
                context['album'] = album
                context['page_title'] = "Альбом \"{}\"".format(context['album'].title)
                # context['added_breadcrumbs'] = [{'url':album.get_absolute_url, 'title':album.title}]
        # assert False,(context['filter'].form['album'][0].data)
        # assert False,(context['filter'].form['album'][1].data['value'].instance.description)
        # assert False, (dir(context['filter'].form['album']), context['filter'].form['album'].field)
        # assert False, [choice for choice in context['filter'].form['album']]
        return context

    def get_queryset(self):
        return models.AlbumPicture.objects.all()

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('count', '')
        return paginate_by if paginate_by in PAGINATE_BY_CHOICES else self.paginate_by
