from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .models import BackgroundSection
from .forms import SectionForm

@plugin_pool.register_plugin
class BackgroundSectionPlugin(CMSPluginBase):
    model = BackgroundSection
    render_template = 'background_section.html'
    name = "Секция"
    module = "Контейнеры"
    allow_children = True
    form = SectionForm

    fieldsets = (
        (None, {
            'fields': [
                ('title', 'title_align'),
                ('padding_top', 'padding_bottom'),
                'container_type',
                'background_color',
                'css_classes',
            ]
        }),
        ('Фоновое изображение (если ширина и высота равны 0 - будет использоваться оригинальный размер)', {
            'fields': [
                ('background_image',
                'thumb_width',
                'thumb_height'),
                'use_parallax',
                'use_blur',
            ]
        }),
        ('Настройки оверлея', {
            'fields': [
                ('use_overlay',
                'overlay_color',
                'overlay_opacity'),
            ]
        }),
    )

    def render(self, context, instance, placeholder):
        context.update({
            'id': instance.generate_id(),
            'instance': instance,
            'background_image':instance.background_image,
            'background_color':instance.background_color,
        })
        return context

