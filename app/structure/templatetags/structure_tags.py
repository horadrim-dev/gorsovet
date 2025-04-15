from django import template

register = template.Library()

@register.inclusion_tag("structure/includes/structure_level.html")
def render_hierarchy(object_list):
    return {'object_list' : object_list}