import http.client

from elasticsearch import Elasticsearch
from elasticsmapp.utils.embeddings import get_embedding

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
http.client._MAXHEADERS = 10000


def find_similar_documents(sentence, index_name='reddit', size=100):
    embedding_vector = get_embedding(sentence)
    query = {'query': {
        "function_score": {
            "boost_mode": "replace",
            "functions": [
                {
                    "script_score": {
                        "script": {
                            "source": "staysense",
                            "lang": "fast_cosine",
                            "params": {
                                "field": "embedding_vector",
                                "cosine": True,
                                "encoded_vector": embedding_vector
                            }
                        }
                    }
                }
            ]
        }
    },
        "size": size
    }
    return es.search(index=index_name, doc_type='_doc', body=query)
