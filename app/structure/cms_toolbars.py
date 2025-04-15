from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.cms_toolbars import PAGE_MENU_IDENTIFIER
from cms.extensions.toolbar import ExtensionToolbar
from cms.utils.urlutils import admin_reverse
from django.urls import reverse 


@toolbar_pool.register
class StructureToolbar(CMSToolbar):

    # we are getting redirect to model.get_absolute_url instance after save
    # watch_models = [Post]

    def populate(self):



        page_menu = self.toolbar.get_menu(PAGE_MENU_IDENTIFIER)

        menu = self.toolbar.get_or_create_menu(
            key='structure_cms_integration',
            verbose_name='Структура',
            position = page_menu
        )
        menu.add_sideframe_item(
            name='Виды организаций',
            url=admin_reverse('structure_categoryorganization_changelist')
        )
        menu.add_sideframe_item(
            name='Организации',
            url=admin_reverse('structure_organization_changelist')
        )
        menu.add_sideframe_item(
            name='Виды спорта',
            url=admin_reverse('structure_activity_changelist')
        )
        menu.add_sideframe_item(
            name='Секции',
            url=admin_reverse('structure_department_changelist')
        )
        menu.add_sideframe_item(
            name='Отделы',
            url=admin_reverse('structure_otdel_changelist')
        )
        menu.add_sideframe_item(
            name='Сотрудники',
            url=admin_reverse('structure_sotrudnik_changelist')
        )

        # self.toolbar.add_modal_button(
        #     name='Документ', 
        #     url=admin_reverse('docs_document_add'),
        #     )