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
            qs = Post.objects.all()
        else:
            qs = Post.objects.published()

        if instance.category:
            qs = qs.filter(category=instance.category)

        context['object_list'] = qs[:instance.num_objects]
        return context


#
