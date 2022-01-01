from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django .views.generic import View

from . utils import ObjectWithFileField,get_avatar_url
from . models import Item,Category


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
    if request.method == 'GET':
        items = (
            Item.objects.filter(is_purchased=False)
            .order_by("sell_time").reverse()
        )
        context = {
            "items": items,
        }
        return render(request, "myapp/home.html", context)



def search(request,category_label):
    if request.method == 'GET':
        user = request.user
        items = (
            Item.objects.filter(category=category_label)
            .order_by("sell_time").reverse()
        )
        context = {
            "items": items,
        }
        return render(request, "myapp/search.html", context)


    if request.method == 'POST':
        q_word = request.POST['item_search'].strip()
        items = (
            Item.objects.filter(name__contains=q_word)
            .order_by("sell_time").reverse()
        )
        
        context = {
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
class ItemView(LoginRequiredMixin,View):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)

        context = {
            "item": item,
            "category":item.get_category_display(),
            "quality":item.get_quality_display(),

        }
        return render(request, "myapp/item.html", context)

