from elasticsearch_dsl import DocType, Completion, Keyword, Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer


connections.create_connection(hosts=['localhost'])


class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])


class ElasticType(DocType):
    suggest = Completion(analyzer=ik_analyzer)
    title = Text(analyzer="ik_max_word")
    url = Keyword()
    author = Keyword()
    html_content = Text(analyzer="ik_max_word")

    class Meta:
        index = "ready2search"
        doc_type = "content"


if __name__ == '__main__':
    ElasticType.init()