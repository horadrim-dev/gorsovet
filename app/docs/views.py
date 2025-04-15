from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, FileResponse
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import PermissionDenied
from .models import Document, DocumentCategory
from django_filters.views import FilterView
from .filtersets import DocumentFilterSet
from cms.models.pluginmodel import CMSPlugin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse
import os

# NEWS_LIST_LAYOUTS = ("list", "grid" )
# NEWS_FILTER_STATES = ("visible", "hidden")
PAGINATE_BY_CHOICES = ('10', '25', '50')
class DocumentListView(FilterView):
    template_name = 'docs/document_list.html'
    # model = Post
    paginate_by = PAGINATE_BY_CHOICES[0]
    filterset_class = DocumentFilterSet

    # def get_news_list_layout(self):
    #     layout = self.request.COOKIES.get('news_list_layout', None)
    #     return layout if layout in NEWS_LIST_LAYOUTS else NEWS_LIST_LAYOUTS[0]

    # def get_filter_state(self):
    #     filter_state = self.request.COOKIES.get('news_filter_state', None)
    #     return filter_state if filter_state in NEWS_FILTER_STATES else NEWS_FILTER_STATES[0]

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('count', '')
        return paginate_by if paginate_by in PAGINATE_BY_CHOICES else self.paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['news_list_layout'] = self.get_news_list_layout()
        # context['news_filter_state'] = self.get_filter_state()

        # меняем заголовок страницы
        category = self.request.GET.get("category", None)
        if category and isinstance(category, str) and category.isdigit():
            try:
                c = DocumentCategory.objects.get(id=category)
                context['page_title'] = c.name
            except:
                pass
            
        context['PAGINATE_BY_CHOICES'] = PAGINATE_BY_CHOICES
        context['active_paginate_by'] = self.get_paginate_by(self.queryset)
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)

        # seting news list layout to cookie
        # response.set_cookie('news_list_layout', 
        #                     self.get_news_list_layout(),
        #                     path=reverse("news:index"),
        #                     max_age=3600*24*7)
        # seting news filter state to cookie
        # response.set_cookie('news_filter_state', 
        #                     self.get_filter_state(),
        #                     path=reverse("news:index"),
        #                     max_age=3600*24*7)
        return response


class DocumentDetailView(DetailView):
    template_name = 'docs/document_detail.html'
    slug_field = 'id'
    model = Document

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['added_breadcrumbs'] = [{'url':self.object.get_absolute_url, 'title':self.object.name}]
        context['page_title'] = self.object.name
        return context
    

def document_download(request, id, *args, **kwargs):
    # media_root = settings.MEDIA_ROOT
    try:
        # document = Attachment.objects.get(uuid=uuid)
        document = Document.objects.get(id=id)
    except:
        raise Http404('Файл не найден.')

    if os.path.isfile(document.document_file.path):
        document.hits += 1
        document.save()
        return FileResponse(
            open(document.document_file.path, 'rb'),
            as_attachment=True,
            filename=document.filename
        )
    else:
        raise Http404(
            'Файл "{}" в хранилище не найден.'.format(
                document.document_file.path)
        )