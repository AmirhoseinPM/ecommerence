from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from accounts.models import Account


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError(" رمز عبور یا ایمیل اشتباه است ")


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

	class Meta:
		model = Account
		fields = ('email', 'phone', 'username',  'password1', 'password2')

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError(' این ایمیل قبلا استفاده شده است')

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(phone=phone)
		except Account.DoesNotExist:
			return phone
		raise forms.ValidationError(' این شماره قبلا استفاده شده است')


	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError(' این نام کاربری قبلا استفاده شده است')
