from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import VendorProduct, Discount, VendorSettlement
from accounts.models import Account


class VendorProductForm(forms.ModelForm):
	class Meta:
		model = VendorProduct
		fields = ['manufacturer_price', 'consumer_price', 'price', 'total_number', 'weight', 'expire_date']


class ProductDiscountForm(forms.ModelForm):
	class Meta:
		model = Discount
		fields = ['expire', 'step_one_number', 'step_one_percent', 'step_two_number', 'step_two_percent']


class AddToCartForm(forms.Form):
	quantity = forms.IntegerField()
