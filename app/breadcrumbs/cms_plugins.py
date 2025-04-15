from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Breadcrumbs

@plugin_pool.register_plugin
class BreadcrumbsPlugin(CMSPluginBase):
    model = Breadcrumbs
    render_template = 'breadcrumbs/base.html'
    name = "Хлебные крошки"
    allow_children = False
    cache = False

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            # 'image': instance.image,
            # 'width_height_thumb': instance.width_height_thumb,
            'white_mode': instance.white_mode
        })
        if instance.title:
            context['page_title'] = instance.title
        return context

