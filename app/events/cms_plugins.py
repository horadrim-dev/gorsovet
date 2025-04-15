from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from news.models import Post
from django.db.models.functions import TruncDay

from .models import UpcomingEventsPlugin, Event, CalendarEventsPlugin, EventEntry

@plugin_pool.register_plugin
class UpcomingEventsPluginPublisher(CMSPluginBase):
    model = UpcomingEventsPlugin
    render_template = 'events/plugins/upcoming_events.html'
    name = "Ближайшие мероприятия"
    module = "Мероприятия"

    def render(self, context, instance, placeholder):
        context.update({
            'id': instance.generate_id(),
        })
        context['object_list'] = instance.get_objects()
        return context


@plugin_pool.register_plugin
class CalendarEventsPluginPublisher(CMSPluginBase):
    '''
    Плагин календарь мероприятий.
    При первой загрузке отображает мероприятия в ближайший день.
    При кликах по другим датам - делает ajax запрос в GetEventListView
    и загружает уже отрендеренный контент
    '''

    model = CalendarEventsPlugin
    render_template = 'events/plugins/calendar.html'
    name = "Календарь мероприятий"
    module = "Мероприятия"

    def render(self, context, instance, placeholder):

        # получаем список дат, в которые есть мероприятия
        events_dates_qs = EventEntry.objects.upcoming() 
        if instance.category:
            events_dates_qs = events_dates_qs.filter(event__category=instance.category)
        events_dates_qs = events_dates_qs.values_list('start_at__date') \
                                         .distinct() \
                                         .order_by('start_at__date')

        if events_dates_qs:
            # формируем список мероприятий в ближайший день
            closest_events_qs = EventEntry.objects.upcoming_by_date(events_dates_qs[0][0])
            if instance.category:
                closest_events_qs = closest_events_qs.filter(event__category=instance.category)
            
            closest_events_qs = closest_events_qs.annotate(day=TruncDay('start_at'))
            context['object_list'] = closest_events_qs 
        
        context.update({
            'id': instance.generate_id(),
            'instance': instance,
            'events_dates': [date[0].strftime("%Y-%m-%d") for date in events_dates_qs],
        })
        return context
