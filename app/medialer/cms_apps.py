from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class MedialerApphook(CMSApp):
    app_name = "medialer"  # must match the application namespace
    name = "Медиа-центр"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["medialer.urls"] # replace this with the path to your application's URLs module