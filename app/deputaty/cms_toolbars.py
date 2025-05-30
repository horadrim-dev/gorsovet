from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.cms_toolbars import PAGE_MENU_IDENTIFIER
from cms.extensions.toolbar import ExtensionToolbar
from cms.utils.urlutils import admin_reverse
from django.urls import reverse 


@toolbar_pool.register
class DeputatyToolbar(CMSToolbar):

    # we are getting redirect to model.get_absolute_url instance after save
    # watch_models = [Post]

    def populate(self):

        page_menu = self.toolbar.get_menu(PAGE_MENU_IDENTIFIER)

        deputaty_menu = self.toolbar.get_or_create_menu(
            key='deputaty_cms_integration',
            verbose_name='Депутаты',
            position = page_menu
        )
        deputaty_menu .add_sideframe_item(
            name='Депутаты',
            url=admin_reverse('deputaty_deputat_changelist')
        )
        deputaty_menu.add_modal_item(
            name='Созывы',
            url=admin_reverse('deputaty_sozyv_changelist')
        )

        # self.toolbar.add_modal_button(
        #     name='Документ', 
        #     url=admin_reverse('docs_document_add'),
        #     )