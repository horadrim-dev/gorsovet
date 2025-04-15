from typing import Any
from django.conf import settings
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.cms_plugins import CMSPlugin
from cms.plugin_pool import plugin_pool

from . import forms
from . import models

@plugin_pool.register_plugin
class AlbumPicturesPlugin(CMSPluginBase):
    module = "Медиа"
    name = "Последние фотографии (из галереи)"
    allow_children = False
    render_template = "medialer/plugins/latestpictures.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['object_list'] = models.AlbumPicture.objects.all()[:8]
        return context

@plugin_pool.register_plugin
class PluginPicturesPlugin(CMSPluginBase):
    module = "Медиа"
    name = "Последние фотографии (из постов)"
    allow_children = False
    render_template = "medialer/plugins/latestpluginpictures.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['object_list'] = models.PluginPicture.objects.all()[:8]
        return context
 

@plugin_pool.register_plugin
class AlbumsPlugin(CMSPluginBase):
    # model = models.Album
    # form = forms.PluginPictureForm
    module = "Медиа"
    name = "Список альбомов"
    allow_children = False
    render_template = "medialer/plugins/albums.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['album_list'] = models.Album.objects.all()
        return context
    




# enable nesting of plugins inside the picture plugin
PICTURE_NESTING = getattr(settings, 'medialer_NESTING', False)

@plugin_pool.register_plugin
class PicturePlugin(CMSPluginBase):
    model = models.PluginPicture
    form = forms.PluginPictureForm
    module = "Медиа"
    name = _('Image')
    allow_children = PICTURE_NESTING
    text_enabled = True

    fieldsets = [
        (None, {
            'fields': (
                'picture',
                'external_picture',
                'alignment',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                # 'template',
                # 'use_responsive_image',
                ('width', 'height'),
                # 'caption_text',
                # 'attributes',
            )
        }),
        (_('Link settings'), {
            'classes': ('collapse',),
            'fields': (
                ('link_url', 'link_page'),
                'link_target',
                # 'link_attributes',
            )
        }),
        (_('Настройка обрезки'), {
            'classes': ('collapse',),
            'fields': (
                ('use_automatic_scaling', 'use_no_cropping', 'use_crop', 'use_upscale'),
                # (),
                # 'thumbnail_options',
            )
        })
    ]

    def get_render_template(self, context, instance, placeholder):
        return 'medialer/{}/picture.html'.format(instance.template)

    def render(self, context, instance, placeholder):
        if instance.alignment:
            classes = 'align-{} '.format(instance.alignment)
            classes += instance.attributes.get('class', '')
            # Set the class attribute to include the alignment html class
            # This is done to leverage the attributes_str property
            instance.attributes['class'] = classes
        # assign link to a context variable to be performant
        context['picture_link'] = instance.get_link()
        context['picture_size'] = instance.get_size(
            width=context.get('width') or 0,
            height=context.get('height') or 0,
        )
        context['img_srcset_data'] = instance.img_srcset_data

        return super().render(context, instance, placeholder)


# =========================== VIDEO ====================================#

@plugin_pool.register_plugin
class VideoPlayerPlugin(CMSPluginBase):
    model = models.VideoPlayer
    name = _('Видео')
    text_enabled = True
    allow_children = False
    module = "Медиа"
    # child_classes = ['VideoSourcePlugin', 'VideoTrackPlugin']
    form = forms.VideoPlayerPluginForm

    fieldsets = [
        (None, {
            'fields': (
                # 'template',
                # 'label',
                'source_file',
                'attributes',
            )
        }),
        (_('Встраиваемое видео'), {
            'classes': ('collapse',),
            'fields': (
                'embed_link',
                'parameters',
            )
        }),
        (_('Обложка'), {
            'classes': ('collapse',),
            'fields': (
                'poster',
            )
        }),
        (_('Настройка размеров'), {
            'classes': ('collapse',),
            'fields': (
                'width', 
                'height',
            )
        }),
        # (_('Advanced settings'), {
        #     'classes': ('collapse',),
        #     'fields': (
        #     )
        # })
    ]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['video_template'] = instance.template
        return context

    def get_render_template(self, context, instance, placeholder):
        return 'medialer/{}/video_player.html'.format(instance.template)



@plugin_pool.register_plugin
class VideoSourcePlugin(CMSPluginBase):
    model = models.VideoSource
    name = _('Source')
    # module = _('Video player')
    module = "Медиа"
    require_parent = True
    parent_classes = ['VideoPlayerPlugin']

    fieldsets = [
        (None, {
            'fields': (
                'source_file',
                'text_title',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'text_description',
                'attributes',
            )
        })
    ]

    def get_render_template(self, context, instance, placeholder):
        return 'medialer/{}/source.html'.format(context.get('video_template', 'default'))


@plugin_pool.register_plugin
class VideoTrackPlugin(CMSPluginBase):
    model = models.VideoTrack
    name = _('Track')
    # module = _('Video player')
    module = "Медиа"
    require_parent = True
    parent_classes = ['VideoPlayerPlugin']

    fieldsets = [
        (None, {
            'fields': (
                'kind',
                'src',
                'srclang',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'label',
                'attributes',
            )
        })
    ]

    def get_render_template(self, context, instance, placeholder):
        return 'medialer/{}/track.html'.format(context.get('video_template', 'default'))
