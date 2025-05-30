from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class DeputatyApphook(CMSApp):
    app_name = "deputaty"  # must match the application namespace
    name = "Депутаты"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["deputaty.urls"] # replace this with the path to your application's URLs module
    
