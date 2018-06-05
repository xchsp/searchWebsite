import datetime
from elasticsearch_dsl.connections import connections
from .es_model import ElasticType

es = connections.create_connection(ElasticType._doc_type.using)


def date_convert(value):
    try:
        create_time = str(value)
    except Exception as e:
        create_time = str(datetime.date.today())
    return create_time


def gen_suggest(index, text):
    if text:
        words = es.indices.analyze(index=index,
                                   analyzer='ik_max_word',
                                   params={'filter': ['lowercase']},
                                   body=text)
        analyzed_words = set([r['token'] for r in words['tokens'] if len(r['token']) > 1])
    else:
        return None
    return list(analyzed_words)