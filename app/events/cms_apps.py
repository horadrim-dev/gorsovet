from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

@apphook_pool.register
class EventsApphook(CMSApp):
    app_name = "events"  # must match the application namespace
    name = "Мероприятия"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["events.urls"] # replace this with the path to your application's URLs module