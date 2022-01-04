from django import forms
from django.contrib.auth import get_user_model
from django.forms import fields
from django.forms.formsets import formset_factory
User = get_user_model()
from .models import Item, Quality

class ItemSearchForm(forms.Form):
    q_word = forms.CharField(label='検索',required=False)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','icon','introduction']


class SellForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('image','category','quality','name','detail','price')
        labels = {
            'image':'出品画像',
            'category':'カテゴリー',
            'quality':'商品の状態',
            'name':'商品名',
            'detail':'商品の説明',
            'price':'販売価格',
        }