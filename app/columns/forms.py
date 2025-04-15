from django import forms

from .models import Columns


class ColumnsForm(forms.ModelForm):
    NUM_COLUMNS = (
        # оставлены только варианты на которые делится 12 
        # для облегчения bootstrap верстки
        ("6-6", "2 колонки, ширина 50% - 50%"),
        ("9-3", "2 колонки, ширина 75% - 25%"),
        ("3-9", "2 колонки, ширина 25% - 75%"),

        ("4-4-4", "3 колонки, ширина 33% - 33% -33%"),
        ("6-3-3", "3 колонки, ширина 50% - 25% - 25%"),
        ("3-6-3", "3 колонки, ширина 25% - 50% - 25%"),
        ("3-3-6", "3 колонки, ширина 25% - 25% - 50%"),
    )

    create = forms.ChoiceField(
        choices=NUM_COLUMNS,
        label="Колонки",
        # help_text=_("Create this number of columns")
    )
    # create_width = forms.ChoiceField(
    #     choices=WIDTH_CHOICES,
    #     label=_("Column width"),
    #     help_text=_(
    #         "Width of created columns. You can still change the width of the "
    #         "column afterwards."
    #     )
    # )

    class Meta:
        model = Columns
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
