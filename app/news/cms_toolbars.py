from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.cms_toolbars import PAGE_MENU_IDENTIFIER
from cms.extensions.toolbar import ExtensionToolbar
from cms.utils.urlutils import admin_reverse
from django.urls import reverse 
from .models import Post
@toolbar_pool.register
class NewsToolbar(CMSToolbar):

    # we are getting redirect to model.get_absolute_url instance after save
    watch_models = [Post]

    def populate(self):


        # self.toolbar.add_sideframe_button(
        #     name='Новости', 
        #     url=admin_reverse('news_post_changelist'),
        #     )

        page_menu = self.toolbar.get_menu(PAGE_MENU_IDENTIFIER)

        news_menu = self.toolbar.get_or_create_menu(
            key='news_cms_integration',
            verbose_name='Новости',
            position = page_menu
        )
        news_menu .add_sideframe_item(
            name='Новости',
            url=admin_reverse('news_post_changelist')
        )
        news_menu.add_modal_item(
            name='Добавить новость',
            url=admin_reverse('news_post_add'), 
            # on_close=reverse('news:index')
        )
        news_menu.add_modal_item(
            name='Категории',
            url=admin_reverse('news_postcategory_changelist')
        )
        news_menu.add_modal_item(
            name='Добавить категорию',
            url=admin_reverse('news_postcategory_add')
        )

        tags_menu = self.toolbar.get_or_create_menu(
            key='taggit_cms_integration',
            verbose_name='Теги',
            position = page_menu
        )
        tags_menu .add_sideframe_item(
            name='Теги',
            url=admin_reverse('taggit_tag_changelist')
        )
        self.toolbar.add_modal_button(
            name='Новость', 
            url=admin_reverse('news_post_add'),
            # on_close=reverse('news:index')
            )
        self.toolbar.add_modal_button(
            name='Тег', 
            url=admin_reverse('taggit_tag_add'),
            )