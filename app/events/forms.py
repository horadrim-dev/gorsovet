from django import forms
from .models import Event


class  SessionEventStackedInlineFormSet(forms.BaseInlineFormSet):

    def clean(self):
        """Проверка того, что хотя бы один день мероприятия добавлен."""

        super().clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('Необходимо добавить хотя бы один день мероприятия')


# class EventForm(forms.ModelForm):

#     class Meta:
#         model = Event
#         # fields = []
#         # exclude = ["extension"]

#     def clean(self):
#         cleaned_data = super().clean()
#         doc_file = cleaned_data.get("document_file")
#         doc_url = cleaned_data.get("document_url")

#         # try:
#         #     post = Post.objects.get(alias=slug)
#         # except Post.DoesNotExist:
#         #     post = None

#         if doc_file and doc_url:
#             msg = "Поля \"Файл документа\" и \"Ссылка на документ\" не должны быть заполнены одновременно."
#             self.add_error("document_url", msg)
#         if not doc_file and not doc_url:
#             msg = "Загрузите файл документа или введите ссылку на него."
#             self.add_error("document_file", msg)


# class DocumentsPluginForm(forms.ModelForm):

#     # tags = TagField(required=False, widget=LabelWidget)

#     class Meta:
#         model = DocumentsPlugin
#         # fields = []
#         exclude = []
