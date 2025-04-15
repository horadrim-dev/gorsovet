from django.utils.translation import gettext_lazy as _

from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import ColumnsForm
from .models import Column, Columns

@plugin_pool.register_plugin
class ColumnsPlugin(CMSPluginBase):
    model = Columns
    module = "Контейнеры"
    name = "Колонки"
    render_template = "columns/columns.html"
    allow_children = True
    child_classes = ["ColumnPlugin"]
    form = ColumnsForm

    def save_model(self, request, obj, form, change):
        response = super().save_model(
            request, obj, form, change
        )
        child_objects = CMSPlugin.objects.filter(parent=obj, plugin_type=ColumnPlugin.__name__)
        for idx, col in enumerate(form.cleaned_data['create'].split('-')):
            bootstrap_col = "col-md-{}".format(col)

            if len(child_objects) >= idx + 1:
                column_obj = Column.objects.get(id=child_objects[idx].id)
                column_obj.classes = bootstrap_col
                column_obj.save()
            else:
                col = Column(
                    parent=obj,
                    placeholder=obj.placeholder,
                    language=obj.language,
                    # width=form.cleaned_data['create_width'],
                    classes=bootstrap_col,
                    position=CMSPlugin.objects.filter(parent=obj).count(),
                    plugin_type=ColumnPlugin.__name__
                )
                col.save()
        return response


@plugin_pool.register_plugin
class ColumnPlugin(CMSPluginBase):
    model = Column
    module = "Колонки"
    name = "Колонка"
    render_template = "columns/column.html"
    parent_classes = ["ColumnsPlugin"]
    allow_children = True


