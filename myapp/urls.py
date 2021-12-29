from . import views
from django.urls import path

app_name = 'myapp'

urlpatterns = [
    path("",views.IndexView.as_view(), name="index"),
    path("home",views.HomeView.as_view(), name="home"),
]