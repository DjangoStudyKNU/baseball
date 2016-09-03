from django.conf.urls import url
from amateur import views

urlpatterns = [

    url(r'^$', views.index, name='index'),

]
