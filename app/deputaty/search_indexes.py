from haystack import indexes
from .models import Deputat


class DeputatIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.NgramField(model_attr='description', null=True)

    def get_model(self):
        return Deputat
