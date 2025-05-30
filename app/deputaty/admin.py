from django.contrib import admin

from .models import *

@admin.register(Sozyv)
class SozyvAdmin(admin.ModelAdmin):
    model = Sozyv


@admin.register(Deputat)
class EventAdmin(admin.ModelAdmin):
    model = Deputat
    list_display = ('name',)