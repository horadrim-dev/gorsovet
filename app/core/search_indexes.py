from django.utils import timezone
from haystack import indexes
from cms.models.managers import PageManager
from cms.models import Page
from cms.models.pluginmodel import CMSPlugin
from taggit.models import Tag
# from .models import ExtendedPage


class PageIndex(indexes.SearchIndex, indexes.Indexable):
    # https://james.lin.net.nz/2013/11/06/django-cms-haystack-2-0-search-index/
    text = indexes.CharField(document=True, use_template=False)
    # pub_date = indexes.DateTimeField(model_attr='publication_date', null=True)
    # login_required = indexes.BooleanField(model_attr='login_required')
    # url = indexes.CharField(model_attr='get_absolute_url')
    # title = indexes.CharField(model_attr='get_title')
    # menu_title = indexes.CharField(model_attr='get_menu_title')

    def prepare(self, obj):    
        self.prepared_data = super(PageIndex, self).prepare(obj)
        plugins = CMSPlugin.objects.filter(placeholder__in=obj.placeholders.all())
        text = ''              
        for plugin in plugins: 
            instance, _ = plugin.get_plugin_instance()
            if hasattr(instance, 'search_fields'):
                text += ''.join(getattr(instance, field) for field in instance.search_fields)
        text += " ".join([
            obj.get_title() or u'',
            obj.get_menu_title() or u'',
            obj.get_meta_description() or u'',
            obj.get_meta_keywords() if hasattr(obj, 'get_meta_keywords') and obj.get_meta_keywords() else u''
        ])
        self.prepared_data['text'] = text
        return self.prepared_data       

    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        return Page.objects.published().filter(publisher_is_draft=False).distinct()


# class TagIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=False)
#     name = indexes.CharField(model_attr='name')
#     slug = indexes.CharField(model_attr='slug')


# class ExtendedPageIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True, model_attr='text')
#     title = indexes.CharField(model_attr='page.get_page_title')
#     get_slug = indexes.CharField(model_attr='page.get_slug')

#     def prepare_text(self,obj):
#         renderedplugins = ""
#         for i in obj.page.cmsplugin_set.all():
#             renderedplugins += i.render_plugin(context={})
#         return renderedplugins

#     def index_queryset(self, using=None):
#         # assert False, dir(ExtendedPage.page)
#         return ExtendedPage.objects.filter(page__publication_date__lte=timezone.now())

#     def get_model(self):
#         return ExtendedPage

# site.register(Page, PageIndex)
