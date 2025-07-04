from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from core.models import OrderedModel
from filer.fields.image import FilerImageField
from django.urls import reverse
from easy_thumbnails.files import get_thumbnailer

class DeputatyBase(OrderedModel):

    class Meta:
        abstract = True

class Sozyv(DeputatyBase):
    name = models.CharField("Название", max_length=256, help_text="Пример: Созыв 3")
    period = models.CharField("Период", max_length=256, help_text="Пример: 04.2003 - 10.2008",
                              blank=True, null=True)

    def save(self, lock_recursion=False, *args, **kwargs):
        # save method для OrderedModel
        super().save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(
                    Sozyv.objects.all().exclude(id=self.id)
                    )
            )

    def __str__(self):
        return "{} ({})".format(self.name, self.period)

    @property
    def fullname(self):
        return self.__str__()

    def get_absolute_url(self):
        return "{}?sozyv={}".format(reverse('deputaty:index'), str(self.id))

    class Meta:
        ordering = ['order' ]
        verbose_name = "созыв"
        verbose_name_plural = "созывы"


class Deputat(DeputatyBase):
    sozyvy = models.ManyToManyField(Sozyv, verbose_name="Созыв", )
    lastname = models.CharField(verbose_name="Фамилия", max_length=128)
    firstname = models.CharField(verbose_name="Имя", max_length=128)
    surname = models.CharField(verbose_name="Отчество", max_length=128)

    description = HTMLField(verbose_name="Описание", blank=True, null=True)
    # birthday = models.DateField(verbose_name="День рождения", blank=True, null=True)
    # education = models.CharField(verbose_name="Образование", max_length=1024,
    #                              blank=True, null=True)
    # membership = models.CharField(verbose_name="Партийность", max_length=1024,
    #                               blank=True, null=True)
    # academic_title = models.CharField(verbose_name="Ученая степень, звание", max_length=1024,
    #                               blank=True, null=True)
    # awards = models.TextField(verbose_name="Награды", max_length=2048,
    #                               blank=True, null=True)
    # position = models.CharField(verbose_name="Место работы, должность", max_length=1024,
    #                               blank=True, null=True)
    photo = FilerImageField(verbose_name="Фото", 
                           on_delete=models.CASCADE, 
                           blank=True, null=True)

    def name(self):
        return "{} {} {}".format(self.lastname, self.firstname, self. surname)
    name.short_description = "ФИО"

    def __str__(self):
        return " ".join([str(self.lastname), str(self.firstname), str(self.surname)])

    def save(self, lock_recursion=False, *args, **kwargs):
        # save method для OrderedModel
        super().save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(
                    Deputat.objects.all().exclude(id=self.id)
                    )
            )

    def photo_thumb_src(self):
        photo = self.photo
        if not photo:
            return ""

        thumbnail_options = {
            'size': (155, 200),
            'crop': True,
            'upscale': True,
            'subject_location': photo.subject_location,
        }
        thumbnailer = get_thumbnailer(photo)
        return thumbnailer.get_thumbnail(thumbnail_options).url


    # def get_absolute_url(self):
    #     return self.page.get_absolute_url() if self.page else None

    class Meta:
        ordering = ['lastname',  'order' ]
        verbose_name = "депутат"
        verbose_name_plural = "депутаты"