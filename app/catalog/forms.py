from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Catalog, CatalogItem, Category

# class CatalogForm(forms.ModelForm):

#     # create = forms.ChoiceField(
#     #     choices=NUM_COLUMNS,
#     #     label=_("Create Columns"),
#     #     help_text=_("Create this number of columns")
#     # )
#     # create_width = forms.ChoiceField(
#     #     choices=WIDTH_CHOICES,
#     #     label=_("Column width"),
#     #     help_text=_(
#     #         "Width of created columns. You can still change the width of the "
#     #         "column afterwards."
#     #     )
#     # )

#     class Meta:
#         model = Catalog
#         exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')


class CatalogItemPluginForm(forms.ModelForm):

    class Meta:
        model = CatalogItem
        exclude = ()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # changing queryset of M2M field 
        # (it works well for editing existing instances, 
        # for new instances (not saved yet), queryset changed in formfield_for_manytomany in cmsplugins.py)
        # Why here? cause we can get access to parent plugin only here
         #https://docs.django-cms.org/en/latest/how_to/custom_plugins.html#nested-plugins
        if self.instance and self.instance.parent:
            self.fields["categories"].queryset = self.fields["categories"].queryset \
                .filter(
                        plugin=self.instance.parent.get_bound_plugin()
                        )
