from django.contrib.auth import get_user_model
from django.http import request
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import generic
from django .views.generic import View

from . models import Item,Category,Quality,Sort
from .forms import UserForm,SellForm



User = get_user_model()

# 最初の画面
class IndexView(generic.TemplateView):
    template_name = "myapp/index.html"

# ログイン選択画面
class LoginListView(generic.TemplateView):
    template_name = "myapp/login_list.html"

# 会員登録選択画面
class SignupListView(generic.TemplateView):
    template_name = "myapp/signup_list.html"

#ホーム画面
def home(request):
    items = Item.objects.filter(is_purchased=False).order_by("-sell_time")
    if request.user.is_authenticated:
        user = request.user
        items = (
            items.exclude(seller=user)
        )

    if request.method == 'GET':
        context = {
            "items": items,
        }
        return render(request, "myapp/home.html", context)


#検索画面
def search(request):
        
    if request.method == 'GET':
        if 'sort' in request.GET:
            sort =  request.GET['sort']
            if sort == 'a_created_time':
                items = Item.objects.order_by("-sell_time")
            elif sort == 'd_created_time':
                items = Item.objects.order_by("sell_time")
            elif sort == 'a_price':
                items = Item.objects.order_by("price")
            elif sort == 'd_price':
                items = Item.objects.order_by("-price")
        else:
            items = Item.objects.order_by("-sell_time")

        if 'keyword' in request.GET:
            keyword = request.GET['keyword']
            items = (
                items.filter(name__contains=keyword)
            )

        if 'category' in request.GET:
            categories = request.GET.getlist('category')
            items = items.filter(category__in=categories)

        if 'status' in request.GET:
            items = items.filter(is_purchased = False)

        if 'quality' in request.GET:
            qualities = request.GET.getlist('quality')
            items = items.filter(quality__in=qualities)

        if request.user.is_authenticated:
            user = request.user
            items.exclude(seller=user)

        context = {
            "Category":Category,
            "Quality":Quality,
            "Sort":Sort,
            "items": items,
        }
        return render(request, "myapp/search.html", context)


# カテゴリー一覧画面
def category(request):
    if request.method == 'GET':
    
        context = {
            "Category": Category,
        }
        return render(request, "myapp/category.html", context)


#商品詳細の画面
class ItemView(View):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)


        context = {
            "item": item,
            "category":item.get_category_display(),
            "quality":item.get_quality_display(),
        }
        return render(request, "myapp/item.html", context)


#出品画面
@login_required
def sell(request):
    form = SellForm()
    context={
        "form":form
    }
    
    if(request.method == 'POST'):
        user = request.user
        new_item = Item()
        form = SellForm(request.POST, request.FILES)
        context={
            "form":form
        }
        if form.is_valid():
            image = form.cleaned_data['image']
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            quality = form.cleaned_data['quality']
            price = form.cleaned_data['price']
            detail = form.cleaned_data['detail']

            new_item.seller = user
            new_item.image = image
            new_item.name = name
            new_item.category = category
            new_item.quality = quality
            new_item.price = price
            new_item.detail = detail

            new_item.save()
            return redirect(to="/home")
        else:
            return render(request, "myapp/sell.html", context)
    return render(request, "myapp/sell.html", context)


# アカウント設定画面
class SettingsView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'myapp/settings.html'


# プロフィール編集画面
@login_required
def change_profile(request):
    obj = User.objects.get(username=request.user.username)
    if(request.method == 'POST'):
        form=UserForm(request.POST,request.FILES)

        if form.is_valid():
            icon = form.cleaned_data['icon']
            name = form.cleaned_data['username']
            introduction = form.cleaned_data['introduction']

            obj.icon = icon
            obj.username = name
            obj.introduction = introduction
            obj.save()
            return redirect(to="/settings")
    context = {
        'form':UserForm(instance=obj),
    }
    return render(request,'myapp/change_profile.html',context)


# 販売者プロフィール画面
class SellerProfileView(View):
    def get(self, request, seller_id):
        seller = get_object_or_404(User, id=seller_id)
        items = Item.objects.filter(seller = seller)

        context = {
            "seller": seller,
            "items":items,
        }
        return render(request, "myapp/seller_profile.html", context)