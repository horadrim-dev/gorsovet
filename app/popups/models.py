from django.db import models
from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField

POPUP_POSITION_CHOICES = [
    ('bottom-right', 'Справа внизу'),
    ('top-left', 'Слева вверху'),
    ('top-right', 'Справа вверху'),
    ('bottom-left', 'Слева внизу'),
    ('bottom', 'Внизу во всю ширину'),
    ('top', 'Вверху во всю ширину'),
]
class Popup(CMSPlugin):
    layout = models.CharField("Расположение", choices=POPUP_POSITION_CHOICES,
                                default=POPUP_POSITION_CHOICES[0][0])
    title = models.CharField("Заголовок", max_length=256, blank=True, null=True)
    content = HTMLField("Содержимое")
    use_button = models.BooleanField("Использовать кнопку", default=True)
    button_text = models.CharField("Текст кнопки", max_length=64, default="Хорошо")