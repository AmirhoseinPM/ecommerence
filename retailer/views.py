from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from . import forms
from cart.cart import Cart
from product.models import Category
from vendor.models import VendorProduct, Vendor
from order.models import Order
from order.utilities import retailer_order_record, retailer_orders_record


# Create your views here.


@login_required()
def mainpage(request):
	cart = Cart(request)
	retailer = request.user.retailer

	return render(request, 'retailer\mainpage.html', {'retailer': retailer,
													  'cart': cart})


@login_required()
def products_view(request):
	cart = Cart(request)
	retailer = request.user.retailer

	# categories that vendors add product from it
	categories = (category for category in Category.objects.all() if category.vendor_products)

	# محصولات توزیع کننده های شهر مربوط به فروشگاه
	city = retailer.city
	vendors = city.vendor.all()
	products = set()
	for vendor in vendors:
		products.update(vendor.get_exist_product())

#	products = random.sample(products, 50)
	return render(request, 'retailer\product\products.html', {'retailer': retailer,
															  'products': products,
															  'categories': categories,
															  'cart': cart})

@login_required()
def product(request, product_slug):
	retailer = request.user.retailer
	product = get_object_or_404(VendorProduct, slug=product_slug)
	vendor_slug = product.vendor.slug

	cart = Cart(request)

	if request.POST:
		form = forms.AddToCartForm(request.POST)
		if form.is_valid():
			quantity = form.cleaned_data['quantity']
			cart.add(vendor_slug=vendor_slug, product_slug=product.slug, quantity=quantity, update_quantity=False)

			return redirect('products')
	else:
		form = forms.AddToCartForm()


	return render(request, 'retailer/product/product.html', {'cart': cart,
															 'retailer': retailer,
															 'product': product,
															 'form': form})


@login_required()
def discounts(request):
	cart = Cart(request)
	retailer = request.user.retailer

	city = retailer.city
	vendors = city.vendor.all()
	products = set()
	for vendor in vendors:
		products.update(vendor.get_discounted_products())

	categories = Category.objects.all()

	return render(request, 'retailer\product\discounts.html', {'retailer': retailer,
															 'products': products,
															 'categories': categories,
															   'cart': cart})


@login_required()
def vendors_view(request):
	cart = Cart(request)
	retailer = request.user.retailer
	city = retailer.city
	vendors = city.vendor.all()

	return render(request, 'retailer\\vendor\\vendors_view.html', {'retailer': retailer,
																   'vendors': vendors,
																   'cart': cart})




@login_required()
def vendor(request, vendor_slug):
	cart = Cart(request)
	retailer = request.user.retailer
	vendor = get_object_or_404(Vendor, slug=vendor_slug)

	return render(request, 'retailer\\vendor\\vendor.html', {'cart': cart,
															 'retailer': retailer,
															 'settlement': vendor.settlement,
															 'vendor': vendor})




@login_required()
def carts(request):
	cart = Cart(request)
	retailer = request.user.retailer

	remove_vendor = request.GET.get('remove_vendor', '')
	if remove_vendor:
		cart.remove_vendor(remove_vendor)
		return redirect('retailer_carts')

	remove_product = request.GET.get('remove_product', '')  # get vendor product slug
	vendor_product = request.GET.get('vendor_product', '')
	if remove_product:
		cart.remove_product(vendor_product, remove_product)
		return redirect('retailer_carts')


	change_quantity = request.GET.get('change_quantity', '')
	vendor = request.GET.get('vendor', '')
	quantity = request.GET.get('quantity', 0)
	if change_quantity:
		cart.add(vendor, change_quantity, quantity, update_quantity=True)
		return redirect('retailer_carts')


	save_orders = request.GET.get('save_orders', '')
	if save_orders:
		orders = retailer_orders_record(request)


		if orders:
			cart.clear()
			#notify_vendor(order)
			#notify_retailer(order)
			return redirect('order_success')

	return render(request, 'retailer\cart\cart.html', {'cart': cart,
													   'retailer': retailer})


@login_required()
def vendor_cart(request, vendor_slug):
	retailer = request.user.retailer
	cart = Cart(request)
	for vendor_cart in cart:
		if vendor_cart['vendor'].slug == vendor_slug:

			removed_vendor = request.GET.get('remove_vendor', '')
			if removed_vendor:
				cart.remove_vendor(removed_vendor)
				return redirect('retailer')

			remove_product = request.GET.get('remove_product', '')  # get vendor product slug
			vendor_product = request.GET.get('vendor_product', '')
			if remove_product:
				cart.remove_product(vendor_product, remove_product)
				return redirect('cart')


			change_quantity = request.GET.get('change_quantity', '')
			vendor = request.GET.get('vendor', '')
			quantity = request.GET.get('quantity', 0)
			if change_quantity:
				cart.add(vendor, change_quantity, quantity, update_quantity=True)
				return redirect('cart')



			return render(request, 'retailer\cart\\vendor_cart.html', {'retailer': retailer,
																	   'vendor_settlement': vendor_cart['vendor'].settlement,
																	   'cart': cart,
																	   'vendor_cart': vendor_cart})


@login_required()
def order_success(request):
	retailer = request.user.retailer
	cart = Cart(request)

	return render(request, 'retailer\cart\success.html', {'cart': cart,
														  'retailer': retailer})


@login_required()
def current_order_view(request):
	retailer = request.user.retailer
	cart = Cart(request)
	orders = retailer.orders.all()
	orders = orders.filter(buyer_confirmation=False)

	order_confirmation = request.GET.get('order_confirmation', '')
	if order_confirmation:
		order = Order.objects.get(id=order_confirmation)
		order.buyer_confirmation = True
		order.save()
		return redirect('retailer_current_orders')

	return render(request, 'retailer\order\current_orders.html', {'retailer': retailer,
																  'cart': cart,
																  'orders': orders})


@login_required()
def final_order_view(request):
	retailer = request.user.retailer
	cart = Cart(request)

	orders = retailer.orders.all()
	orders = orders.filter(buyer_confirmation=True)

	return render(request, 'retailer\order\\final_orders.html', {'retailer': retailer,
																 'cart': cart,
																 'orders': orders})


@login_required
def edit_retailer(request):
	retailer = request.user.retailer
	cart = Cart(request)

	if request.method == 'POST':
		name = request.POST.get('name', '')
		email = request.POST.get('email', '')
		username = request.POST.get('username', '')
		phone = request.POST.get('phone', '')
		manager_name = request.POST.get('manager_name', '')
		manager_phone = request.POST.get('manager_phone', '')
		if name:
			retailer.user.email = email
			retailer.user.username = username
			retailer.user.save()

			retailer.name = name
			retailer.phone = phone
			retailer.manager_name = manager_name
			retailer.manager_phone = manager_phone
			retailer.save()
			return redirect('retailer_mainpage')

	return render(request, 'retailer/edit_retailer.html', {'retailer': retailer,
														   'cart': cart})

