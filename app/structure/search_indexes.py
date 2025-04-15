from haystack import indexes
from .models import Organization, Activity, Department, Otdel



class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', null=True)
    short_name = indexes.CharField(model_attr='short_name', null=True)

    def get_model(self):
        return Organization


class ActivityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', null=True)

    def get_model(self):
        return Activity

class DepartmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', null=True)

    def get_model(self):
        return Department
