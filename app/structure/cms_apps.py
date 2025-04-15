from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class StructureApphook(CMSApp):
    app_name = "structure"  # must match the application namespace
    name = "Структура"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["structure.urls"] # replace this with the path to your application's URLs module
    

@apphook_pool.register
class DepartmentApphook(CMSApp):
    app_name = "department"  # must match the application namespace
    name = "Спортивные секции"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["structure.department_urls"] # replace this with the path to your application's URLs module