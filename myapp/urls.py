from os import name
from . import views
from django.urls import path

app_name = 'myapp'

urlpatterns = [
    path("",views.home, name="home"),
    path("home",views.home, name="home"),
    path("login_list",views.LoginListView.as_view(), name="login_list"),
    path("signup_list",views.SignupListView.as_view(), name="signup_list"),

    path("item/<int:item_id>/", views.ItemView.as_view(), name="item"),
    path("purchase/<int:item_id>/", views.PurchaseView.as_view(), name="purchase"),
    path("seller_profile/<int:seller_id>/", views.SellerProfileView.as_view(), name="seller_profile"),
    path("search",views.search, name="search"),
    path("category",views.category, name="category"),

    path("sell",views.sell, name="sell"),

    path("settings",views.SettingsView.as_view(),name="settings"),
    path("change_profile",views.change_profile,name="change_profile"),

    path("mypage/listings/<str:status>",views.ListingsView.as_view(), name="mypage/listings"),
    path("mypage/purchases/<str:status>",views.PurchasesView.as_view(), name="mypage/purchases"),
    path("talk_room/<int:user_id>/<int:item_id>/",views.talk_room,name="talk_room"),

    path("nortify",views.NortifyView.as_view(),name="nortify")

]