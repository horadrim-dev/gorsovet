import django_filters
from django import forms
from .models import Post, PostCategory
from taggit.models import Tag
from taggit.managers import TaggableManager
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

class TagFilter(django_filters.CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, **kwargs)

    

class PostFilterSet(django_filters.FilterSet):

    category = django_filters.filters.ModelChoiceFilter(
        queryset=PostCategory.objects.all(), 
        blank=True,
        empty_label='Все новости',
        widget=forms.RadioSelect(attrs={'class':'hidden autoapply'})
        )
    tags = TagFilter(
        field_name='tags__name',
        widget=LabelWidget(attrs={'class':'tags'})
        )
    start_date = django_filters.filters.DateFilter(field_name='published_at',
        widget= forms.DateInput(attrs={'class': 'form-control autoapply', 'type': 'date'}),
        lookup_expr='gte', label='от')
    end_date = django_filters.filters.DateFilter(field_name='published_at',
        widget= forms.DateInput(attrs={'class': 'form-control autoapply', 'type': 'date'}),
        lookup_expr='lte', label='до')
    # tags = django_filters.filters.ModelMultipleChoiceField(
    #     blank=True,
    #     # empty_label='Все новости',
    #     name='tags__name',
    #     to_field_name='name',
    #     conjoined=True,
    #     distinct=True,
    #     queryset=Tag.objects.all(), 
    #     widget=forms.CheckboxSelectMultiple(attrs={'class':''})
    #     )
    # season = django_filters.filters.ChoiceFilter(
    #     choices=SEASON_CHOICES, 
    #     empty_label='<i class="bi bi-funnel"></i>',
    #     widget=forms.RadioSelect(attrs={'class':'btn-check'})
    #     )

    # def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
    #     super().__init__(data, queryset, request=request, prefix=prefix)
    #     self.form.initial['work_in_summer'] =True

    class Meta:
        model = Post
        # fields = ['category', 'tags']
        # исключаем автоматическую генерацию фильтров для этих полей, заданы вручную в теле класса
        exclude = ['category', 'tags', 'start_date', 'end_date']
        
        # filter_overrides = {
        #     TaggableManager: {
        #         'filter_class': django_filters.ModelChoiceFilter, 
        #         # 'extra': lambda f: {
        #         #     'queryset': remote_model(f)._default_manager.complex_filter(
        #         #         remote_field(f).limit_choices_to),
        #         # }
        #     },
        # }