from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.cms_toolbars import PAGE_MENU_IDENTIFIER
from cms.extensions.toolbar import ExtensionToolbar
from cms.utils.urlutils import admin_reverse
from django.urls import reverse 


@toolbar_pool.register
class DocsToolbar(CMSToolbar):

    # we are getting redirect to model.get_absolute_url instance after save
    # watch_models = [Post]

    def populate(self):


        # self.toolbar.add_sideframe_button(
        #     name='Новости', 
        #     url=admin_reverse('news_post_changelist'),
        #     )

        page_menu = self.toolbar.get_menu(PAGE_MENU_IDENTIFIER)

        news_menu = self.toolbar.get_or_create_menu(
            key='docs_cms_integration',
            verbose_name='Документы',
            position = page_menu
        )
        news_menu .add_sideframe_item(
            name='Документы',
            url=admin_reverse('docs_document_changelist')
        )
        news_menu.add_modal_item(
            name='Категории',
            url=admin_reverse('docs_documentcategory_changelist')
        )
        # news_menu.add_modal_item(
        #     name='Типы документов',
        #     url=admin_reverse('docs_documenttype_changelist')
        # )

        self.toolbar.add_modal_button(
            name='Документ', 
            url=admin_reverse('docs_document_add'),
            )