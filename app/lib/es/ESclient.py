import typing

from elasticsearch import Elasticsearch


class ESClient:
    es_client: Elasticsearch

    def __init__(self, index: str = 'riester'):
        self.es_client = Elasticsearch("http://elasticsearch:9200")
        self.index = index

    def queryDocument(self):
        try:
            return self.es_client.search(index=self.index, query= {"match_all": {}}, size=10000)
        except Exception as e:
            print(e.message)

    def updateDocument(self, _id: str, doc: dict[str, typing.Any]):
        try:
            self.es_client.update(index=self.index, id=_id, body={"doc": doc})
        except Exception as e:
            print(e.message)
