from django.db import models
from core.models import SingletonModel
from djangocms_text_ckeditor.fields import HTMLField
import datetime
# Create your models here.

class ContactSettings(SingletonModel):
    # site_url = models.URLField(verbose_name=_('Website url'), max_length=256)
    agreement_title = models.CharField("Название этапа ознакомления с соглашением", max_length=256,
        default="Прочитайте правила пользования виртуальной приемной")
    agreement = HTMLField("Соглашение", configuration='CKEDITOR_SETTINGS_POST', default="")
    # agreement_checkbox_text = models.CharField("Текст галочки на форме соглашения", max_length=256,
        # default="Я прочитал(а) правила пользования виртуальной приемной")
    agreement_checkbox_text = HTMLField("Текст галочки на форме соглашения", configuration='CKEDITOR_SETTINGS_POST', 
                                       default="Я прочитал(а) правила пользования виртуальной приемной")
    userdata_title = models.CharField("Название этапа ввода пользовательских данных", max_length=256,
        default="Укажите данные о себе")
    # recipient_list не работает по невыясненным причинам, поэтому поле удалено
    # recipient_emails = models.EmailField(verbose_name='Email адреса', blank=True, null=True,
    #                                  help_text="Через запятую! На эти адреса будут приходить обращения из виртуальной приемной")
    userdata_form_text = HTMLField("Текст на форме данных пользователя", configuration='CKEDITOR_SETTINGS_POST', default="")
    userdata_checkbox_text = HTMLField("Текст галочки на форме данных пользователя", configuration='CKEDITOR_SETTINGS_POST', 
                                       default="Я соглашаюсь на обработку моих персональных данных")
    # userdata_checkbox_text = models.CharField("Текст галочки на форме данных пользователя", max_length=256,
    #     default="Я соглашаюсь на обработку моих персональных данных")
    message_title = models.CharField("Название этапа заполнения обращение", max_length=256,
        default="Заполните и отправьте обращение")
    message_form_text = HTMLField("Текст на форме заполнения обращения ", configuration='CKEDITOR_SETTINGS_POST', default="")

    success_text = HTMLField("Текст после успешной отправки обращения ", default="")

    valid_file_extensions = models.CharField("Разрешенные форматы файлов (через запятую)", max_length=512,
                                             default="pdf, txt, doc, docx, xls, xlsx, ppt, pptx, odt, ods, odp, jpg, png, gif, tiff, zip")

    @property
    def valid_extensions(self):
        return self.valid_file_extensions.replace(" ", "").split(',')

    # recipient_list не работает по невыясненным причинам, поэтому свойство удалено
    # @property
    # def recipient_list(self):
    #     if self.recipient_emails:
    #         return self.recipient_emails.replace(" ", "").split(',')
    #     else:
    #         return []

    def __str__(self):
        return 'Конфигурация виртуальной приемной'

    class Meta:
        verbose_name = "Конфигурация виртуальной приемной"
        verbose_name_plural = "Конфигурация виртуальной приемной"

    

class Appeal(models.Model):

    subject = models.TextField("Тема обращения", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Принято решение не хранить персональные данные в БД, поэтому эти полей тут нет
    # LASTNAME
    # MIDDLENAME
    # FIRSTNAME
    # PHONE
    # EMAIL
    # text = models.TextField("Текст обращения", blank=True, null=True)

    @property
    def register_id(self):
        return "{}{}".format(self.created_at.strftime('%y%m%d'), str(self.id))

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "обращения"