from haystack import indexes
from .models import EventEntry


class SessionEventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', null=True)
    description = indexes.CharField(model_attr='description', null=True)
    place = indexes.CharField(model_attr='place', null=True)
    start_at = indexes.DateTimeField(model_attr='start_at', null=True)

    def get_model(self):
        return EventEntry

    def index_queryset(self, using=None):
        "Used when the entire index for model is updated."
        return self.get_model().objects.upcoming()