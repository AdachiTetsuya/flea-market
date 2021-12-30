from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django .views.generic import View


from .models import Item


User = get_user_model()

# 最初の画面
class IndexView(generic.TemplateView):
    template_name = "myapp/index.html"


# home画面
class HomeView(LoginRequiredMixin,generic.ListView):
    model = Item
    template_name = "myapp/home.html"

    def get_queryset(self):
        user = self.request.user

        items = (
            Item.objects.filter(is_purchased=False).exclude(seller=user)
            .order_by("sell_time").reverse()
        )

        return items


class SearchView(View):
    def get(self, request):
        q_word = request.GET['item_search'].strip()
        items = (
            Item.objects.filter(name__contains=q_word)
            .order_by("sell_time").reverse()
        )
        
        context = {
            "items": items,
        }

        return render(request, "myapp/search.html", context)


#商品詳細の画面
class ItemView(LoginRequiredMixin,View):
    def get(self, request, item_id):
        item = get_object_or_404(Item, id=item_id)

        context = {
            "item": item,
        }
        return render(request, "myapp/item.html", context)

