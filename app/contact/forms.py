from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import *
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget
from django.urls import reverse_lazy
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
from .models import ContactSettings
from filer.fields.file import FilerFileField
from django.core.validators import FileExtensionValidator
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox
import random

class ContactForm(forms.Form):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # загружаем модель с настройками приложения
        self.settings = ContactSettings.load()

class AgreementForm(ContactForm):
    accept_terms = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            "class": "form-control form-value checkbox"
        })
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_before_form = self.settings.agreement
        self.fields['accept_terms'].label = self.settings.agreement_checkbox_text

class UserDataForm(ContactForm):
    lastname = forms.CharField(label="Фамилия",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Фамилия"
        })
    )
    firstname = forms.CharField(label="Имя",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Имя"
        })
    )
    middlename = forms.CharField(label="Отчество",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Отчество"
        })
    )
    birthday = forms.DateField(label="Дата рождения",
        # widget=forms.DateInput(attrs={
        #     # "class": "form-control",
        #     # "placeholder": "Укажите дату вашего рождения"
        # })
    )
    address = forms.CharField(label="Адрес",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Укажите ваш фактический адрес проживания"
        })
    )
    email = forms.EmailField(label="Электронная почта",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Укажите ваш адрес электронной почты"
        })
    )
    phone = PhoneNumberField(label="Телефон", region="RU")
            # "placeholder": "+7 1112223344"

    agree_pd = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            "class": "form-control form-value checkbox",
        })
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_before_form = self.settings.userdata_form_text
        self.fields['agree_pd'].label = self.settings.userdata_checkbox_text

    # def clean(self):
    #     cleaned_data = super().clean()
    #     # compatibility of earlier and current step


    #     return cleaned_data

# Code Generation and Storage:

#     Upon form submission, generate a random verification code.
#     Store this code temporarily, either in the session or a dedicated model field, associated with the user or the form data.
#     Send the verification code to the user via email or SMS. 

# Verification Form:

#     Create a separate form or include a field in the existing form for the user to enter the verification code. 

# Validation:

#     When the user submits the verification code, retrieve the stored code.
#     Compare the user-provided code with the stored code.
#     If the codes match, proceed with the form processing or user authentication.
#     If the codes do not match, display an error message and prompt the user to re-enter the code.

class VerificationForm(ContactForm):
    verification_code = forms.CharField(max_length=5, label='Код')

    def __init__(self, **kwargs):
        self.stored_code = kwargs.pop("stored_code", None)
        super().__init__(**kwargs)
        self.html_before_form = self.settings.verification_form_text

    def clean_verification_code(self):
        user_code = self.cleaned_data['verification_code']
        if user_code != self.stored_code:
            raise ValidationError('Неверный код.')
        return user_code
    

class MessageForm(ContactForm):
    subject = forms.CharField(
        label="Тема обращения",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Укажите суть обращения"
        })
    )
    message = forms.CharField(
        label="Текст обращения",
        widget=forms.Textarea(attrs={
            "class": "form-control",
        })
    )
    attachment_1 = forms.FileField(required=False, 
                                   widget=forms.ClearableFileInput(attrs={"class": "form-control"}))
    attachment_2 = forms.FileField(required=False, 
                                   widget=forms.ClearableFileInput(attrs={"class": "form-control"}))
    attachment_3 = forms.FileField(required=False, 
                                   widget=forms.ClearableFileInput(attrs={"class": "form-control"}))

    # Капча отключена изза ошибки "timeout-or-duplicate"
    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.html_before_form = self.settings.message_form_text
        # загружаем разрешенные расширения файлов из настроек в валидатор
        validators_list = [FileExtensionValidator(self.settings.valid_extensions)]
        self.fields['attachment_1'].validators = validators_list
        self.fields['attachment_2'].validators = validators_list
        self.fields['attachment_3'].validators = validators_list