from tabnanny import verbose
from django.db import models
from cms.models.pluginmodel import CMSPlugin
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from django.urls import reverse
# from filer.models.imagemodels import Image
import uuid
import datetime

class Attachments(CMSPlugin):
    # num_items = models.PositiveSmallIntegerField("Количество отображаемых элементов", default=5)
    # def get_slides(self):
    #     return self.slide_set.all()

    # def generate_id(self):
    #     return str(uuid.uuid4().fields[-1])[:7]

    def copy_relations(self, oldinstance):
        # Before copying related objects from the old instance, the ones
        # on the current one need to be deleted. Otherwise, duplicates may
        # appear on the public version of the page
        self.attachment_set.all().delete()

        for slide in oldinstance.attachment_set.all():
            # instance.pk = None; instance.pk.save() is the slightly odd but
            # standard Django way of copying a saved model instance
            slide.pk = None
            slide.plugin = self
            slide.save()

class Attachment(models.Model):
    plugin = models.ForeignKey(Attachments, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField("Название", max_length=512)
    _file = FilerFileField(verbose_name="Файл", on_delete=models.CASCADE)
    extension = models.CharField(default="", max_length=16, blank=True, null=True,
                                verbose_name="Расширение файла")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")
    hits = models.PositiveIntegerField(default=0, verbose_name="Кол-во загрузок")


    def save(self,  *args, **kwargs):
        # считываем расширение файла
        if self._file:
            self.extension = self._file.path.split('.')[-1].lower()

        super().save(*args, **kwargs)

    def url(self):
        '''Формирует url для скачивания'''
        return reverse('attachment_download', kwargs={'id': self.id})

    def __str__(self):
        return self.name

    @property
    def file(self):
        return self._file

    @property
    def filename(self):
        return "{}.{}".format(self.name[:100], self.extension)
    
    def fa_icon(self):
        """Возвращает название иконки (font awesome 4.7) для файла документа """

        ARCHIVE = { "ext" : ("rar", "zip", "7z"),  "icon": "fa-file-archive-o"}
        WORD = {"ext": ("doc", "docx"), "icon": "fa-file-word-o"}
        EXCEL = {"ext": ("xls", "xlsx"), "icon": "fa-file-excel-o"}
        VIDEO = {"ext": ("mp4", "avi", "mkv"), "icon": "fa-file-video-o"}
        PDF = {"ext" : ("pdf", ), "icon": "fa-file-pdf-o"}

        file_types = [ARCHIVE, WORD, EXCEL, VIDEO, PDF]
        for file_type in file_types:
            if self.extension in file_type["ext"]:
                return file_type["icon"]

        return "fa-file-o"


    class Meta:
        verbose_name = "вложение"
        verbose_name_plural = "вложения"
        ordering = ["-updated_at"]

