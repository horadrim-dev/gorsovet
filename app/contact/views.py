from typing import Any, List
from django.db import models
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404, FileResponse
from django.views.generic import ListView, DetailView, View, TemplateView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from formtools.wizard.views import CookieWizardView, SessionWizardView
from .forms import AgreementForm, UserDataForm, VerificationForm, MessageForm
from .models import ContactSettings, Appeal
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, select_template
import random 

def generate_verification_code():
    return ''.join(random.choices('0123456789', k=5))


FORM_TEMPLATES = {0: 'contact/form_agreement.html',
                  1: 'contact/form_userdata.html',
                  2: 'contact/form_verification.html',
                  3: 'contact/form_message.html'}
class ContactWizard(SessionWizardView):

    form_list = [AgreementForm, UserDataForm, VerificationForm, MessageForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
    subject_template = "contact/email/email_subject.html"
    email_template = "contact/email/email_body.html"
    verification_subject_template = "contact/email/verification_email_subject.html"
    verification_email_template = "contact/email/verification_email_body.html"
    # использовал разные шаблоны для разных форм get_templates_names()
    # template_name = 'contact/form.html'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # загружаем модель с настройками приложения
        self.settings = ContactSettings.load()
        # генерируем код подтверждения
        # self.stored_code = generate_verification_code()
        # self.request['stored_code'] = generate_verification_code()

    def get_template_names(self):
        return [FORM_TEMPLATES[int(self.steps.current)]]


    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context.update({
            'STEP_TITLES': [self.settings.agreement_title,
                            self.settings.userdata_title,
                            self.settings.verification_form_title,
                            self.settings.message_title],
        })
        return context 
    
    def dispatch(self, request, *args, **kwargs):

        stored_code = request.session.get('stored_code')
        if not stored_code:
            request.session['stored_code'] = generate_verification_code()

        return super().dispatch(request, *args, **kwargs)
        
    def get_form_kwargs(self, step):
        kwargs = {}
        if step == '2': # verification 
            kwargs['stored_code'] = self.request.session.get('stored_code')
        return kwargs
    

    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)
        if step is None:
            step = self.steps.current
        if step == '2': # verification
            # email = self.get_cleaned_data_for_step('1')['email']
            # form.fields['stored_code'] = self.stored_code
            # form.fields['first_form_field'].label = data1

            # SEND VERIFICATION EMAIL
            data = {
                "stored_code" : self.request.session.get('stored_code')
            }
            self.send_email(
                subject_template=self.subject_template,
                email_template=self.email_template,
                cleaned_data=data,
            )
        return form


    def send_email(self, subject_template, email_template, cleaned_data, attachments=None):
        '''Функция рендерит данные в шаблон и отправляет email'''

        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')
        # recipient_list не работает по невыясненным причинам, поэтому адреса из 
        # конфигурации удалены. Список получателей указывается на хостинге в 
        # поле "Слать копии писем на адреса"
        recipient_list = getattr(settings, 'RECIPIENTS_EMAIL') # + self.settings.recipient_list

        content_subtype = 'html' # 'plain'

        email_message = EmailMessage(
            subject=render_to_string(subject_template, {
                    'data': cleaned_data,
            }).splitlines()[0],
            body=render_to_string(email_template, {
                'data': cleaned_data,
                'from_email': from_email,
            }),
            from_email=from_email,
            to=recipient_list,
            # headers={'Reply-To': form.cleaned_data['email']},
        )

        if attachments:
            for uploaded_file in attachments:
                if uploaded_file:
                    email_message.attach(uploaded_file.name, 
                                        uploaded_file.read(), 
                                        uploaded_file.content_type)
        email_message.content_subtype = content_subtype
        email_message.send(fail_silently=False)

    def done(self, form_list, **kwargs):
        '''
        Функция вызывается когда все формы успешно отработали
        Собираем очищенные данные всех форм, регистрируем обращение и
        отправляем по электронной почте.
        '''
        agreement_form_data = form_list[0].cleaned_data
        userdata_form_data = form_list[1].cleaned_data
        message_form_data = form_list[3].cleaned_data
        # аккумулируем данные, одинаковых полей нет, значит ничего не потеряем
        data = {**agreement_form_data, **userdata_form_data, **message_form_data}

        # создаем объект обращения и получаем его номер регистрации
        appeal = Appeal(subject=data['subject'])
        appeal.save()
        data.update({'register_id': appeal.register_id})

        # формируем список вложений для дальнейшей отправки по email
        attachments = [data['attachment_1'],
                       data['attachment_2'],
                       data['attachment_3']]

        # отправляем email
        self.send_email(
            subject_template=self.subject_template,
            email_template=self.email_template,
            cleaned_data=data,
            attachments=attachments
        )
        # рендерим страницу успешной регистрации обращения
        return render(self.request, 'contact/success.html', {
            'data': data,
            'SUCCESS_TEXT': self.settings.success_text,
        })
