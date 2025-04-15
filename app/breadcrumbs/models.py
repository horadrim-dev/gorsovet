from email.policy import default
from django.db import models
from django.utils.translation import gettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from colorfield.fields import ColorField
from djangocms_text_ckeditor.fields import HTMLField
import uuid


class Breadcrumbs(CMSPlugin):

    _title = models.CharField("Заголовок", max_length=255, default="", 
                             blank=True, null=True, 
                             help_text="Не обязательно. Если не заполнено - будет использован заголовок страницы.")

    white_mode = models.BooleanField("Текст белым цветом", default=False)
    # image = FilerImageField(
    #     verbose_name=_('Изображение'),
    #     on_delete=models.CASCADE,
    #     blank=True, null=True
    # )
    # thumb_width = models.PositiveSmallIntegerField("Ширина", default=400)
    # thumb_height = models.PositiveSmallIntegerField("Высота", default=300)

    @property
    def title(self):
        return self._title if self._title and self._title.strip() else None

    # @property
    # def width_height_thumb(self):
    #     return "{}x{}".format(self.thumb_width, self.thumb_height)

    def __str__(self):
        return self.__class__.__name__