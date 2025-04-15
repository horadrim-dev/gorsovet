from django.contrib import admin
from core.admin import SingletonModelAdmin
from .models import ContactSettings, Appeal
# Register your models here.

@admin.register(ContactSettings)
class ContactSettingsAdmin(SingletonModelAdmin):
    model = ContactSettings
