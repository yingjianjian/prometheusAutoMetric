from elasticsearch import Elasticsearch

class esApi():
    def __init__(self):
        self.es = Elasticsearch([{'host': 'elasticsearch-logging', 'port': 9200}], timeout=3600)
        self.result = dict()
        self.Value = dict()
        self.esStatus = dict()

    def es_object(self):

        body1 = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                '@timestamp': {'gt': 'now-1m'}
                            }
                        },
                        {
                            "term": {
                                "appname": "watcher"
                            }
                        },
                        {
                            "regexp": {
                                "message.keyword": "数据共享平台,接口响应异常.*"
                            }
                        },
                    ]
                }
            }
        }
        body2 = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                '@timestamp': {'gt': 'now-1m'}
                            }
                        },
                        {
                            "term": {
                                "appname": "watcher"
                            }
                        },
                        {
                            "match": {
                                "message.keyword": "数据共享平台,通过身份证号获取健康码失败"
                            }
                        }
                    ]
                }
            }
        }
        result1=self.es.search(index="isyscore-*",body=body1,size=1000)['hits']['hits']
        result2 = self.es.search(index="isyscore-*", body=body2, size=1000)['hits']['hits']
        result = result1 + result2
        return result





    # def es_status(self):
    #     #    for key,value in self.es.nodes.stats()['nodes'].items():
    #     #        self.Value['es_heap_used_percent'] = value['jvm']['mem']['heap_used_percent']           #75的时候进行GC   节点总是大约75%，那你节点正在承受内存方面的压力，这是一个告警，预示着你不久就会出现慢GC heap使用率一直在85%
    #     #        self.Value['es_heap_used_in_bytes'] = value['jvm']['mem']['heap_used_in_bytes']
    #     #        self.Value['es_young_collection_count'] = value['jvm']['gc']['collectors']['young']['collection_count']
    #     #        self.Value['es_young_collection_millis'] = value['jvm']['gc']['collectors']['young']['collection_time_in_millis']
    #     #        self.Value['es_old_collection_count'] = value['jvm']['gc']['collectors']['old']['collection_count']
    #     #        self.Value['es_old_collection_millis'] = value['jvm']['gc']['collectors']['old']['collection_time_in_millis']
    #     #        self.Value['es_index_total'] = value['indices']['indexing']['index_total']
    #     #        self.Value['index_time_in_millis'] = value['indices']['indexing']['index_time_in_millis']
    #     #        self.result[key] = self.Value
    #     #    return self.result
    #     # def cluster_status(self):
    #     #     esStatus = self.es.cluster.health()
    #     #     self.esStatus['es_status'] = esStatus['status']
    #     #     self.esStatus['es_unassigned_shards'] = esStatus['unassigned_shards']
    #     #     return self.esStatus


