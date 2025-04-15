"""
Enables the user to add an "Image" plugin that displays an image
using the HTML <img> tag.
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin
from cms.models.fields import PageField

from djangocms_attributes_field.fields import AttributesField
from easy_thumbnails.files import get_thumbnailer
from filer.fields.image import FilerImageField
from filer.models import ThumbnailOption

from django.urls import reverse

class Album(models.Model):
    title = models.CharField("Название", max_length=256)
    description = models.CharField("Описание", max_length=1024, blank=True, null=True)
    cover_image = FilerImageField(
        verbose_name="Обложка",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Если оставить пустым, будет использовано изображение из альбома"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "альбом"
        verbose_name_plural = "альбомы"

    def get_absolute_url(self):
        return reverse("medialer:index") + "?album={}".format(self.pk)


    def get_cover_image(self):
        if self.cover_image:
            return self.cover_image

        pic = AlbumPicture.objects.filter(album=self).first()
        if pic and pic.picture:
            return pic.picture

        return None

    def thumb_src(self):
        image = self.get_cover_image()
        if not image:
            return None

        thumbnail_options = {
            'size': (360, 240),
            'crop': True,
            'upscale': True,
            'subject_location': image.subject_location,
        }
        thumbnailer = get_thumbnailer(image)
        return thumbnailer.get_thumbnail(thumbnail_options).url
    
    def get_object_list(self):
        return self.albumpicture_set.all()

# class Photo(models.Model):
#     title = models.CharField(
#         default="", max_length=1000, verbose_name="Заголовок")

#     alias = models.SlugField(default="", blank=True, unique=True,
#                              max_length=1000, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.")
#     album = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
#                                     verbose_name="Дата публикации")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")

#     # text = HTMLField("Содержимое", configuration='CKEDITOR_SETTINGS_POST', default="", blank=True, null=True)
#     content = PlaceholderField('content')

#     # placeholder = PlaceholderField('post', related_name="news_post")

#     cover_image = FilerImageField(verbose_name="Обложка поста", 
#                                   on_delete=models.CASCADE, 
#                                   blank=True, null=True,
#                                   help_text="Если не задано - будет использовано первое изображение из содержимого поста")

#     tags = TaggableManager()

#     IMAGE_POSITION_CHOICES = [
#         ('left', 'Слева'),
#         ('stretch', 'Растянуть'),
#         ('right', 'Справа'),
#         ('hide', 'Скрыть'),
#     ]
#     # image_position = models.CharField(max_length=64, choices=IMAGE_POSITION_CHOICES, default=IMAGE_POSITION_CHOICES[0][0],
#     #     verbose_name="Расположение изображения")

#     # placeholder_top = PlaceholderField('top', related_name="post_top")
#     # placeholder_bottom = PlaceholderField('bottom', related_name="post_bottom")

#     objects = ContentManager()

#     @property
#     def gen_id(self):
#         return str(uuid.uuid4().fields[-1])[:7]

#     def get_absolute_url(self):
#         return reverse("news:detail", kwargs={"slug": self.alias})

#     def __str__(self):
#         return self.title

#     def save(self, lock_recursion=False, *args, **kwargs):
#         # только при создании объекта, id еще не существует
#         if not self.id or not self.alias:
#             # заполняем алиас
#             self.alias = slugify_rus(self.title)

#         super().save(*args, **kwargs)

#     def pubdate_has_arrived(self):
#         return False if self.published_at > datetime.date.today() else True

#     def has_content_plugins(self):
#         return CMSPlugin.objects.filter(placeholder_id=self.content_id).count()
    
#     @property
#     def image(self):
#         if self.cover_image:
#             return self.cover_image
#         else:
#             plugin = CMSPlugin.objects.filter(placeholder_id=self.content_id, 
#                                               plugin_type__in=PLUGINS_WITH_IMAGES) \
#                                         .order_by('position') \
#                                         .first()
                                        
#             if not plugin:
#                 return None
#             if plugin.plugin_type == "PicturePlugin":
#                 return plugin.medialer_picture.picture
#             elif plugin.plugin_type == "SliderItemPlugin":
#                 return plugin.slider_slide.image

#     @property
#     def description(self):
#         text = CMSPlugin.objects.filter(placeholder_id=self.content_id, plugin_type="TextPlugin").first()
#         return text.djangocms_text_ckeditor_text.body if text else False 


#     class Meta:
#         verbose_name = "Пост"
#         verbose_name_plural = "Посты"
#         ordering = ['-published_at']


# =========================== PICTURE ====================================#


# add setting for picture alignment, renders a class or inline styles
# depending on your template setup
def get_alignment():
    alignment = getattr(
        settings,
        'DJANGOCMS_PICTURE_ALIGN',
        (
            ('left', _('Слева')),
            ('right', _('Справа')),
            ('center', _('По центру')),
        )
    )
    return alignment


# Add additional choices through the ``settings.py``.
def get_templates():
    choices = [
        ('default', _('Default')),
    ]
    choices += getattr(
        settings,
        'DJANGOCMS_PICTURE_TEMPLATES',
        [],
    )
    return choices


# use golden ration as default (https://en.wikipedia.org/wiki/Golden_ratio)
PICTURE_RATIO = getattr(settings, 'DJANGOCMS_PICTURE_RATIO', 1.6180)

# required for backwards compability
PICTURE_ALIGNMENT = get_alignment()

LINK_TARGET = (
    ('_blank', _('Open in new window')),
    ('_self', _('Open in same window')),
    ('_parent', _('Delegate to parent')),
    ('_top', _('Delegate to top')),
)

RESPONSIVE_IMAGE_CHOICES = (
    ('inherit', _('Let settings.DJANGOCMS_PICTURE_RESPONSIVE_IMAGES decide')),
    ('yes', _('Yes')),
    ('no', _('No')),
)


class AbstractPicture(models.Model):
    """
    Renders an image with the option of adding a link
    """
    template = models.CharField(
        verbose_name=_('Template'),
        choices=get_templates(),
        default=get_templates()[0][0],
        max_length=255,
    )
    picture = FilerImageField(
        verbose_name=_('Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    external_picture = models.URLField(
        verbose_name="Ссылка на внешнее изображение",
        blank=True,
        null=True,
        max_length=255,
        help_text=_(
            'Если указано, переопределяет встроенное изображение. '
            'Некоторые параметры, такие как обрезка, неприменимы к внешним изображениям.'
        )
    )
    width = models.PositiveIntegerField(
        verbose_name="Ширина",
        blank=True,
        null=True,
        help_text=_(
            'Ширина изображения в пикселях'
        ),
    )
    height = models.PositiveIntegerField(
        verbose_name="Высота",
        blank=True,
        null=True,
        help_text=_(
            'Высота изображения в пикселях'
        ),
    )
    alignment = models.CharField(
        verbose_name="Выравнивание",
        choices=get_alignment(),
        blank=True,
        max_length=255,
        # help_text=_('Aligns the image according to the selected option.'),
    )
    caption_text = models.TextField(
        verbose_name=_('Caption text'),
        blank=True,
        null=True,
        help_text=_('Provide a description, attribution, copyright or other information.')
    )
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
        excluded_keys=['src', 'width', 'height'],
    )
    # link models
    link_url = models.URLField(
        verbose_name=_('Внешняя ссылка'),
        blank=True,
        null=True,
        max_length=2040,
        help_text=_('Обернуть изображение в ссылку на внешний ресурс'),
    )
    link_page = PageField(
        verbose_name=_('Внутрення ссылка'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_('Обернуть изображение в ссылку на страницу сайта'),
    )
    link_target = models.CharField(
        verbose_name=_('Цель ссылки'),
        choices=LINK_TARGET,
        blank=True,
        max_length=255,
    )
    link_attributes = AttributesField(
        verbose_name=_('Link attributes'),
        blank=True,
        excluded_keys=['href', 'target'],
    )
    # cropping models
    # active per default
    use_automatic_scaling = models.BooleanField(
        verbose_name=_('Автоматическое масштабирование'),
        blank=True,
        default=True,
        # help_text=_('Uses the placeholder dimensions to automatically calculate the size.'),
    )
    # ignores all other cropping options
    # throws validation error if other cropping options are selected
    use_no_cropping = models.BooleanField(
        verbose_name=_('Использовать оригинальное изображение'),
        blank=True,
        default=False,
        # help_text=_('Вывести изображение в исходном разрешении'),
    )
    # upscale and crop work together
    # throws validation error if other cropping options are selected
    use_crop = models.BooleanField(
        verbose_name=_('Обрезать изображение'),
        blank=True,
        default=False,
        # help_text=_('Crops the image according to the thumbnail settings provided in the template.'),
    )
    use_upscale = models.BooleanField(
        verbose_name=_('Увеличить изображение'),
        blank=True,
        default=False,
        # help_text=_('Upscales the image to the size of the thumbnail settings in the template.')
    )
    use_responsive_image = models.CharField(
        verbose_name=_('Use responsive image'),
        max_length=7,
        choices=RESPONSIVE_IMAGE_CHOICES,
        default=RESPONSIVE_IMAGE_CHOICES[0][0],
        help_text=_(
            'Uses responsive image technique to choose better image to display based upon screen viewport. '
            'This configuration only applies to uploaded images (external pictures will not be affected). '
        )
    )
    # overrides all other options
    # throws validation error if other cropping options are selected
    thumbnail_options = models.ForeignKey(
        ThumbnailOption,
        verbose_name=_('Thumbnail options'),
        blank=True,
        null=True,
        help_text=_('Overrides width, height, and crop; scales up to the provided preset dimensions.'),
        on_delete=models.CASCADE,
    )


    class Meta:
        abstract = True

    def __str__(self):
        if self.picture and self.picture.label:
            return self.picture.label
        return str(self.pk)

    def get_short_description(self):
        if self.external_picture:
            return self.external_picture
        if self.picture and self.picture.label:
            return self.picture.label
        return gettext('<file is missing>')


    def get_size(self, width=None, height=None):
        crop = self.use_crop
        upscale = self.use_upscale
        # use field thumbnail settings
        if self.thumbnail_options:
            width = self.thumbnail_options.width
            height = self.thumbnail_options.height
            crop = self.thumbnail_options.crop
            upscale = self.thumbnail_options.upscale
        elif not self.use_automatic_scaling:
            width = self.width
            height = self.height

        # calculate height when not given according to the
        # golden ratio or fallback to the picture size
        if not height and width:
            height = int(width / PICTURE_RATIO)
        elif not width and height:
            width = int(height * PICTURE_RATIO)
        elif not width and not height and self.picture:
            width = self.picture.width
            height = self.picture.height

        options = {
            'size': (width, height),
            'crop': crop,
            'upscale': upscale,
        }
        return options

    def get_link(self):
        if self.link_url:
            return self.link_url
        elif self.link_page_id:
            return self.link_page.get_absolute_url(language=self.language)
        elif self.external_picture:
            return self.external_picture
        return False

    def clean(self):
        # there can be only one link type
        if self.link_url and self.link_page_id:
            raise ValidationError(
                gettext(
                    'Вы указали и внешнее изображение и внутреннее.'
                    'Оставьте что-то одно'
                )
            )

        # you shall only set one image kind
        if not self.picture and not self.external_picture:
            raise ValidationError(
                gettext(
                    'Необходимо загрузить изображение,'
                    'или ссылку на внешнее изображение'
                )
            )

        # certain cropping options do not work together, the following
        # list defines the disallowed options used in the ``clean`` method
        invalid_option_pairs = [
            ('use_automatic_scaling', 'use_no_cropping'),
            ('use_automatic_scaling', 'thumbnail_options'),
            ('use_no_cropping', 'use_crop'),
            ('use_no_cropping', 'use_upscale'),
            ('use_no_cropping', 'thumbnail_options'),
            ('thumbnail_options', 'use_crop'),
            ('thumbnail_options', 'use_upscale'),
        ]
        # invalid_option_pairs
        invalid_option_pair = None

        for pair in invalid_option_pairs:
            if getattr(self, pair[0]) and getattr(self, pair[1]):
                invalid_option_pair = pair
                break

        if invalid_option_pair:
            message = gettext(
                'Неправильные настройки обрезки'
                'Вы не можете использовать "{field_a}" одновременно с "{field_b}".'
            )
            message = message.format(
                field_a=self._meta.get_field(invalid_option_pair[0]).verbose_name,
                field_b=self._meta.get_field(invalid_option_pair[1]).verbose_name,
            )
            raise ValidationError(message)

    @property
    def is_responsive_image(self):
        if self.external_picture:
            return False
        if self.use_responsive_image == 'inherit':
            return getattr(settings, 'DJANGOCMS_PICTURE_RESPONSIVE_IMAGES', False)
        return self.use_responsive_image == 'yes'

    @property
    def img_srcset_data(self):
        if not (self.picture and self.is_responsive_image):
            return None

        srcset = []
        thumbnailer = get_thumbnailer(self.picture)
        picture_options = self.get_size(self.width, self.height)
        picture_width = picture_options['size'][0]
        thumbnail_options = {'crop': picture_options['crop']}
        breakpoints = getattr(
            settings,
            'DJANGOCMS_PICTURE_RESPONSIVE_IMAGES_VIEWPORT_BREAKPOINTS',
            [576, 768, 992],
        )

        for size in filter(lambda x: x < picture_width, breakpoints):
            thumbnail_options['size'] = (size, size)
            srcset.append((int(size), thumbnailer.get_thumbnail(thumbnail_options)))

        return srcset

    @property
    def img_src(self):
        # we want the external picture to take priority by design
        # please open a ticket if you disagree for an open discussion
        if self.external_picture:
            return self.external_picture
        # picture can be empty, for example when the image is removed from filer
        # in this case we want to return an empty string to avoid #69
        elif not self.picture:
            return ''
        # return the original, unmodified picture
        elif self.use_no_cropping:
            return self.picture.url

        picture_options = self.get_size(
            width=self.width or 0,
            height=self.height or 0,
        )

        thumbnail_options = {
            'size': picture_options['size'],
            'crop': picture_options['crop'],
            'upscale': picture_options['upscale'],
            'subject_location': self.picture.subject_location,
        }

        thumbnailer = get_thumbnailer(self.picture)
        return thumbnailer.get_thumbnail(thumbnail_options).url


class PluginPicture(AbstractPicture, CMSPlugin):

    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    # ИЗНАЧАЛЬНО БЫЛО В КЛАССЕ AbstractPicture
    # cmsplugin_ptr = models.OneToOneField(
    #     CMSPlugin,
    #     related_name='%(app_label)s_%(class)s',
    #     parent_link=True,
    #     on_delete=models.CASCADE,
    # )

    def copy_relations(self, oldinstance):
        # Because we have a ForeignKey, it's required to copy over
        # the reference from the instance to the new plugin.
        self.picture = oldinstance.picture

    class Meta:
        abstract = False
        verbose_name = "изображение"
        verbose_name_plural = "изображения"


class AlbumPicture(AbstractPicture):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, 
                            #   blank=True, null=True,
                              verbose_name="Альбом")
    class Meta:
        abstract = False
        verbose_name = "фото"
        verbose_name_plural = "фото"



# =========================== VIDEO ====================================#

"""
Enables the user to add a "Video player" plugin that can render content
from external resources through an embed link or upload single files as
sources to be displayed in an HTML5 player.
"""
import sys

# from django.conf import settings
# from django.core.exceptions import ValidationError
# from django.db import models
# from django.utils.translation import gettext
# from django.utils.translation import gettext_lazy as _

# from cms.models import CMSPlugin

# from djangocms_attributes_field.fields import AttributesField
from filer.fields.file import FilerFileField
# from filer.fields.image import FilerImageField


if sys.version_info.major < 3:  # pragma: no cover
    from urlparse import urlparse, parse_qsl, urlunparse
    from urllib import urlencode
else:
    from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


# The mp4 file format is supported by all major browsers
def get_extensions():
    extensions = getattr(
        settings,
        'DJANGOCMS_VIDEO_ALLOWED_EXTENSIONS',
        ['mp4', 'webm', 'ogv'],
    )
    return extensions


# Add additional choices through the ``settings.py``.
def get_templates():
    return [
        ('default', _('Default')),
    ] + getattr(
        settings,
        'DJANGOCMS_VIDEO_TEMPLATES',
        [],
    )


class VideoPlayer(CMSPlugin):
    """
    Renders either an Iframe when ``link`` is provided or the HTML5 <video> tag
    """
    template = models.CharField(
        verbose_name=_('Template'),
        choices=get_templates(),
        default=get_templates()[0][0],
        max_length=255,
    )
    label = models.CharField(
        verbose_name=_('Label'),
        blank=True,
        max_length=255,
    )
    embed_link = models.CharField(
        verbose_name=_('Встраиваемое видео'),
        blank=True,
        max_length=255,
        help_text=_(
            'Используйте это поля для встраивания видео с внешних видеосервисов '
            'таких как Youtube, VK, Vimeo и др. '
        ),
    )
    source_file = FilerFileField(
        verbose_name=_('Файл видео'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    parameters = AttributesField(
        verbose_name=_('Параметры'),
        blank=True,
        # help_text=_(
        #     'Parameters are appended to the video link if provided.'
        # ),
    )
    poster = FilerImageField(
        verbose_name=_('Обложка'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    attributes = AttributesField(
        verbose_name=_('Атрибуты'),
        blank=True,
    )
    width = models.PositiveIntegerField(
        verbose_name="Ширина",
        blank=True,
        null=True,
        help_text=_(
            'Ширина плеера в пикселях (по умолчанию ширина 100%)'
        ),
    )
    height = models.PositiveIntegerField(
        verbose_name="Высота",
        default=400,
        help_text=_(
            'Высота плеера в пикселях'
        ),
    )

    class Meta:
        verbose_name = "видео"

    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.label or self.embed_link or str(self.pk)

    def copy_relations(self, oldinstance):
        # Because we have a ForeignKey, it's required to copy over
        # the reference from the instance to the new plugin.
        self.poster = oldinstance.poster
        self.source_file = oldinstance.source_file

    @property
    def embed_link_with_parameters(self):
        if not self.embed_link:
            return ''
        if not self.parameters:
            return self.embed_link
        return self._append_url_parameters(self.embed_link, self.parameters)

    def _append_url_parameters(self, url, params):
        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        return urlunparse(url_parts)

    def clean(self):
        if self.source_file and self.source_file.extension not in get_extensions():
            raise ValidationError(
                gettext('Неверный формат файла: {extension}.')
                .format(extension=self.source_file.extension)
            )

class VideoSource(CMSPlugin):
    """
    Renders the HTML <source> element inside of <video>.
    """
    source_file = FilerFileField(
        verbose_name=_('Source'),
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    text_title = models.CharField(
        verbose_name=_('Title'),
        blank=True,
        max_length=255,
    )
    text_description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
    )
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
    )

    def __str__(self):
        if self.source_file_id and self.source_file.label:
            return self.source_file.label
        return str(self.pk)

    def clean(self):
        if self.source_file and self.source_file.extension not in get_extensions():
            raise ValidationError(
                gettext('Incorrect file type: {extension}.')
                .format(extension=self.source_file.extension)
            )

    def get_short_description(self):
        if self.source_file_id and self.source_file.label:
            return self.source_file.label
        return gettext('<file is missing>')

    def copy_relations(self, oldinstance):
        # Because we have a ForeignKey, it's required to copy over
        # the reference from the instance to the new plugin.
        self.source_file = oldinstance.source_file


class VideoTrack(CMSPlugin):
    """
    Renders the HTML <track> element inside <video>.
    """
    KIND_CHOICES = [
        ('subtitles', _('Subtitles')),
        ('captions', _('Captions')),
        ('descriptions', _('Descriptions')),
        ('chapters', _('Chapters')),
    ]

    kind = models.CharField(
        verbose_name=_('Kind'),
        choices=KIND_CHOICES,
        max_length=255,
    )
    src = FilerFileField(
        verbose_name=_('Source file'),
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    srclang = models.CharField(
        verbose_name=_('Source language'),
        blank=True,
        max_length=255,
        help_text=_('Examples: "en" or "de" etc.'),
    )
    label = models.CharField(
        verbose_name=_('Label'),
        blank=True,
        max_length=255,
    )
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
    )

    def __str__(self):
        label = self.kind
        if self.srclang:
            label += ' ({})'.format(self.srclang)
        return label
