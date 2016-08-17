from django.conf.urls import include, url
from main import views


urlpatterns = [
    url(r'^$', views.home),

]