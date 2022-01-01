from . import views
from django.urls import path

app_name = 'myapp'

urlpatterns = [
    path("",views.home, name="index"),
    path("home",views.home, name="home"),
    path("login_list",views.LoginListView.as_view(), name="login_list"),
    path("signup_list",views.SignupListView.as_view(), name="signup_list"),

    path("item/<int:item_id>/", views.ItemView.as_view(), name="item"),
    path("search",views.search, name="search"),
    path("category",views.category, name="category"),

    path("settings",views.SettingsView.as_view(),name="settings"),
    path("change_profile",views.change_profile,name="change_profile"),
]