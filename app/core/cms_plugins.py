from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.template import Template
from .models import HeaderPlugin, WhitespacePlugin, SubmenuPlugin, PureCodePlugin, \
                    TabsPlugin, TabPlugin, AccordionPlugin, ItemAccordionPlugin, \
                    ItemArticlePlugin

@plugin_pool.register_plugin
class HeaderPluginPublisher(CMSPluginBase):
    module = "Общий"
    name = "Заголовок"
    model = HeaderPlugin
    allow_children = False
    render_template = "core/plugins/header.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['title'] = instance.title
        context['subtitle'] = instance.subtitle
        context['layout'] = instance.layout
        context['align'] = instance.align
        return context

@plugin_pool.register_plugin
class WhitespacePluginPublisher(CMSPluginBase):
    module = "Общий"
    name = "Пустое место"
    model = WhitespacePlugin
    allow_children = False
    render_template = "core/plugins/whitespace.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['size'] = instance.size
        return context
    
@plugin_pool.register_plugin
class SubmenuPluginPublisher(CMSPluginBase):
    module = "Меню"
    name = "Дочернее меню"
    model = SubmenuPlugin
    allow_children = False
    render_template = "core/plugins/submenu.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['layout'] = instance.layout
        context['parent_page'] = instance.parent_page
        return context


@plugin_pool.register_plugin
class BlockPluginPublisher(CMSPluginBase):
    module = "Контейнеры"
    name = "Блок"
    allow_children = True
    render_template = "core/plugins/block.html"


@plugin_pool.register_plugin
class PureCodePluginPublisher(CMSPluginBase):
    module = "Общий"
    name = "Код"
    model = PureCodePlugin
    allow_children = False
    render_template = "core/plugins/purecode.html"

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['code'] = instance.code
        context['css'] = instance.css
        context['js'] = instance.js
        return context

@plugin_pool.register_plugin
class TabPluginPublisher(CMSPluginBase):
    model = TabPlugin
    module = "Общий"
    name = "Вкладка"
    render_template = "core/plugins/tab.html"
    parent_classes = ["TabsPluginPublisher"]
    allow_children = True


@plugin_pool.register_plugin
class TabsPluginPublisher(CMSPluginBase):
    module = "Контейнеры"
    name = "Вкладки"
    model = TabsPlugin
    allow_children = True
    child_classes = ["TabPluginPublisher"]
    render_template = "core/plugins/tabs.html"


@plugin_pool.register_plugin
class ItemAccordionPluginPublisher(CMSPluginBase):
    model = ItemAccordionPlugin
    module = "Общий"
    name = "Элемент аккордеона"
    render_template = "core/plugins/accordion_item.html"
    parent_classes = ["AccordionPluginPublisher"]
    allow_children = True


@plugin_pool.register_plugin
class AccordionPluginPublisher(CMSPluginBase):
    module = "Контейнеры"
    name = "Аккордеон"
    model = AccordionPlugin
    allow_children = True
    child_classes = ["ItemAccordionPluginPublisher"]
    render_template = "core/plugins/accordion.html"

@plugin_pool.register_plugin
class ItemArticlePluginPublisher(CMSPluginBase):
    model = ItemArticlePlugin
    module = "Общий"
    name = "Раздел"
    render_template = "core/plugins/article_item.html"
    parent_classes = ["ArticlePluginPublisher"]
    allow_children = True


@plugin_pool.register_plugin
class ArticlePluginPublisher(CMSPluginBase):
    module = "Общий"
    name = "Статья"
    # model = ArticlePlugin
    allow_children = True
    child_classes = ["ItemArticlePluginPublisher"]
    render_template = "core/plugins/article.html"