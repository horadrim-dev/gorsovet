from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.extensions.toolbar import ExtensionToolbar
from cms.utils.urlutils import admin_reverse
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, HELP_MENU_IDENTIFIER, LANGUAGE_MENU_IDENTIFIER
from django.utils.translation import gettext_lazy as _
from .models import MenuItemSettingsExtension


@toolbar_pool.register
class MenuItemSettingsToolbar(ExtensionToolbar):
    # defines the model for the current toolbar
    model = MenuItemSettingsExtension

    def populate(self):
        # setup the extension toolbar with permissions and sanity checks
        current_page_menu = self._setup_extension_toolbar()

        # if it's all ok
        if current_page_menu:
            # retrieves the instance of the current extension (if any) and the toolbar item URL
            page_extension, url = self.get_page_extension_admin()
            if url:
                # adds a toolbar item in position 0 (at the top of the menu)
                current_page_menu.add_modal_item(_('Настройки пункта меню'), url=url,
                    disabled=not self.toolbar.edit_mode_active, position=0)

@toolbar_pool.register
class CoreToolbarClass(CMSToolbar):
    def populate(self):

        admin_menu = self.toolbar.get_menu(ADMIN_MENU_IDENTIFIER)
        admin_menu.name = "Сайт"

        # removing standart menus "LANGUAGE_MENU" and "HELP_MENU" 
        self.toolbar.last_left_items = []
        # assert False, (dir(self.toolbar),(self.toolbar.toolbars))
        # self.toolbar.get_or_create_menu()