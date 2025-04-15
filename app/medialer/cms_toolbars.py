from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, PAGE_MENU_IDENTIFIER
from cms.extensions.toolbar import ExtensionToolbar
from cms.utils.urlutils import admin_reverse
from django.urls import reverse 


@toolbar_pool.register
class MedialerToolbar(CMSToolbar):

    def populate(self):


        page_menu = self.toolbar.get_menu(PAGE_MENU_IDENTIFIER)
        media_menu = self.toolbar.get_or_create_menu(
            key='medialer_cms_integration',
            verbose_name='Медиа', 
            position=page_menu
        )
        media_menu .add_sideframe_item(
            name='Альбомы',
            url=admin_reverse('medialer_album_changelist')
        )
        self.toolbar.add_modal_button(
            name='Фото в галерею', 
            url=admin_reverse('medialer_albumpicture_add'),
            # on_close=reverse('news:index')
            )