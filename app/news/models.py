from email.policy import default
from django.db import models
from filer.fields.image import FilerImageField, FilerFileField
from djangocms_text_ckeditor.fields import HTMLField
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.urls import reverse
from cms.models.pluginmodel import CMSPlugin
# from cms.models.fields import PlaceholderField
from taggit.managers import TaggableManager
# from taggit_autosuggest.managers import TaggableManager
# from taggit.models import TagBase
import uuid
import datetime
from core.utils import slugify_rus
import locale
from easy_thumbnails.files import get_thumbnailer
from attachments.models import Attachment
import random

class ContentManager(models.Manager):

    def published(self):
        return self.filter(published=True, published_at__lte=datetime.date.today())


class PostCategory(models.Model):
    title = models.CharField("Название", max_length=256)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    @property
    def name(self):
        return self.title

    def get_absolute_url(self):
        return "{}?category={}".format(reverse("news:index"), self.id) 
    
# class TagPost(TagBase):
#     class Meta:
#         verbose_name = "тег"
#         verbose_name_plural = "теги"

# POSTER_PLUGINS = ("PicturePlugin", "SliderItemPlugin", "VideoPlayerPlugin" )

class Post(models.Model):
    title = models.CharField(
        default="", max_length=1000, verbose_name="Заголовок")

    alias = models.SlugField(default="", blank=True, unique=True,
                             max_length=1000, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.")
    category = models.ForeignKey(PostCategory, verbose_name="Категория", on_delete=models.SET_NULL, blank=True, null=True)
    published = models.BooleanField(default=True, verbose_name='Опубликовано')
    published_at = models.DateTimeField(default=datetime.datetime.now, 
                                    verbose_name="Дата публикации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")

    text = HTMLField("Содержимое", configuration='CKEDITOR_SETTINGS_POST', default="", blank=True, null=True)
    # content = PlaceholderField('content')

    # placeholder = PlaceholderField('post', related_name="news_post")

    cover_image = FilerImageField(verbose_name="Обложка поста", 
                                  on_delete=models.CASCADE, 
                                  blank=True, null=True,)
                                #   help_text="Если не задано - будет использовано первое изображение из содержимого поста")

    tags = TaggableManager()

    IMAGE_POSITION_CHOICES = [
        ('left', 'Слева'),
        ('stretch', 'Растянуть'),
        ('right', 'Справа'),
        ('hide', 'Скрыть'),
    ]
    # image_position = models.CharField(max_length=64, choices=IMAGE_POSITION_CHOICES, default=IMAGE_POSITION_CHOICES[0][0],
    #     verbose_name="Расположение изображения")

    # placeholder_top = PlaceholderField('top', related_name="post_top")
    # placeholder_bottom = PlaceholderField('bottom', related_name="post_bottom")

    objects = ContentManager()

    @property
    def gen_id(self):
        return str(uuid.uuid4().fields[-1])[:7]

    def get_absolute_url(self):
        return reverse("news:detail", kwargs={"slug": self.alias})

    def __str__(self):
        return self.title

    def save(self, lock_recursion=False, *args, **kwargs):
        # только при создании объекта, id еще не существует
        if not self.id or not self.alias:
            # заполняем алиас
            self.alias = slugify_rus(self.title)

            # проверяем что таких постов с таким алиасом нет
            try:
                qs = Post.objects.get(alias=self.alias)
            except ObjectDoesNotExist:
                pass
            else:
                self.alias += ''.join(random.choices('0123456789', k=6))

        super().save(*args, **kwargs)
        

    def pubdate_has_arrived(self):
        return False if self.published_at > datetime.date.today() else True

    # def has_content_plugins(self):
    #     return CMSPlugin.objects.filter(placeholder_id=self.content_id).count()
    
    @property
    def poster(self):
        if self.cover_image:
            return {"type": "image", "image": self.cover_image }

    #     plugin = CMSPlugin.objects.filter(placeholder_id=self.content_id, 
    #                                       plugin_type__in=POSTER_PLUGINS) \
    #                                 .order_by('position') \
    #                                 .first()
    #     # return plugin or None
    #     if not plugin:
    #         return None
    #     if plugin.plugin_type == "PicturePlugin":
    #         return {"type":"image", "image" :plugin.medialer_pluginpicture.picture }
    #     elif plugin.plugin_type == "SliderItemPlugin":
    #         return {"type":"image", "image" :plugin.slider_slide.image }
    #     elif plugin.plugin_type == "VideoPlayerPlugin":
    #         return {"type":"video", "videoplayer" :plugin.medialer_videoplayer }


    def thumb_src(self):
        # poster = self.poster
        # if not poster or poster['type'] == "video":
        #     return ""
        # image = poster['image']
        image = self.cover_image
        if not image:
            return None

        thumbnail_options = {
            'size': (300, 200),
            'crop': True,
            'upscale': True,
            'autocrop': False,
            'subject_location': image.subject_location,
        }
        thumbnailer = get_thumbnailer(image)
        return thumbnailer.get_thumbnail(thumbnail_options).url

    @property
    def description(self):
        # text = CMSPlugin.objects.filter(placeholder_id=self.content_id, plugin_type="TextPlugin").first()
        # return self.text.djangocms_text_ckeditor_text.body if self.text else False 
        return self.text

    def images(self):
        return self.photopost_set.all()

    def videos(self):
        return self.videopost_set.all()

    def attachments(self):
        return self.attachmentpost_set.all()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-published_at']


class PhotoPost(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = FilerImageField(verbose_name="Фото", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")

    def __str__(self):
        return self.image.original_filename
    
    def thumb_src(self):
        image = self.image

        thumbnail_options = {
            'size': (360, 240),
            'crop': True,
            'upscale': True,
            'autocrop': False,
            'subject_location': image.subject_location,
        }
        thumbnailer = get_thumbnailer(image)
        return thumbnailer.get_thumbnail(thumbnail_options).url
    

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
        ordering = ['-created_at']


class VideoPost(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    videofile = FilerFileField(verbose_name="Видеофайл", on_delete=models.CASCADE,
                           blank=True, null=True)
    external_url = models.URLField("Ссылка на внешнее видео", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")


    def __str__(self):
        if self.videofile:
            return self.videofile.original_filename
        if self.external_url:
            return "Внешнее видео"
        return None
    
    def clean(self):
        # проверка на заполнение обоих полей
        if self.videofile and self.external_url:
            raise ValidationError("Источник видео, должен быть только один: видеофайл или ссылка на видео")

        if not self.videofile and not self.external_url:
            raise ValidationError("Не выбран источник видео, загрузите файл или укажите ссылку на видео")

    def src(self):
        if self.videofile:
            return self.videofile.url
        if self.external_url:
            return self.external_url
        return None

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ['-created_at']


class AttachmentPost(Attachment):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    plugin = models.NOT_PROVIDED

    class Meta:
        verbose_name = "вложение"
        verbose_name_plural = "вложения"
        ordering = ["-updated_at"]

LAYOUT_CHOICES = [ ("blocks", "Блоки"), ("list", "Список") ] # (ширина колонки, кол-во элементов)
BOOTSTRAP_COL_CHOICES = [ ("12", 1), ("6", 2), ("4", 3), ] # (ширина колонки, кол-во элементов)
class NewsPlugin(CMSPlugin):

    num_objects = models.PositiveIntegerField("Количество новостей", default=3)
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name="Категория")
    layout = models.CharField("Макет отображения", max_length=16,
                                     choices=LAYOUT_CHOICES, default=LAYOUT_CHOICES[0][0])
    bootstrap_col = models.CharField("Количество блоков в строке", max_length=8,
                                     choices=BOOTSTRAP_COL_CHOICES, default=BOOTSTRAP_COL_CHOICES[2][0])

    def generate_id(self):
        return str(uuid.uuid4().fields[-1])[:7]
    
    def get_absolute_url(self):
        if self.category:
            return self.category.get_absolute_url()
        
        return reverse("news:index")