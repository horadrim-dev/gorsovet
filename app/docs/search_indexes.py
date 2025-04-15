from haystack import indexes
from .models import Document, DocumentCategory


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    subname = indexes.CharField(model_attr='subname', null=True)
    number = indexes.CharField(model_attr='number', null=True)
    date = indexes.DateTimeField(model_attr='date', null=True)

    def get_model(self):
        return Document

class DocumentCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', null=True)

    def get_model(self):
        return DocumentCategory
