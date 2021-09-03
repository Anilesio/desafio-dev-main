from django.conf.urls import url
from .views import index, result

urlpatterns = [
    url(r'^$',index, name="index" ),
    url(r'^result/(?P<pk>\w+)/$', result, name="result"),

]