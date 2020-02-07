from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views
urlpatterns = [
    # url(r'/metric',views.requests_count.as_view()),
    url(r'/Apimetric',views.ApiResponse.as_view()),
    url(r'/urlRequest',views.urlStatus.as_view())
]