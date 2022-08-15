from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from . import forms


# Create your views here.

def frontpage(request):
    return render(request, 'accounts\\frontpage.html')

def contact_us(request):
    return render(request, 'accounts\contactus.html')


def logout_view(request):
	logout(request)
	return redirect("frontpage")


def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated:
		if user.vendor:
			return redirect('mainpage')
		elif user.retailer:
			return redirect('retailer_mainpage')
		return redirect('seccess')

	context = {}
	if request.POST:
		form = forms.RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			destination = kwargs.get("next")
			if destination:
				return redirect(destination)
			return redirect('success')

		else:
			context['registration_form'] = form

	else:
		form = forms.RegistrationForm()
		context['registration_form'] = form
	return render(request, 'accounts/register.html', context)

def success(request):
	return render(request, 'accounts\success.html')


def login_view(request, *args, **kwargs):
	context = {}

	user = request.user
	if user.is_authenticated:
		if user.is_vendor:
			redirect('vendor')
		elif user.is_retailer:
			redirect('retailer')

		return redirect('success')

	destination = get_redirect_if_exists(request)
	print("destination: " + str(destination))

	if request.POST:
		form = forms.AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				if destination:
					return redirect(destination)
				if user.is_vendor:
					return redirect('vendor')
				elif user.is_retailer:
					return redirect('retailer')
				return redirect("contactus")

	else:
		form = forms.AccountAuthenticationForm()

	context['login_form'] = form

	return render(request, "accounts/login.html", context)


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))
	return redirect

