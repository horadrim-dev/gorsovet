from cms.menu_bases import CMSAttachMenu
from django.utils.translation import ugettext_lazy as _
from menus.base import NavigationNode
from menus.menu_pool import menu_pool

from .models import CategoryOrganization


@menu_pool.register_menu
class CategoryOrganizationMenu(CMSAttachMenu):

  name = _("Меню \"Категории организаций\"")

  def get_nodes(self, request):

    nodes = []
    for obj in CategoryOrganization.objects.all():

        node = NavigationNode(
            obj.name,
            obj.get_absolute_url(),
            obj.pk
        )
        nodes.append(node)

    return nodes

# menu_pool.register_menu(CategoryOrganization)