from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from .models import Catalog, CatalogItem, Category
from .forms import CatalogItemPluginForm
# from .forms import InfoblockForm

class CategoryInlineAdmin(admin.TabularInline):
    model = Category
    extra = 0
    # prepopulated_fields = {"slug": ("title",)}
    

@plugin_pool.register_plugin
class CatalogPlugin(CMSPluginBase):
    model = Catalog
    module = "Каталог"
    name = "Каталог"
    render_template = "./catalog/base.html"
    cache = True
    inlines = (CategoryInlineAdmin, )
    allow_children = True
    child_classes = ["CatalogItemPlugin"]
    # form = InfoblockForm
    # fieldsets = (
    #     (None, {
    #         'fields': [
    #             'folder',
    #             ('pageThumbWidth',
    #             'pageThumbHeight',
    #             'pageThumbMarginVertical',
    #             'pageThumbMarginHorizontal',),
    #         ]
    #     }),
    #     ('Фоновое изображение (если ширина и высота равны 0 - будет использоваться оригинальный размер)', {
    #         'fields': [
    #             ('background_image',
    #             'thumb_width',
    #             'thumb_height'),
    #         ]
    #     }),
    # )

    def render(self, context, instance, placeholder):
        context.update({
            'id': instance.generate_id(),
            'instance': instance,
        })
        return context


@plugin_pool.register_plugin
class CatalogItemPlugin(CMSPluginBase):
    model = CatalogItem
    module = "Каталог"
    name = "Элемент каталога"
    render_template = "./catalog/item.html"
    parent_classes = ["CatalogPlugin"]
    allow_children = False
    form = CatalogItemPluginForm


    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
        })
        return context
    
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):

        # changing queryset of M2M field
        # i couldnt get access to form get_bound_plugin() method,
        # so used just GET parameter
        # it works well on creating and failing validation of plugin form 
        # For editing existing plugins see __init__ of form in forms.py
        if db_field.name == "categories":
            parent = request.GET.get('plugin_parent', None)
            if parent:
                kwargs["queryset"] = Category.objects.filter(plugin_id=parent)

        return super().formfield_for_manytomany(db_field, request, **kwargs)