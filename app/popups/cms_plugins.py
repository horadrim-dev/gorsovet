from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib import admin

from .models import Popup

@plugin_pool.register_plugin
class PopupPlugin(CMSPluginBase):
    model = Popup
    name = "Всплывающее сообщение"
    render_template = "popups/popup.html"
    cache = True
    allow_children = False

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'DO_NOT_SHOW': context['request'].COOKIES.get('hide_popup_' + str(instance.id), None)
        })
        return context