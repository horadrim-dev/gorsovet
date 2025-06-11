from cms.menu_bases import CMSAttachMenu
from django.utils.translation import ugettext_lazy as _
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import PostCategory


class NewsMenu(CMSAttachMenu):

  name = _("Меню \"Новости\"")

  def get_nodes(self, request):

    nodes = []
    for obj in PostCategory.objects.all():

        node = NavigationNode(
            obj.name,
            obj.get_absolute_url(),
            obj.pk
        )
        nodes.append(node)

    return nodes

menu_pool.register_menu(NewsMenu)