from django.forms import ModelForm, ModelChoiceField
from .models import Listing, Bids, Comments, Category
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

# For for creating Listing
class Item_Form(ModelForm):
    title = forms.CharField(max_length= 200, required=True)

    class Meta:
        model = Listing
        fields = ['title', 'category', 'currentPrice', 'description', 'img']

# For for creating Comments
class Comment_Form(ModelForm):
        class Meta:
            model = Comments
            fields = ['comment']

# Form for creating Bids
class Bid_Form(ModelForm):
        class Meta:
            model = Bids
            fields = ['bid']

# Form for creating Category
class Cat_Form(ModelForm):
        class Meta:
            model = Category
            fields = ['name']
