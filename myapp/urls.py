from . import views
from django.urls import path

app_name = 'myapp'

urlpatterns = [
    path("",views.IndexView.as_view(), name="index"),
    path("home",views.HomeView.as_view(), name="home"),
    path("item/<int:item_id>/", views.ItemView.as_view(), name="item"),
    path("search",views.SearchView.as_view(), name="search"),
]