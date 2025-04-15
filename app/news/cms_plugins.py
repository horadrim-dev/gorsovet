from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from news.models import Post

from .models import NewsPlugin

@plugin_pool.register_plugin
class NewsPlugin(CMSPluginBase):
    model =  NewsPlugin
    render_template = 'news/news.plugin.html'
    name = "Новости"   

    def render(self, context, instance, placeholder):

        context.update({
            'id': instance.generate_id(),
            'instance': instance,
        })

        if context['request'].user.is_authenticated:
            context['object_list'] = Post.objects.all()[:instance.num_objects]
        else:
            context['object_list'] = Post.objects.published()[:instance.num_objects]

        return context


#
