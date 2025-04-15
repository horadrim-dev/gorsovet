from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from colorfield.fields import ColorField
from djangocms_text_ckeditor.fields import HTMLField
import uuid

TITLE_ALIGN_CHOICES = [
    ('center', 'По центру'),
    ('left', 'Слева'),
    ('right', 'Справа')
]
OVERLAY_OPACITY_CHOICES = [
    ('0', '0'),
    ('.1', '10%'),
    ('.25', '25%'),
    ('.5', '50%'),
    ('.75', '75%'),
    ('.90', '90%'),
    ('1', '100%'),
]

CONTAINER_CHOICES = [
    ('container', 'С отступами справа и слева'),
    ('container-fluid no-paddings', 'Во всю ширину'),
]

class BackgroundSection(CMSPlugin):

    # name = models.CharField("Название", max_length=255, default="", help_text="Системное название секции (отображается только в панели администрирования)")
    title = models.CharField("Заголовок", max_length=255, default="", blank=True, null=True, help_text="Не обязательно")
    title_align = models.CharField(
        max_length=16,
        verbose_name="Расположение заголовка",
        choices=TITLE_ALIGN_CHOICES,
        default=TITLE_ALIGN_CHOICES[0][0],
    )
    # text = HTMLField("Текст", default="", blank=True, null=True, help_text="Не обязательно")
    # text_bottom = HTMLField("Текст снизу секции", default="", blank=True, null=True, help_text="Не обязательно")

    background_image = FilerImageField(
        verbose_name=_('Фоновое изображение'),
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    thumb_width = models.PositiveSmallIntegerField("Ширина", default=0)
    thumb_height = models.PositiveSmallIntegerField("Высота", default=0)
    background_color = ColorField(default='#FFFFFF', verbose_name="Фоновый цвет", help_text="Опция будет проигнорирована, если задано фоновое изображение",
        blank=True, null=True
    )
    css_classes = models.CharField("CSS классы", max_length=256, help_text="указать классы через пробел", default="", blank=True, null=True)
    use_parallax = models.BooleanField(default=False, verbose_name="Использовать эффект параллакса")
    use_blur = models.BooleanField(default=False, verbose_name="Использовать эффект размытия")
    use_overlay = models.BooleanField(default=False, verbose_name="Использовать оверлей")
    overlay_color = ColorField(default='#FFFFFF', verbose_name="Цвет оверлея", help_text="Этот цвет будет накладываться на изображение",
        blank=True, null=True
    )
    overlay_opacity = models.CharField(
        max_length=8,
        verbose_name="Прозрачность оверлея",
        choices=OVERLAY_OPACITY_CHOICES,
        default='.5',
    )
    container_type = models.CharField(
        max_length=64,
        verbose_name="Расположение контента",
        choices=CONTAINER_CHOICES,
        default='container',
    )
    padding_top = models.PositiveSmallIntegerField("Отступ сверху (px)", default=50)
    padding_bottom = models.PositiveSmallIntegerField("Отступ снизу (px)", default=50)

    def generate_id(self):
        return str(uuid.uuid4().fields[-1])[:7]

    def get_width_height_thumb(self):
        return "{}x{}".format(self.thumb_width, self.thumb_height)

    def __str__(self):
        return self.title if self.title else ''
