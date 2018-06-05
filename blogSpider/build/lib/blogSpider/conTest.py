from elasticsearch_dsl.connections import connections
from es_model import ElasticType

es = connections.create_connection(ElasticType._doc_type.using)
used_words = set()
words = es.indices.analyze(index=ElasticType._doc_type.index,
                           analyzer='ik_max_word',
                           params={'filter': ['lowercase']},
                           body="我真的需要第三方安全审计吗？ - FreeBuf互联网安全新媒体平台 | 关注黑客与极客")
anylyzed_words = set([r['token'] for r in words['tokens'] if len(r['token']) > 1])
