from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Q, Subquery
from django.views import generic
from django .views.generic import View
from django.views.generic.base import TemplateView

from . models import Item,Category,Quality,Sort,Talk
from .forms import UserForm,SellForm,TalkForm

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


User = get_user_model()

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

# 商品の購入画面
class PurchaseView(View):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)

        context = {
            "item": item,
            "publick_key":settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, "myapp/purchase.html", context)

    def post(self, request, item_id):
        """購入時の処理"""
        item = get_object_or_404(Item, id=item_id)
        item.is_purchased = True
        item.save()
        user = request.user
        token = request.POST['stripeToken']  # フォームでのサブミット後に自動で作られる
        try:
            # 購入処理
            charge = stripe.Charge.create(
                amount=item.price,
                currency='jpy',
                source=token,
                description='書籍名:{}'.format(item.name),
            )
        except stripe.error.CardError as e:
            # カード決済が上手く行かなかった(限度額超えとか)ので、メッセージと一緒に再度ページ表示
            context = self.get_context_data()
            context['message'] = 'Your payment cannot be completed. The card has been declined.'
            item.is_purchased = False
            item.save()
            return render(request, 'myapp/purchase.html', context)
        else:
            # 上手く購入できた。
            item.buyer = user
            item.is_settle = True
            item.save()
            user.buy_num += 1
            user.save()
            user_id = item.seller.id

            return redirect("myapp:talk_room", user_id,item_id)


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
            user.sell_num += 1
            user.save()
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

#マイページ
class MyPageView(generic.TemplateView):
    template_name = "myapp/mypage.html"

class ListingsView(View):
    def get(self, request, status):
        if status == 'listing':
            items = Item.objects.filter(seller=request.user,is_purchased = False)
        elif status == 'in_progress':
            items = Item.objects.filter(seller=request.user,is_purchased = True, is_got = False)
        elif status == 'completed':
            items = Item.objects.filter(seller=request.user,is_got = True)
        context = {
            "items": items,
        }
        return render(request, "myapp/mypage_listings.html",context)

class PurchasesView(View):
    def get(self, request, status):
        if status == 'in_progress':
            items = Item.objects.filter(buyer=request.user,is_purchased = True,is_got = False)
        elif status == 'completed':
            items = Item.objects.filter(buyer=request.user,is_got = True)

        context = {
            "items": items,
        }
        return render(request, "myapp/mypage_purchases.html",context)


# トーク画面
@login_required
def talk_room(request,user_id,item_id):
    user = request.user
    friend = get_object_or_404(User, id=user_id)
    item = get_object_or_404(Item, id=item_id)
    talk = Talk.objects.filter(
        Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
    ).filter(talk_item = item).order_by("time")
    form = TalkForm()
    if item.is_settle == True:
        buyer = item.buyer
    else:
        buyer = None
        
    context = {
        "form": form,
        "talks": talk,
        "item":item,
        "friend":friend,
        "user":user,
        "buyer":buyer,
    }
    if "status" in request.GET:
        status = request.GET['status']
        if status == 'given':
            item.is_given = True
            item.save()
        elif status == 'got':
            item.is_got = True
            item.save()

    # POST（メッセージ送信あり）
    if request.method == "POST":
        # 送信内容を取得
        new_talk = Talk(talk_from=user, talk_to=friend, talk_item=item)
        form = TalkForm(request.POST, instance=new_talk)

        # 送信内容があった場合
        if form.is_valid():
            # 保存
            form.save()
            # 更新
            return redirect("myapp:talk_room", user_id,item_id)

    # POSTでない（リダイレクトorただの更新）&POSTでも入力がない場合
    return render(request, "myapp/talk_room.html", context)


