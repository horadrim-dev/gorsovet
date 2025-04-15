from tabnanny import verbose
from django.db import models
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
# from filer.models.imagemodels import Image
import uuid


class Slider(CMSPlugin):

    num_items = models.PositiveSmallIntegerField("Количество отображаемых элементов", default=5)
    # def get_slides(self):
    #     return self.slide_set.all()

    def generate_id(self):
        return str(uuid.uuid4().fields[-1])[:7]

    # def copy_relations(self, oldinstance):
    #     # Before copying related objects from the old instance, the ones
    #     # on the current one need to be deleted. Otherwise, duplicates may
    #     # appear on the public version of the page
    #     self.slide_set.all().delete()

    #     for slide in oldinstance.slide_set.all():
    #         # instance.pk = None; instance.pk.save() is the slightly odd but
    #         # standard Django way of copying a saved model instance
    #         slide.pk = None
    #         slide.slider = self
    #         slide.save()

class Slide(CMSPlugin):
    # slider = models.ForeignKey(
    #         Slider,
    #         on_delete=models.CASCADE,
    #     )
    # title = models.CharField("Название", max_length=255, help_text="Не обязательно", default="", blank=True, null=True)
    # subtitle = models.CharField("Подзаголовок", max_length=255, default="", blank=True, null=True)

    image = FilerImageField(
        verbose_name='Изображение',
        on_delete=models.CASCADE,
    )
    lightbox_on = models.BooleanField("Увеличивать изображение по клику", default=True)

    thumb_width = models.PositiveSmallIntegerField("Ширина", default=300)
    thumb_height = models.PositiveSmallIntegerField("Высота", default=200)
    url = models.URLField("Ссылка", help_text="Не обязательно", default="", blank=True, null=True)
    # def __str__(self):
    #     return self.title if self.title else ""

    def get_width_height_thumb(self):
        return "{}x{}".format(self.thumb_width, self.thumb_height)

    class Meta:
        verbose_name = "слайд"
        verbose_name_plural = "слайды"
