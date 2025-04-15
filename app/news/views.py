from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import PermissionDenied
from .models import Post
from django_filters.views import FilterView
from .filtersets import PostFilterSet
from cms.models.pluginmodel import CMSPlugin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt


class PublishedObjectsMixin:

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.all() # [:instance.num_objects]
        else:
            return Post.objects.published() # [:instance.num_objects]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ADMIN_MODE"] = self.request.user.is_authenticated
        context["EDIT_MODE"] = True if self.request.toolbar.edit_mode_active else False
        return context
    

NEWS_LIST_LAYOUTS = ("list", "grid" )
NEWS_FILTER_STATES = ("visible", "hidden")

PAGINATE_BY_CHOICES = ('5', '10', '20')
class PostListView(PublishedObjectsMixin, FilterView):
    template_name = 'news/post.list.html'
    # model = Post
    paginate_by = PAGINATE_BY_CHOICES[0]
    filterset_class = PostFilterSet

    def get_news_list_layout(self):
        layout = self.request.COOKIES.get('news_list_layout', None)
        return layout if layout in NEWS_LIST_LAYOUTS else NEWS_LIST_LAYOUTS[0]

    def get_filter_state(self):
        filter_state = self.request.COOKIES.get('news_filter_state', None)
        return filter_state if filter_state in NEWS_FILTER_STATES else NEWS_FILTER_STATES[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list_layout'] = self.get_news_list_layout()
        context['news_filter_state'] = self.get_filter_state()

        context['PAGINATE_BY_CHOICES'] = PAGINATE_BY_CHOICES
        context['active_paginate_by'] = self.get_paginate_by(self.queryset)
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)

        # seting news list layout to cookie
        response.set_cookie('news_list_layout', 
                            self.get_news_list_layout(),
                            path=reverse("news:index"),
                            httponly=False,
                            samesite=None,
                            max_age=3600*24*7)
        # seting news filter state to cookie
        response.set_cookie('news_filter_state', 
                            self.get_filter_state(),
                            path=reverse("news:index"),
                            httponly=False,
                            samesite=None,
                            max_age=3600*24*7)
        return response

    def get_paginate_by(self, queryset):
        paginate_by = self.request.GET.get('count', '')
        return paginate_by if paginate_by in PAGINATE_BY_CHOICES else self.paginate_by


class PostDetailView(PublishedObjectsMixin, DetailView):
    template_name = 'news/post.detail.html'
    slug_field = 'alias'
    model = Post

    @method_decorator(csrf_exempt)
    def get(self, request, *args, **kwargs) :
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['added_breadcrumbs'] = [{'url':self.object.get_absolute_url, 'title':self.object.title}]
        context['other_objects'] = self.get_queryset().exclude(id=context['object'].id)[:9]
        context['page_title'] = self.object.title
        return context
    


ACTION_LIST = ("toggle-publish-state", )
RESULTS = {
    0 : "error",
    1 : "success",
}

class AdminView(View):


    def dispatch(self, request, *args, **kwargs):

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return self.ajax_post(request, *args, **kwargs)

        return super().dispatch(request, *args, **kwargs)
    

    def ajax_post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            print('NOT LOGGED IN')
            raise PermissionDenied

        action = request.POST.get("action")
        post = request.POST.get("post")

        if action not in ACTION_LIST:
            raise Http404

        try:
            post = Post.objects.get(pk=post)
        except Post.DoesNotExist:
            raise Http404
        
        if post and (action == 'toggle-publish-state'):
            try:
                return self.toggle_publish_state_post(request, post)
            except PermissionDenied:
                return JsonResponse({"result": RESULTS[0], "message": "Нет прав доступа для этой операции"})

        raise Http404
    

    @method_decorator(permission_required("news.change_post", raise_exception=True))
    def toggle_publish_state_post(self, request, post:Post):
        '''Switching publish state of Post'''
        if post.published:
            post.published = False
            post.save()
            return JsonResponse({"result": RESULTS[1], "message": "Снято с публикации"})
        else:
            # if post has child plugins
            if CMSPlugin.objects.filter(placeholder_id=post.content_id).count() > 0:
                post.published = True
                post.save()
                return JsonResponse({"result": RESULTS[1], "message": "Опубликовано"})
            else: # no child plugins
                message = "Новость пуста и поэтому не может быть опубликована. \n Добавьте плагинов на страницу."
                return JsonResponse({"result": RESULTS[0], "message": message})
