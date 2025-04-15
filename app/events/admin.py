from django.contrib import admin
from .models import Event, CategoryEvent, SessionEvent
from .forms import SessionEventStackedInlineFormSet

@admin.register(CategoryEvent)
class CategoryEventAdmin(admin.ModelAdmin):
    model = CategoryEvent


class SessionEventStackedInline(admin.StackedInline):
    model = SessionEvent
    extra = 0
    # exclude = ['postfix_name']
    formset = SessionEventStackedInlineFormSet

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('name', 'category',)
    inlines = (SessionEventStackedInline, )