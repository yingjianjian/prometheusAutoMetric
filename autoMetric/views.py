from django.shortcuts import render
import prometheus_client
from prometheus_client import Counter,Gauge
from prometheus_client.core import CollectorRegistry
from django.views.generic import View
from django.http import HttpResponse
import random
from .util import esApi

# requests_total=Counter("request_count", "Total request count of the host") # 数值只增
# class requests_count(View):
#     def get(self,request):
#         requests_total.inc(1)
#         return HttpResponse(prometheus_client.generate_latest(requests_total),content_type="text/plain")

REGISTRY = CollectorRegistry(auto_describe=False)
esStatus = Gauge("elasticsearch", "elasticsearch status is:", ["node", "class"],
                 registry=REGISTRY)  # 数值可大可小
# manageStatus = Gauge("manage_api_21","Api response stats is:",registry=REGISTRY)
# random_value = Gauge("random_value","Random value of the request",registry=REGISTRY)
# c = Counter("request_total","HTTP requests total",["method","clientip"],registry=REGISTRY)
# g = Gauge('my_inprogress_requests','Description of gauge',['mylabelname'],registry=REGISTRY)



class ApiResponse(View):
    def get(self,request):
        es_obj = esApi.esApi()
        es_result = es_obj.es_status()
        for node, values in es_result.items():
            for key,value in values.items():
                esStatus.labels(node,key).set(value)
        # c.labels('get', '127.0.0.1').inc()
        # c.labels('post', '127.0.0.1').inc(3)
        # c.labels(method='get', clientip="192.168.0.1").inc()
        # g.labels(mylabelname='str').set(3.6)
        return HttpResponse(prometheus_client.generate_latest(REGISTRY),content_type="text/plain")

# Create your views here.
