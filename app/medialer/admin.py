from django.contrib import admin
from .models import *
from .forms import *
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from .cms_plugins import PicturePlugin

@admin.register(AlbumPicture)
class AlbumPictureAdmin(admin.ModelAdmin):
    # поле alias будет автоматически заполнено на основе заголовка
    # prepopulated_fields = {
    #     "alias" : ("title",)
    # 
    form = AlbumPictureForm
    exclude = []
    fieldsets =  [(None, {'fields': ('album',)}) ] + PicturePlugin.fieldsets

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    form = AlbumForm
    exclude = []
    # fieldsets =  [(None, {'fields': ('album',)}) ] + PicturePlugin.fieldsets

# @admin.register(Category)
# class PostAdmin( PlaceholderAdminMixin, admin.ModelAdmin):
#     form = CategoryForm