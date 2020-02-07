from django.shortcuts import render
import prometheus_client
from prometheus_client import Counter,Gauge
from prometheus_client.core import CollectorRegistry
from django.views.generic import View
from django.http import HttpResponse
import random
from .util import esApi,urlRequest

REGISTRY = CollectorRegistry(auto_describe=False)
esStatus = Gauge("elasticsearch", "elasticsearch status is:", ["node", "class"],
                 registry=REGISTRY)  # 数值可大可小


REGISTRY_URL = CollectorRegistry(auto_describe=False)
urlCollector = Counter("watcherStatus","watcher Url status",["status","code","url"],registry=REGISTRY_URL)
class ApiResponse(View):
    def get(self,request):
        es_obj = esApi.esApi()
        es_result = es_obj.es_status()
        for node, values in es_result.items():
            for key,value in values.items():
                esStatus.labels(node,key).set(value)
        return HttpResponse(prometheus_client.generate_latest(REGISTRY),content_type="text/plain")
class urlStatus(View):
    def get(self,request):
        urlObj = 'http://111.0.120.180:38080/iscias/project/page/2019ncov'
        code = urlRequest.isciasStatus(urlObj)
        if code >= 400 and code <=599:
            status = "failed"
            urlCollector.labels(status, code,urlObj).inc()
        else:
            status = "success"
            urlCollector.labels(status,code,urlObj).inc()
        return HttpResponse(prometheus_client.generate_latest(REGISTRY_URL),content_type="text/plain")
# Create your views here.
