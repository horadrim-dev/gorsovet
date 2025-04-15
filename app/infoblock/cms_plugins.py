from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .models import Infoblock, Slide
from .forms import InfoblockForm

# class SlideInlineAdmin(admin.StackedInline):
#     model = Slide
#     extra = 0

@plugin_pool.register_plugin
class InfoBlockPlugin(CMSPluginBase):
    model = Infoblock
    module = "Контейнеры"
    name = "Контент-слайдер"
    render_template = "./infoblock.html"
    cache = True
    # inlines = (SlideInlineAdmin, )
    allow_children = True
    child_classes = ["BackgroundSectionPlugin"]
    form = InfoblockForm
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
    #     ('Фоновое изображение (если ширина и высота равны 0 - будет использоваться оригинальный размер)', {
    #         'fields': [
    #             ('background_image',
    #             'thumb_width',
    #             'thumb_height'),
    #         ]
    #     }),
    # )

    def render(self, context, instance, placeholder):
        context.update({
            'id': instance.generate_id(),
            # 'slides': instance.get_slides(),
            'instance': instance,
        })
        return context


@plugin_pool.register_plugin
class SlidePlugin(CMSPluginBase):
    # НЕ ИСПОЛЬЗУЕТСЯ, ОСТАВЛЕНО ВО ИЗБЕЖАНИЕ ПРОБЛЕМ С МИГРАЦИЕЙ
    model = Slide
    module = "Инфослайдер"
    name = "Слайд"
    render_template = "./slide.html"
    parent_classes = ["InfoblockPlugin"]
    allow_children = True

    def render(self, context, instance, placeholder):
        # assert False, dir(instance)
        context.update({
            'instance': instance,
        })
        return context