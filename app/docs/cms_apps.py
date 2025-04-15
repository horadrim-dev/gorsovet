from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class DocsApphook(CMSApp):
    app_name = "docs"  # must match the application namespace
    name = "Документы"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["docs.urls"] # replace this with the path to your application's URLs module