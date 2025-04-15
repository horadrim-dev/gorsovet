from haystack import indexes
from .models import Attachment


class AttachmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', null=True)

    def get_model(self):
        return Attachment