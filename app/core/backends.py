from haystack.backends.elasticsearch7_backend import FIELD_MAPPINGS, \
    DEFAULT_FIELD_MAPPING, Elasticsearch7SearchBackend, Elasticsearch7SearchEngine

from haystack.constants import DJANGO_CT, DJANGO_ID
from haystack.backends import elasticsearch7_backend
# https://silentsokolov.github.io/django-haystack-elasticsearch-prombiemy-avtodopolnieniia
from elasticsearch.exceptions import NotFoundError
import haystack

# Hack analyser
elasticsearch7_backend.DEFAULT_FIELD_MAPPING = {'type': 'text', 'analyzer': 'russian'}
# FIELD_MAPPINGS['edge_ngram'] = {'type': 'text', 'index_analyzer': 'edgengram_analyzer', 'search_analyzer': 'standard'}
# FIELD_MAPPINGS['text'] = {'type': 'text', 'analyzer': 'russian'}

class ElasticsearchCustomBackend(Elasticsearch7SearchBackend):
    DEFAULT_SETTINGS = {
        'settings': {
            "analysis": {
                "analyzer": {
                    "russian": {
                        #  добавляем удаление html тегов 
                        "type": "custom",
                        "char_filter": ["html_strip"],
                        "tokenizer":  "whitespace",
                        "filter": [
                            "lowercase",
                            "ru_RU",
                            # "snowball",
                            # "elision"
                            "ru_stopwords",
                        ]
                    },
                    # "ngram_analyzer": {
                    #     "type": "custom",
                    #     "tokenizer": "lowercase",
                    #     "filter": ["haystack_ngram"]
                    # },
                    # "edgengram_analyzer": {
                    #     "type": "custom",
                    #     "tokenizer": "lowercase",
                    #     "filter": ["haystack_edgengram"]
                    # },
                },
                "filter": {
                    'ru_stopwords': {
                        'type': 'stop',
                        'stopwords': u'а,без,более,бы,был,была,были,было,быть,в,вам,вас,весь,во,вот,все,всего,всех,вы,где,да,даже,для,до,его,ее,если,есть,еще,же,за,здесь,и,из,или,им,их,к,как,ко,когда,кто,ли,либо,мне,может,мы,на,надо,наш,не,него,нее,нет,ни,них,но,ну,о,об,однако,он,она,они,оно,от,очень,по,под,при,с,со,так,также,такой,там,те,тем,то,того,тоже,той,только,том,ты,у,уже,хотя,чего,чей,чем,что,чтобы,чье,чья,эта,эти,это,я,a,an,and,are,as,at,be,but,by,for,if,in,into,is,it,no,not,of,on,or,such,that,the,their,then,there,these,they,this,to,was,will,with',
                    },
                    "ru_RU": {
                        "type": "hunspell",
                        "locale": "ru_RU",
                        "dedup": False
                    }
                    # "haystack_ngram": {
                    #     "type": "ngram",
                    #     "min_gram": 3,
                    #     "max_gram": 15
                    # },
                    # "haystack_edgengram": {
                    #     "type": "edge_ngram",
                    #     "min_gram": 2,
                    #     "max_gram": 15
                    # },
                },
                # "tokenizer": {
                #     "haystack_ngram_tokenizer": {
                #         "type": "ngram",
                #         "min_gram": 3,
                #         "max_gram": 15,
                #     },
                #     "haystack_edgengram_tokenizer": {
                #         "type": "edge_ngram",
                #         "min_gram": 2,
                #         "max_gram": 15,
                #         "side": "front"
                #     }
                # },
            }
        }
    }
    # def setup(self):
    #     """
    #     Defers loading until needed.
    #     """
    #     # Get the existing mapping & cache it. We'll compare it
    #     # during the ``update`` & if it doesn't match, we'll put the new
    #     # mapping.
    #     try:
    #         self.existing_mapping = self.conn.indices.get_mapping(index=self.index_name)
    #     except NotFoundError:
    #         pass
    #     except Exception:
    #         if not self.silently_fail:
    #             raise

    #     unified_index = haystack.connections[self.connection_alias].get_unified_index()
    #     self.content_field_name, field_mapping = self.build_schema(unified_index.all_searchfields())
    #     current_mapping = {
    #         'modelresult': {
    #             'properties': field_mapping,
    #             # this option doesnt work with elasticsearch 2.4.6
    #             # '_boost': {
    #             #     'name': 'boost',
    #             #     'null_value': 1.0
    #             # }
    #         }
    #     }

    #     if current_mapping != self.existing_mapping:
    #         try:
    #             # Make sure the index is there first.
    #             self.conn.indices.create(index=self.index_name, body=self.DEFAULT_SETTINGS, ignore=400)
    #             self.conn.indices.put_mapping(index=self.index_name, doc_type='modelresult', body=current_mapping)
    #             self.existing_mapping = current_mapping
    #         except Exception:
    #             if not self.silently_fail:
    #                 raise

    #     self.setup_complete = True

    # def build_schema(self, fields):
    #     content_field_name = ''
    #     mapping = {
    #         # DJANGO_CT: {'type': 'text', 'index': 'not_analyzed', 'include_in_all': False},
    #         # DJANGO_ID: {'type': 'text', 'index': 'not_analyzed', 'include_in_all': False},
    #         # DJANGO_CT: {'type': 'text', 'index': False, 'include_in_all': False},
    #         # DJANGO_ID: {'type': 'text', 'index': False, 'include_in_all': False},
    #         DJANGO_CT: {'type': 'text'},
    #         DJANGO_ID: {'type': 'text'},
    #     }

    #     for field_name, field_class in fields.items():
    #         field_mapping = FIELD_MAPPINGS.get(field_class.field_type, DEFAULT_FIELD_MAPPING).copy()
    #         if field_class.boost != 1.0:
    #             field_mapping['boost'] = field_class.boost

    #         if field_class.document is True:
    #             content_field_name = field_class.index_fieldname

    #         # Do this last to override `text` fields.
    #         if field_mapping['type'] == 'text':
    #             if field_class.indexed is False or hasattr(field_class, 'facet_for'):
    #                 field_mapping['index'] = 'keyword'
    #                 del field_mapping['analyzer']

    #         mapping[field_class.index_fieldname] = field_mapping

    #     return (content_field_name, mapping)


class ElasticsearchCustomSearchEngine(Elasticsearch7SearchEngine):
    backend = ElasticsearchCustomBackend
