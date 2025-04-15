from django.contrib import admin
from cms.extensions import PageExtensionAdmin

from .models import MenuItemSettingsExtension

from django.db.utils import ProgrammingError
from .models import SiteSettings, Social
from django.core.exceptions import ImproperlyConfigured
# from cms.admin.pageadmin import PageAdmin
# from cms.models.pagemodel import Page


class SingletonModelAdmin(admin.ModelAdmin):

    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        if not self.model:
            raise ImproperlyConfigured("Не задана модель для Singleton")
        try:
            self.model.load().save()
        except ProgrammingError:
            pass
 
    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False
 
    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False

class MenuItemSettingsExtensionAdmin(PageExtensionAdmin):
    pass

class SocialInline(admin.TabularInline):
    model = Social
    exclude = []
    extra = 0
    # formset = ModuleContentInlineFormSet
    # raw_id_fields = ("content_post", )
    # class Media:
    #     js = ('grid/js/modulecontent_inline.js',)

class SiteSettingsAdmin(SingletonModelAdmin):
    # model = SiteSettings
    inlines = (SocialInline, )
 
 
admin.site.register(MenuItemSettingsExtension, MenuItemSettingsExtensionAdmin)
admin.site.register(SiteSettings, SiteSettingsAdmin)


# class ExtendedPageAdmin(admin.StackedInline):
#     model = ExtendedPage
#     can_delete = False

# PageAdmin.inlines.append(ExtendedPageAdmin)
# try:
#     admin.site.unregister(Page)
# except:
#     pass
# admin.site.register(Page, PageAdmin)