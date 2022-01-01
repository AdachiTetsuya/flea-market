from django import forms

class ItemSearchForm(forms.Form):
    q_word = forms.CharField(label='検索',required=False)