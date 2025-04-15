from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from filer.fields.file import File
from core.models import OrderedModel
from easy_thumbnails.files import get_thumbnailer
from django.urls import reverse, NoReverseMatch
from phonenumber_field.modelfields import PhoneNumberField
from cms.models.fields import PlaceholderField, PageField
from cms.models.pluginmodel import CMSPlugin
from django.dispatch import receiver
import os


class StructureBase(OrderedModel):

    
    class Meta:
        abstract = True


class CategoryOrganization(StructureBase):
    name = models.CharField(verbose_name="Полное название", max_length=128)

    class Meta:
        verbose_name = "вид организаций"
        verbose_name_plural = "виды организаций"

    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return "{}?category={}".format(reverse("structure:index"), self.pk)
    

class Organization(StructureBase):
    category = models.ForeignKey(CategoryOrganization, verbose_name="Вид организации (не обязательно)",
                                 on_delete=models.SET_NULL, blank=True, null=True)
    parent = models.ForeignKey('self', verbose_name="Родительская организация",
                            on_delete=models.SET_NULL,
                            blank=True, null=True,)
    # уровень вложенности записи
    level = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    # номер в общем списке, учитывая древовидную структуру
    list_order = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    name = models.CharField(verbose_name="Полное название", max_length=256)
    short_name = models.CharField(verbose_name="Краткое название", max_length=128, )
    address = models.CharField(verbose_name="Адрес", max_length=256,
                             blank=True, null=True)
    phone = PhoneNumberField(verbose_name="Телефон приемной")
    fax = models.CharField(verbose_name="Факс приемной", max_length=32,
                             blank=True, null=True)
    email = models.EmailField(verbose_name='Электронная почта',
                              blank=True, null=True)
    site = models.URLField(verbose_name="Сайт", blank=True, null=True)
    shedule = models.CharField(verbose_name="График работы", max_length=256,
                              blank=True, null=True)
    phone = models.CharField(verbose_name="Телефон приемной", max_length=32,
                             blank=True, null=True)
    logo = FilerImageField(verbose_name="Логотип", 
                           on_delete=models.CASCADE, 
                           blank=True, null=True)
    # content = PlaceholderField('content')
    page = PageField(verbose_name="Ссылка на страницу", blank=True, null=True)

    # PRIEM?
    # DOCUMENT (основной документ, положение, устав)?
    # ВИДЫ ДЕЯТЕЛЬНОСТИ? (САМБО ДЗЮДО И т.д.)?

    def __str__(self):
        return self.short_name
    
    def leveled_name(self):
        if self.level > 1:
            return '|---' * (self.level - 1) + self.name
        else:
            return self.name

    leveled_name.short_description = "Название"

    def childs(self):
        return Organization.objects.filter(parent=self)

    def get_otdels(self):
        return self.otdel_set.all()
    
    def apparat(self):
        return self.sotrudnik_set.filter(apparat=True)
    
    def update_list_order(self, parent_id=None, start_order=1):
        '''обновляет порядок всех элементов при выводе списком'''
        # получаем соседние объекты
        menus = list(Organization.objects.filter(parent_id=parent_id).order_by('order'))
        if len(menus) == 0:
            return start_order

        new_order = start_order
        for obj in menus:
            obj.list_order = new_order
            obj.save(update_fields=['list_order'], lock_recursion=True)
            new_order = obj.update_list_order(parent_id=obj.id, start_order= new_order + 1)
        return new_order

    def save(self, lock_recursion=False, *args, **kwargs):
        if self.parent_id:
            self.level = Organization.objects.get(id=self.parent_id).level + 1
        else:
            self.level = 1

        super().save(*args, **kwargs)

        # save method для OrderedModel
        if not lock_recursion:
            self.update_order(
                list_of_objects = list(
                    Organization.objects.filter(parent=self.parent).exclude(id=self.id)
                    )
            )
            # обновляем номера в общем списке
            self.update_list_order()

    def logo_thumb_src(self):
        logo = self.logo
        if not logo:
            return ""

        thumbnail_options = {
            'size': (155, 200),
            'crop': False,
            'upscale': True,
            'subject_location': logo.subject_location,
        }
        thumbnailer = get_thumbnailer(logo)
        return thumbnailer.get_thumbnail(thumbnail_options).url

    def get_absolute_url(self):
        return self.page.get_absolute_url() if self.page else None
        # return reverse("org-detail", kwargs={"pk": self.pk})
    

    class Meta:
        ordering = ['list_order' ]
        verbose_name = "организация"
        verbose_name_plural = "организации"


class Activity(StructureBase):
    name = models.CharField("Название")
    logo = FilerImageField(verbose_name="Лого", 
                           on_delete=models.CASCADE)

    class Meta:
        verbose_name = "вид деятельности"
        verbose_name_plural = "виды деятельности"

    def __str__(self):
        return self.name

    def thumb_src(self):
        image = self.logo
        if not image:
            return None

        thumbnail_options = {
            'size': (193, 115),
            'crop': True,
            'upscale': True,
            'subject_location': image.subject_location,
        }
        thumbnailer = get_thumbnailer(image)
        return thumbnailer.get_thumbnail(thumbnail_options).url
    
    def get_absolute_url(self):
        try:
            return "{}?activity={}".format(reverse("department:index"), self.pk)
        except NoReverseMatch:
            return "#"

class Department(StructureBase):

    organization = models.ForeignKey(Organization, verbose_name="Организация", on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, verbose_name="Вид деятельности", on_delete=models.CASCADE)
    name = models.CharField("Название")
    schedule  = models.CharField("Режим работы", max_length=256, blank=True, null=True)
    address_same = models.BooleanField("Адрес совпадает с адресом организации", default=True)
    address = models.CharField("Адрес", max_length=512, blank=True, null=True,
                               help_text="Заполняется если адрес секции не совпадает с адресом организации")
    phone = PhoneNumberField(verbose_name="Телефон", blank=True, null=True)
    description = HTMLField("Описание")

    def __str__(self):
        return self.name
    
    def get_address(self):
        return self.organization.address if self.address_same else self.address

    def get_photos(self):
        return self.photodepartment_set.all()

    class Meta:
        verbose_name = "секция"
        verbose_name_plural = "секции"

class PhotoDepartment(StructureBase):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    photo = FilerImageField(verbose_name="Фото", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "фото"
        verbose_name_plural = "фото"

    def thumb_src(self):
        image = self.photo
        if not image:
            return None

        thumbnail_options = {
            'size': (150, 130),
            'crop': True,
            'upscale': True,
            'subject_location': image.subject_location,
        }
        thumbnailer = get_thumbnailer(image)
        return thumbnailer.get_thumbnail(thumbnail_options).url



@receiver(models.signals.post_delete, sender=PhotoDepartment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Удаляет файл при удалении объекта
    """
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            # delete file from file system
            os.remove(instance.photo.path)
            # delete Filer File object
            File.objects.filter(id=instance.photo_id).delete()


class Otdel(StructureBase):
    organization = models.ForeignKey(Organization, verbose_name="Организация",
                                     on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=256)
    page = PageField(verbose_name="Ссылка на страницу", blank=True, null=True,
                          help_text="Не обязательно")
    # PHONEs?


    def __str__(self):
        return self.name

    def save(self, lock_recursion=False, *args, **kwargs):
        # save method для OrderedModel
        super().save(*args, **kwargs)

        if not lock_recursion:
            self.update_order(
                list_of_objects = list(
                    Otdel.objects.filter(organization=self.organization).exclude(id=self.id)
                    )
            )

    def get_employees(self):
        return self.sotrudnik_set.all()

    def phones(self):
        return self.phone_set.all()

    def get_absolute_url(self):
        return self.page.get_absolute_url() if self.page else None

    class Meta:
        ordering = ['organization', 'order' ]
        verbose_name = "отдел"
        verbose_name_plural = "отделы"


class Sotrudnik(StructureBase):
    organization = models.ForeignKey(Organization, verbose_name="Организация",
                                     on_delete=models.CASCADE)
    otdel = models.ForeignKey(Otdel, verbose_name="Отдел",
                            on_delete=models.SET_NULL,
                            blank=True, null=True,
                            help_text="Если не заполнено, сотрудник будет \
                                отображаться в разделе \"Прочие сотрудники\" организации")
    lastname = models.CharField(verbose_name="Фамилия", max_length=32)
    firstname = models.CharField(verbose_name="Имя", max_length=32)
    surname = models.CharField(verbose_name="Отчество", max_length=32)
    position = models.CharField(verbose_name="Должность", max_length=128)
    photo = FilerImageField(verbose_name="Фото", 
                           on_delete=models.CASCADE, 
                           blank=True, null=True)
    apparat = models.BooleanField(verbose_name="В аппарате управления",
                                  default=False,
                                  help_text="Если отмечено, сотрудник будет выведен \
                                  в разделе \"Аппарат управления\" организации")
    page = PageField(verbose_name="Ссылка на страницу", blank=True, null=True,
                          help_text="Не обязательно")
    # PHONE?


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
                    Sotrudnik.objects.filter(organization=self.organization, otdel=self.otdel).exclude(id=self.id)
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

    def phones(self):
        phones = self.phone_set.all()  
        if phones:
            return phones
        if self.otdel:
            return self.otdel.phones()

    def get_absolute_url(self):
        return self.page.get_absolute_url() if self.page else None

    class Meta:
        ordering = ['organization', 'otdel', 'order' ]
        verbose_name = "сотрудник"
        verbose_name_plural = "сотрудники"


class Phone(models.Model):

    sotrudnik = models.ForeignKey(Sotrudnik, on_delete=models.CASCADE, 
                                  blank=True, null=True)
    otdel = models.ForeignKey(Otdel, on_delete=models.CASCADE, 
                                  blank=True, null=True)
    number = PhoneNumberField(verbose_name="Номер")

    def __str__(self):
        return self.number.as_international

    class Meta:
        verbose_name = "телефон"
        verbose_name_plural = "телефоны"



class AttributesPlugin(CMSPlugin):
    """Модель для плагина выводящего атрибуты оргнизации"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, 
                                 verbose_name="Организация")

class LogoPlugin(CMSPlugin):
    """Модель для плагина выводящего логотип оргнизации"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, 
                                 verbose_name="Организация")

class OtdelOrganizationPlugin(CMSPlugin):
    """Модель для плагина выводящего сотрудников по отделам"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, 
                                 verbose_name="Организация")
    show_detail_link = models.BooleanField("Отображать ссылку на страницы отделов и сотрудников",
                                           default=True, help_text="если она есть")       

LAYOUT_CHOICES = [
    ("rows", "Построчно"),
    ("blocks", "Блоки"),
]
class SotrudnikOrganizationPlugin(CMSPlugin):
    """Модель для плагина выводящего сотрудников"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, 
                                 verbose_name="Организация")
    otdel = models.ForeignKey(Otdel, verbose_name="Отдел",
                            on_delete=models.SET_NULL,
                            blank=True, null=True,
                            help_text="Если не заполнено, сотрудник будет \
                                отображаться в разделе \"Прочие сотрудники\" организации")
    apparat = models.BooleanField(verbose_name="Только аппарат управления",
                                  default=False,
                                  help_text="Оставить только сотрудников аппарата (поле \"Отдел\" будет проигнорировано)" )
    layout = models.CharField("Макет", choices=LAYOUT_CHOICES, default=LAYOUT_CHOICES[0][0])

    show_detail_link = models.BooleanField("Отображать ссылку на страницу сотрудников",
                                           default=True, help_text="если она есть")       
    
LAYOUT_CHOICES = [
    ("blocks", "Блоки (без лого)"),
    ("image-blocks", "Блоки с логотипом на фоне"),
]
class ActivityPlugin(CMSPlugin):
    """Модель для плагина выводящего список видов деятельности"""
    layout = models.CharField("Макет", choices=LAYOUT_CHOICES, default=LAYOUT_CHOICES[0][0])


class DepartmentPlugin(CMSPlugin):
    """Модель для плагина выводящего список секций по виду деятельности"""
    activity = models.ForeignKey(Activity, verbose_name="Вид спорта", on_delete=models.CASCADE)

    def get_departments(self):
        return Department.objects.filter(activity=self.activity)