from collections.abc import Iterable
from django.db import models
from djangocms_text_ckeditor.fields import HTMLField
import datetime
from filer.fields.image import FilerImageField
from easy_thumbnails.files import get_thumbnailer
from django.urls import reverse, NoReverseMatch
from cms.models.pluginmodel import CMSPlugin
import uuid
from django.utils import timezone
from recurrence.fields import RecurrenceField

class CategoryEvent(models.Model):
    name = models.CharField("Название категории", max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория мероприятий"
        verbose_name_plural = "категории мероприятий"

class Event(models.Model):
    '''Модель мероприятия'''
    category = models.ForeignKey(CategoryEvent, verbose_name="Категория", 
                                 on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField("Название мероприятия", max_length=512)

    poster = FilerImageField(
        verbose_name="Обложка",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    description = HTMLField(verbose_name="Описание", blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")


    class Meta:
        verbose_name = "мероприятие"
        verbose_name_plural = "мероприятия"
        # ordering = ['start_at']

    def __str__(self):
        return self.name


class SessionEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_time = models.TimeField(default=datetime.time(12, 0, 0), 
                                    verbose_name="Время начала")
    place = models.CharField("Место проведения", max_length=256, blank=True, null=True)
    postfix_name = models.CharField("Постфикс названия мероприятия", blank=True, null=True,
                                    help_text="Пример: День 1, Второй этап и т.д. \
                                               Будет отображено в квадратных скобках в \
                                               конце названия мероприятия.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее изменение")

    recurrences = RecurrenceField(verbose_name="Правила применения", blank=True, null=True)


    class Meta:
        verbose_name = "сессия"
        verbose_name_plural = "сессии"
        ordering = ['event']

    def save(self, *args, **kwargs):
        if self.pk is None:
            is_object_new = True
        else:
            is_object_new = False
            current_obj = SessionEvent.objects.get(pk=self.pk)

        super().save(*args, **kwargs)

        if is_object_new:
            self.create_event_entries()
        if not is_object_new and current_obj:
            if current_obj.recurrences != self.recurrences:
                self.delete_event_entries()
                self.create_event_entries()

    def create_event_entries(self):
        now = datetime.datetime.today() - datetime.timedelta(days=1)
        then = now.replace(year=now.year + 10)
        tz = timezone.get_current_timezone()

        entries = self.recurrences.between(
            datetime.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=tz),
            datetime.datetime(then.year, then.month, then.day, 0, 0, 0, tzinfo=tz),
            dtstart=datetime.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=tz),
            inc=False,
        )

        # assert False, [x for x in entries]

        for entry in entries:

            # Если подставлять время в полученные рекуренсы напрямую, смещаются даты мероприятий
            # Поэтому в рекуренсах время не меняем, а полученные объекты просто сортируются по start_time

            # start_time = datetime.datetime.combine(
            #     entry.date() + datetime.timedelta(days=1),
            #     self.start_time,
            #     tzinfo=tz
            # )
            #start_time = entry.replace(hour=self.start_time.hour, minute=self.start_time.minute)

            e = EventEntry.objects.create(
                start_at=entry,
                #start_at=start_time,
                event=self.event,
                session=self
            )
            e.save()

    def delete_event_entries(self):
        EventEntry.objects.filter(event=self.event, session=self).delete()



class EventEntryContentManager(models.Manager):

    def upcoming(self):
        return self.filter(start_at__gte=timezone.now().date())

    def upcoming_by_date(self, date):
        return self.upcoming().filter(start_at__date=date)
    # def finished(self):
    #     return self.filter(published=True, start_at__lte=datetime.datetime.now())

class EventEntry(models.Model):
    """Модель с расчитанными по дням событиями, обновляется при сохранении
    объектов SessionEvent (НЕ РЕДАКТИРУЕТСЯ НАПРЯМУЮ)"""

    start_at = models.DateTimeField(default=timezone.now, 
                                    verbose_name="Время начала")

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    session = models.ForeignKey(SessionEvent, on_delete=models.CASCADE)

    objects = EventEntryContentManager()

    class Meta:
        # ordering = ['start_at']
        ordering = ['start_at', 'session__start_time']

    def __str__(self):
        return self.name

    @property
    def category(self):
        return self.event.category

    @property
    def place(self):
        return self.session.place

    @property
    def start_time(self):
        return self.session.start_time

    @property
    def poster(self):
        return self.event.poster

    @property
    def description(self):
        return self.event.description

    @property
    def name(self):
        if self.session.postfix_name:
            return "{} [{}]".format(self.event.name, self.session.postfix_name)
        else:
            return self.event.name

    def get_absolute_url(self):
        try:
            return "{}?lightbox=event-{}".format(reverse("events:index"), self.id)
        except NoReverseMatch:
            return "#"

    def poster_thumb_src(self):
        image = self.poster
        if not image:
            return None

        thumbnail_options = {
            'size': (360, 240),
            'crop': False,
            'upscale': True,
            'subject_location': image.subject_location,
        }
        thumbnailer = get_thumbnailer(image)
        return thumbnailer.get_thumbnail(thumbnail_options).url

class UpcomingEventsPlugin(CMSPlugin):

    num_objects = models.PositiveIntegerField("Количество мероприятий", default=3)
    category = models.ForeignKey(CategoryEvent, verbose_name="Категория", 
                                 on_delete=models.SET_NULL, blank=True, null=True)

    def get_objects(self):
        qs = EventEntry.objects.upcoming()
        if self.category:
            qs = qs.filter(event__category=self.category)
        if self.num_objects:
            qs = qs[:self.num_objects]
        return qs

    def generate_id(self):
        return str(uuid.uuid4().fields[-1])[:7]


class CalendarEventsPlugin(CMSPlugin):

    # num_objects = models.PositiveIntegerField("Количество мероприятий", default=3)
    category = models.ForeignKey(CategoryEvent, verbose_name="Категория мероприятий", 
                        on_delete=models.SET_NULL, blank=True, null=True,
                        help_text="Оставьте пустым для использования всех категорий")

    def generate_id(self):
        return str(uuid.uuid4().fields[-1])[:7]
    