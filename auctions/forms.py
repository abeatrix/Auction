from django.forms import ModelForm, ModelChoiceField
from .models import Listing, Bids, Comments, Category
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

class Item_Form(ModelForm):
    title = forms.CharField(max_length= 200, required=True)

    class Meta:
        model = Listing
        fields = ['title', 'category', 'currentPrice', 'description', 'img']

class Comment_Form(ModelForm):
        class Meta:
            model = Comments
            fields = ['comment']

class Bid_Form(ModelForm):
        class Meta:
            model = Bids
            fields = ['bid']

class Cat_Form(ModelForm):
        class Meta:
            model = Category
            fields = ['name']
