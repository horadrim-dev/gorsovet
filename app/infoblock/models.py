from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from filer.models.imagemodels import Image
import uuid
from djangocms_text_ckeditor.fields import HTMLField
from colorfield.fields import ColorField

CONTAINER_CHOICES = [
    ('container', 'С отступами справа и слева'),
    ('container-fluid no-paddings', 'Во всю ширину'),
]

class Infoblock(CMSPlugin):

    height = models.PositiveSmallIntegerField("Высота слайдера", default=450)
    # def get_slides(self):
    #     return self.slide_set.all()

    def generate_id(self):
        return str(uuid.uuid4().fields[-1])[:7]

    # def copy_relations(self, oldinstance):
        # Before copying related objects from the old instance, the ones
        # on the current one need to be deleted. Otherwise, duplicates may
        # appear on the public version of the page
        # self.slide_set.all().delete()

        # for slide in oldinstance.slide_set.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance

            # slide.pk = None
            # slide.plugin = self
            # slide.save()

class Slide(CMSPlugin):
    # plugin = models.ForeignKey(
    #         Infoblock,
    #         on_delete=models.CASCADE,
    #     )
    # title = models.CharField("Заголовок", max_length=1024, default="", blank=True, null=True)
    # description = HTMLField("Описание", default="", blank=True, null=True)
    background_color = ColorField(default='#FFFFFF', verbose_name="Цвет фона",
        blank=True, null=True
    )
    container_type = models.CharField(
        max_length=64,
        verbose_name="Расположение контента",
        choices=CONTAINER_CHOICES,
        default='container',
    )
    # image = FilerImageField(
    #     verbose_name=_('Изображение'),
    #     on_delete=models.CASCADE,
    #     blank=True, null=True
    # )
    # thumb_width = models.PositiveSmallIntegerField("Ширина", default=400)
    # thumb_height = models.PositiveSmallIntegerField("Высота", default=300)

    # def __str__(self):
    #     return self.title if self.title else super(self)

    # def get_width_height_thumb(self):
        # return "0x0"
        # return "{}x{}".format(self.thumb_width, self.thumb_height)

    class Meta:
        verbose_name = "слайд"
        verbose_name_plural = "слайды"


# LINK_CLASS_CHOICES = [
#     ('btn btn-lg', 'стиль 1'),
#     ('btn btn-lg btn-border', 'стиль 2'),
# ]

# class Link(models.Model):
#     slide = models.ForeignKey(
#             Infoblock,
#             on_delete=models.CASCADE,
#         )
#     title = models.CharField("Название", max_length=64, default="", blank=True, null=True)
#     icon = models.CharField(verbose_name="Иконка",
#                                 help_text='Названия иконок брать <a href="https://fontawesome.com/v4/icons/" target="blank">отсюда</a>', 
#                                 max_length=32, default="", blank=True, null=True)
#     url = models.URLField("Ссылка", default="")
#     link_class = models.CharField(
#         max_length=64, verbose_name="Стиль ссылки",
#         choices=LINK_CLASS_CHOICES, default='',
#     )