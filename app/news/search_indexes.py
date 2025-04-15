from haystack import indexes
from .models import Post, PostCategory
from cms.models.pagemodel import Page
from cms.models.pluginmodel import CMSPlugin


class PostCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', null=True)

    def get_model(self):
        return PostCategory

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    title = indexes.CharField(model_attr='title')
    # pub_date = indexes.DateTimeField(model_attr='publishe', null=True)

    def prepare(self, obj):    
        self.prepared_data = super().prepare(obj)
        plugins = CMSPlugin.objects.filter(placeholder=obj.content)
        text = ''              
        for plugin in plugins: 
            instance, _ = plugin.get_plugin_instance()
            if hasattr(instance, 'search_fields'):
                text += ''.join(getattr(instance, field) for field in instance.search_fields)
        # text += obj.get_meta_description() or u''
        # text += obj.get_title() or u''
        # text += obj.get_meta_keywords() if hasattr(obj, 'get_meta_keywords') and obj.get_meta_keywords() else u''
        self.prepared_data['text'] = text
        return self.prepared_data       

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return Post.objects.published()