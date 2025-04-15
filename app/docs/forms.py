from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget
from django.urls import reverse_lazy
from phonenumber_field.formfields import PhoneNumberField

class DocumentCategoryForm(forms.ModelForm):

    class Meta:
        model = DocumentCategory
        # fields = []
        exclude = []

# class DocumentTypeForm(forms.ModelForm):
#     class Meta:
#         model = DocumentType
#         # fields = []
#         exclude = []

class DocumentForm(forms.ModelForm):

    tags = TagField(required=False, widget=LabelWidget)

    class Meta:
        model = Document
        # fields = []
        exclude = ["extension"]

    def clean(self):
        cleaned_data = super().clean()
        doc_file = cleaned_data.get("document_file")
        doc_url = cleaned_data.get("document_url")

        # try:
        #     post = Post.objects.get(alias=slug)
        # except Post.DoesNotExist:
        #     post = None

        if doc_file and doc_url:
            msg = "Поля \"Файл документа\" и \"Ссылка на документ\" не должны быть заполнены одновременно."
            self.add_error("document_url", msg)
        if not doc_file and not doc_url:
            msg = "Загрузите файл документа или введите ссылку на него."
            self.add_error("document_file", msg)


# class DocumentsPluginForm(forms.ModelForm):

#     # tags = TagField(required=False, widget=LabelWidget)

#     class Meta:
#         model = DocumentsPlugin
#         # fields = []
#         exclude = []
