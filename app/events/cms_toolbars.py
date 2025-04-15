from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.cms_toolbars import PAGE_MENU_IDENTIFIER
from cms.extensions.toolbar import ExtensionToolbar
from cms.utils.urlutils import admin_reverse
from django.urls import reverse 


@toolbar_pool.register
class EventsToolbar(CMSToolbar):

    # we are getting redirect to model.get_absolute_url instance after save
    # watch_models = [Post]

    def populate(self):


        page_menu = self.toolbar.get_menu(PAGE_MENU_IDENTIFIER)

        menu = self.toolbar.get_or_create_menu(
            key='events_cms_integration',
            verbose_name='Мероприятия',
            position = page_menu
        )
        menu .add_sideframe_item(
            name='Мероприятия',
            url=admin_reverse('events_event_changelist')
        )
        menu .add_sideframe_item(
            name='Категории мероприятий',
            url=admin_reverse('events_categoryevent_changelist')
        )
        # news_menu.add_modal_item(
        #     name='Типы документов',
        #     url=admin_reverse('docs_documenttype_changelist')
        # )

        self.toolbar.add_modal_button(
            name='Мероприятие', 
            url=admin_reverse('events_event_add'),
            )