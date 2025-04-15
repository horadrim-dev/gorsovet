from email.policy import default
from django.db import models
from filer.fields.image import FilerImageField
from djangocms_text_ckeditor.fields import HTMLField
from django.urls import reverse
from cms.models.pluginmodel import CMSPlugin
from cms.models.fields import PlaceholderField
from taggit.managers import TaggableManager
# from taggit_autosuggest.managers import TaggableManager
# from taggit.models import TagBase
import uuid
import datetime
from core.utils import slugify_rus
import locale
from easy_thumbnails.files import get_thumbnailer

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

    def get_absolute_url(self):
        return "{}?category={}".format(reverse("news:index"), self.id) 
    
# class TagPost(TagBase):

#     class Meta:
#         verbose_name = "тег"
#         verbose_name_plural = "теги"

POSTER_PLUGINS = ("PicturePlugin", "SliderItemPlugin", "VideoPlayerPlugin" )

class Post(models.Model):
    title = models.CharField(
        default="", max_length=1000, verbose_name="Заголовок")

    alias = models.SlugField(default="", blank=True, unique=True,
                             max_length=1000, help_text="Краткое название транслитом через тире (пример: 'kratkoe-nazvanie-translitom'). Чем короче тем лучше. Для автоматического заполнения - оставьте пустым.")
    category = models.ForeignKey(PostCategory, verbose_name="Категория", on_delete=models.SET_NULL, blank=True, null=True)
    published = models.BooleanField(default=False, verbose_name='Опубликовано')
    published_at = models.DateField(default=datetime.date.today, 
                                    verbose_name="Дата публикации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")

    # text = HTMLField("Содержимое", configuration='CKEDITOR_SETTINGS_POST', default="", blank=True, null=True)
    content = PlaceholderField('content')

    # placeholder = PlaceholderField('post', related_name="news_post")

    cover_image = FilerImageField(verbose_name="Обложка поста", 
                                  on_delete=models.CASCADE, 
                                  blank=True, null=True,
                                  help_text="Если не задано - будет использовано первое изображение из содержимого поста")

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

        super().save(*args, **kwargs)

    def pubdate_has_arrived(self):
        return False if self.published_at > datetime.date.today() else True

    def has_content_plugins(self):
        return CMSPlugin.objects.filter(placeholder_id=self.content_id).count()
    
    @property
    def poster(self):
        if self.cover_image:
            return {"type": "image", "image": self.cover_image }

        plugin = CMSPlugin.objects.filter(placeholder_id=self.content_id, 
                                          plugin_type__in=POSTER_PLUGINS) \
                                    .order_by('position') \
                                    .first()
        # return plugin or None
        if not plugin:
            return None
        if plugin.plugin_type == "PicturePlugin":
            return {"type":"image", "image" :plugin.medialer_pluginpicture.picture }
        elif plugin.plugin_type == "SliderItemPlugin":
            return {"type":"image", "image" :plugin.slider_slide.image }
        elif plugin.plugin_type == "VideoPlayerPlugin":
            return {"type":"video", "videoplayer" :plugin.medialer_videoplayer }


    def thumb_src(self):
        poster = self.poster
        if not poster or poster['type'] == "video":
            return ""
        image = poster['image']

        thumbnail_options = {
            'size': (360, 240),
            'crop': False,
            'upscale': False,
            'autocrop': False,
            'subject_location': image.subject_location,
        }
        thumbnailer = get_thumbnailer(image)
        return thumbnailer.get_thumbnail(thumbnail_options).url

    @property
    def description(self):
        text = CMSPlugin.objects.filter(placeholder_id=self.content_id, plugin_type="TextPlugin").first()
        return text.djangocms_text_ckeditor_text.body if text else False 


    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-published_at']


class NewsPlugin(CMSPlugin):

    num_objects = models.PositiveIntegerField("Количество новостей", default=3)

    def generate_id(self):
        return str(uuid.uuid4().fields[-1])[:7]