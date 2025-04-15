from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class NewsApphook(CMSApp):
    app_name = "news"  # must match the application namespace
    name = "Новости"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["news.urls"] # replace this with the path to your application's URLs module