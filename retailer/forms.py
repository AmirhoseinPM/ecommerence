from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from accounts.models import Account



class AddToCartForm(forms.Form):
	quantity = forms.IntegerField()


class OrderSettelementForm(forms.Form):
	cash_settlement = forms.BooleanField()
	draft_settlement = forms.BooleanField()
	trust_settlement = forms.BooleanField()
