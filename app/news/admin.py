from django.contrib import admin
from .models import *
from .forms import PostForm, PostCategoryForm
from cms.admin.placeholderadmin import PlaceholderAdminMixin


class PhotoPostInline(admin.TabularInline):
    model = PhotoPost
    exclude = ['created_at', 'updated_at']
    extra = 3

class VideoPostInline(admin.TabularInline):
    model = VideoPost
    exclude = ['created_at', 'updated_at']
    extra = 1

@admin.register(Post)
class PostAdmin( PlaceholderAdminMixin, admin.ModelAdmin):
    # поле alias будет автоматически заполнено на основе заголовка
    # prepopulated_fields = {
    #     "alias" : ("title",)
    # 
    form = PostForm
    inlines = (PhotoPostInline, VideoPostInline)
    exclude = [ 'alias']

@admin.register(PostCategory)
class PostCategoryAdmin( PlaceholderAdminMixin, admin.ModelAdmin):
    form = PostCategoryForm