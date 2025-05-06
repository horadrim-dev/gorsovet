from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import AttributesPlugin, LogoPlugin, OtdelOrganizationPlugin, SotrudnikOrganizationPlugin, \
                    ActivityPlugin, Activity, Department, DepartmentPlugin
from .forms import SotrudnikOrganizationPluginForm

@plugin_pool.register_plugin
class AttributesPluginPublisher(CMSPluginBase):
    module = "Структура"
    name = "Атрибуты организации"
    model = AttributesPlugin
    allow_children = False
    render_template = "structure/plugins/attributes_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['object'] = instance.organization
        return context
 
@plugin_pool.register_plugin
class LogoPluginPublisher(CMSPluginBase):
    module = "Структура"
    name = "Логотип организации"
    model = LogoPlugin
    allow_children = False
    render_template = "structure/plugins/logo_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['object'] = instance.organization
        return context


@plugin_pool.register_plugin
class OtdelOrganizationPluginPublisher(CMSPluginBase):
    module = "Структура"
    name = "Отделы организации"
    model = OtdelOrganizationPlugin
    allow_children = False
    render_template = "structure/plugins/otdel_organization_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['object_list'] = instance.organization.get_otdels()
        context['SHOW_DETAIL_LINK'] = instance.show_detail_link
        return context
 
@plugin_pool.register_plugin
class SotrudnikOrganizationPluginPublisher(CMSPluginBase):
    module = "Структура"
    name = "Сотрудники организации"
    model = SotrudnikOrganizationPlugin
    form = SotrudnikOrganizationPluginForm
    allow_children = False
    render_template = "structure/plugins/sotrudnik_organization_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        if instance.apparat:
            qs = instance.organization.sotrudnik_set.filter(apparat=True)
        elif instance.otdel:
            qs = instance.organization.sotrudnik_set.filter(otdel=instance.otdel) 
        else:
            qs = instance.organization.sotrudnik_set.all()

        context['object_list'] = qs
        context['layout'] = instance.layout
        context['SHOW_DETAIL_LINK'] = instance.show_detail_link
        return context
 

# @plugin_pool.register_plugin
class ActivityPluginPublisher(CMSPluginBase):
    module = "Структура"
    name = "Виды спорта"
    model = ActivityPlugin
    allow_children = False
    render_template = "structure/plugins/activity_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['object_list'] = Activity.objects.all()
        return context
    

# @plugin_pool.register_plugin
class DepartmentPluginPublisher(CMSPluginBase):
    module = "Структура"
    name = "Спортивные секции"
    model = DepartmentPlugin
    allow_children = False
    render_template = "structure/plugins/department_plugin.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['object_list'] = instance.get_departments()
        return context