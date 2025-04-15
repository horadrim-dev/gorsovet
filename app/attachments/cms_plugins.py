from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.contrib import admin
from .models import Attachment, Attachments


class AttachmentInlineAdmin(admin.StackedInline):
    model = Attachment
    extra = 2
    exclude = ('extension', "hits")

@plugin_pool.register_plugin
class AttachmentPlugin(CMSPluginBase):
    model = Attachments
    name = "Вложения"
    module = "Документы"
    render_template = "attachments/attachments.html"
    allow_children = False
    inlines = (AttachmentInlineAdmin, )

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance,
            'object_list': instance.attachment_set.all()
            # 'id': instance.generate_id(),
        })
        return context
