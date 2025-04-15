from django.contrib import admin
from .models import *
from .forms import *
from cms.admin.placeholderadmin import PlaceholderAdminMixin

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    form = DocumentCategoryForm
    list_display = ('name', 'order', )
    exclude = []

# @admin.register(DocumentType)
# class DocumentTypeAdmin(admin.ModelAdmin):
#     form = DocumentTypeForm
#     list_display = ('name', 'order', )
    # list_filter = ["organization" ]

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentForm
    list_display = ('short_name', 'number', 'date', 'subname', 'category', )
    list_filter = ["category",]
