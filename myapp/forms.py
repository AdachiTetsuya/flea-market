from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class ItemSearchForm(forms.Form):
    q_word = forms.CharField(label='検索',required=False)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','icon','introduction']
