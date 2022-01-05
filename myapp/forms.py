from django import forms
from django.contrib.auth import get_user_model
from django.forms import fields, widgets
from django.forms.formsets import formset_factory

User = get_user_model()
from .models import Item, Quality

class ItemSearchForm(forms.Form):
    q_word = forms.CharField(label='検索',required=False)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username','icon','introduction']
        labels = {
            'username':'ニックネーム',
            'icon':'アイコン画像',
            'introduction':'自己紹介',
        }







class SellForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'name'}))
    detail = forms.CharField(widget=forms.Textarea(attrs={'placeholder': '色、素材、重さ、定価、注意点など'}))
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': '0'}))

    
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