from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import generic
from django .views.generic import View,ListView
from django.views.generic.base import TemplateView

from . models import Item,Category, Nortify,Quality,Sort,Talk
from . forms import UserForm,SellForm,TalkForm
from . utils import is_notify

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


User = get_user_model()

# ログイン選択画面
class LoginListView(generic.TemplateView):
    template_name = "myapp/login_list.html"

# 会員登録選択画面
class SignupListView(generic.TemplateView):
    template_name = "myapp/signup_list.html"

# ホーム画面
class HomeView(ListView):
    template_name = 'myapp/home.html'
    model = Item
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs).filter(is_purchased=False).order_by('-sell_time')

        if self.request.user.is_authenticated:
            user = self.request.user
            queryset = queryset.exclude(seller=user)

        return queryset
    
    def get_context_data(self):
        ctx = super().get_context_data()
        nortify = False
        if self.request.user.is_authenticated:
            nortify = is_notify(self.request.user)

        ctx['nortify'] = nortify
            
        return ctx

# 検索画面
class SearchView(ListView):
    template_name = 'myapp/search.html'
    model = Item
    context_object_name = 'items' # オブジェクト名を items に指定
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs).order_by("-sell_time")
        if 'sort' in self.request.GET:
            sort =  self.request.GET['sort']
            if sort == 'a_created_time':
                queryset = queryset.order_by("-sell_time")
            elif sort == 'd_created_time':
                queryset = queryset.order_by("sell_time")
            elif sort == 'a_price':
                queryset = queryset.order_by("price")
            elif sort == 'd_price':
                queryset = queryset.order_by("-price")

        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
            queryset = queryset.filter(name__contains=keyword)
        
        if 'category' in self.request.GET:
            categories = self.request.GET.getlist('category')
            queryset = queryset.filter(category__in=categories)

        if 'status' in self.request.GET:
            queryset = queryset.filter(is_purchased = False)

        if 'quality' in self.request.GET:
            qualities = self.request.GET.getlist('quality')
            queryset = queryset.filter(quality__in=qualities)

        return queryset
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            "Category":Category,
            "Quality":Quality,
            "Sort":Sort,
        })

        return ctx


# カテゴリー一覧画面
class CategoryView(TemplateView):
    template_name = 'myapp/category.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['Category'] = Category

        return ctx


#商品詳細の画面
class ItemView(TemplateView):
    template_name = 'myapp/item.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        item = get_object_or_404(Item, id=kwargs.get('item_id'))
        ctx.update({
            "item": item,
            "category":item.get_category_display(),
            "quality":item.get_quality_display(),
        })

        return ctx


# 商品の購入画面
class PurchaseView(View):
    def get(self, request, **kwargs):
        item = get_object_or_404(Item, id=kwargs.get('item_id'))

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
            #nortifyを作る
            notice = Nortify(notice_to=item.seller,friend=user,nortify_item=item)
            notice.set_purchased(item,user)
            notice.save()

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
            #nortifyを作る
            notice = Nortify(notice_to=friend,friend=user,nortify_item=item)
            notice.set_given(user)
            notice.save()

        elif status == 'got':
            item.is_got = True
            item.save()
            #nortifyを作る
            notice = Nortify(notice_to=friend,friend=user,nortify_item=item)
            notice.set_end(user)
            notice.save()

    if "nortify" in request.GET:
        nortify_id = request.GET['nortify']
        nortify = get_object_or_404(Nortify, id=nortify_id)
        nortify.is_checked = True
        nortify.save()

    # POST（メッセージ送信あり）
    if request.method == "POST":
        # 送信内容を取得
        new_talk = Talk(talk_from=user, talk_to=friend, talk_item=item)
        form = TalkForm(request.POST, instance=new_talk)

        # 送信内容があった場合
        if form.is_valid():
            # 保存
            form.save()
            #nortifyを作る
            notice = Nortify(notice_to=friend,friend=user,nortify_item=item)
            notice.set_message(user)
            notice.save()
            # 更新
            return redirect("myapp:talk_room", user_id,item_id)

    # POSTでない（リダイレクトorただの更新）&POSTでも入力がない場合
    return render(request, "myapp/talk_room.html", context)



# お知らせ画面
class NortifyView(TemplateView,LoginRequiredMixin):
    template_name = "myapp/nortify.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'nortifys':Nortify.objects.filter(notice_to=self.request.user).order_by("-time"),
            'nortify':is_notify(self.request.user)
        })
        return ctx

        
        