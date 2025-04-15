from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib import admin

from .models import Slider, Slide


class SlideInlineAdmin(admin.StackedInline):
    model = Slide
    extra = 0

@plugin_pool.register_plugin
class SliderPlugin(CMSPluginBase):
    model = Slider
    name = "Слайдер"
    render_template = "./slider/slider.html"
    cache = True
    allow_children = True
    child_classes = ["SliderItemPlugin"]
    # inlines = (SlideInlineAdmin, )
    # fieldsets = (
    #     (None, {
    #         'fields': [
    #             'folder',
    #             ('pageThumbWidth',
    #             'pageThumbHeight',
    #             'pageThumbMarginVertical',
    #             'pageThumbMarginHorizontal',),
    #         ]
    #     }),
    #     (_('Toolbar Settings'), {
    #         'fields': [
    #             'zoomActualSize',
    #             'fullscreen',
    #             'zoom',
    #         ]
    #     }),
    # )

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'id': instance.generate_id(),
        })
        return context


@plugin_pool.register_plugin
class SliderItemPlugin(CMSPluginBase):
    model = Slide
    module = "Слайдер"
    name = "Слайд"
    render_template = "./slider/slide.html"
    parent_classes = ["SliderPlugin"]
    allow_children = False
    # form = CatalogItemPluginForm


    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
        })
        return context