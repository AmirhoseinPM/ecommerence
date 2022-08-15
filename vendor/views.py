from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.db.models import Q


from . import forms
from .models import VendorProduct, VendorSettlement

from product.models import Product, Brand, SubBrand
from retailer.models import Retailer
from order.models import Order
from order.utilities import vendor_order_record
from cart.cart import VendorCart

import random


@login_required()
def mainpage(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	return render(request, 'vendor\mainpage.html', {'vendor': vendor,
													'vendor_cart': cart,
													'current_orders': vendor.get_current_orders})


@login_required()
def vendor_admin(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	if VendorSettlement.objects.filter(vendor__slug=vendor.slug):
		settlement = vendor.settlement
	else:
		settlement = VendorSettlement.create(cls=VendorSettlement, vendor_slug=vendor.slug)

	return render(request, 'vendor\\vendor_admin.html', {'vendor': vendor,
														 'settlement': settlement,
														 'vendor_cart': cart,
														 'current_orders': vendor.get_current_orders})



@login_required()
def local_products(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	return render(request, 'vendor\product\local_products.html', {'vendor': vendor,
																  'vendor_cart': cart,
																  'brands': vendor.brands.all ,
																  'current_orders': vendor.get_current_orders})



def brand_local_product(request, brand_slug):
	vendor = request.user.vendor
	cart = VendorCart(request)

	vendor_brands = vendor.brands.all()
	vendor_brand  = vendor_brands.filter(slug=brand_slug)[0]


	return render(request, 'vendor\product\local_brand_products.html', {'vendor': vendor,
																		'vendor_cart': cart,
																		'brand': vendor_brand,
																		'brands': vendor_brands,
																		'products': vendor_brand.products.all,
																		'current_orders': vendor.get_current_orders})


@login_required()
def add_product(request, product_slug):
	vendor = request.user.vendor
	cart = VendorCart(request)

	original_product = Product.objects.get(slug=product_slug)
	if request.POST:
		form = forms.VendorProductForm(request.POST)
		if form.is_valid():
			vendor_product = form.save(commit=False)
			vendor_product.product = original_product
			vendor_product.vendor = request.user.vendor
			vendor_product.slug = slugify(random.randint(1, 100000000000000000000))
			vendor_product.brand = original_product.brand
			vendor_product.category = original_product.category
			vendor_product.subcategory = original_product.subcategory
			vendor_product.sub_brand = original_product.sub_brand
			random.seed(int(vendor_product.slug))
			vendor_product.save()

			return redirect('vendor_products')
	else:
		form = forms.VendorProductForm()

	return render(request, 'vendor\product\\add_product.html', {'vendor': vendor,
																'form': form,
																'vendor_cart': cart,
																'current_orders': vendor.get_current_orders,
																'product': original_product})


@login_required()
def vendor_products(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	return render(request, 'vendor\product\\vendor_products.html', {'vendor': vendor,
																	'brands': vendor.brands.all,
																	'vendor_cart': cart,
																	'products': vendor.get_exist_product,
																	'current_orders': vendor.get_current_orders })



@login_required()
def vendor_product(request, product_slug):
	vendor = request.user.vendor
	product = get_object_or_404(VendorProduct, slug=product_slug)
	cart = VendorCart(request)

	archive_product = request.GET.get('archive_product', '')
	if archive_product:
		product.exist = False
		product.save()
		return redirect('vendor_products')

	if request.POST:
		form = forms.AddToCartForm(request.POST)
		if form.is_valid():
			quantity = form.cleaned_data['quantity']
			cart.add_product(product_slug=product.slug, quantity=quantity, update_quantity=True, update_discount=False)

			return redirect('vendor_products')
	else:
		form = forms.AddToCartForm()

	return render(request, 'vendor/product/product.html', {'vendor': vendor, 'product': product,
														   'vendor_cart': cart,
														   'form': form,
														   'current_orders': vendor.get_current_orders })



@login_required()
def add_discount(request, product_slug):
	vendor = request.user.vendor
	cart = VendorCart(request)

	product = VendorProduct.objects.get(slug=product_slug)
	if request.POST:
		form = forms.ProductDiscountForm(request.POST)
		if form.is_valid():
			product_discount = form.save(commit=False)
			product_discount.product = product
			product_discount.vendor = vendor
			product_discount.save()

			return redirect('vendor_discounts')
	else:
		form = forms.ProductDiscountForm()

	return render(request, 'vendor\product\\add_discount.html', {'vendor': vendor, 'form': form,
																 'vendor_cart': cart,
																 'product': product, 'current_orders': vendor.get_current_orders })


@login_required()
def discounts(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	discounts = vendor.discount.all()
	products = (discount.product for discount in discounts if discount.product.exist)

	return render(request, 'vendor\product\discounts.html', {'vendor': vendor, 'products': products,
															 'vendor_cart': cart,
															 'current_orders': vendor.get_current_orders })




@login_required()
def archives_product(request, product_slug):
	vendor = request.user.vendor
	cart = VendorCart(request)

	product = get_object_or_404(Product, slug=product_slug)

	products = product.vendor_products.all()
	products = products.filter(exist=False)

	return render(request, 'vendor\product\\archives_product.html', {'vendor': vendor,
																	 'current_orders': vendor.get_current_orders,
																	 'vendor_cart': cart,
																	 'product': product,
																	 'products': products})



@login_required()
def brand_view(request, brand_slug):
	vendor = request.user.vendor
	cart = VendorCart(request)

	brand = get_object_or_404(Brand, slug=brand_slug)

	products = brand.vendor_products.all()
	products = products.filter(vendor=vendor)
	products = products.filter(exist=True)

	return render(request,'vendor\product\\brand.html', {'vendor': vendor,
														 'brand': brand,
														 'vendor_cart': cart,
														 'products': products,
														 'current_orders': vendor.get_current_orders })


@login_required()
def sub_brand_view(request, sub_brand_slug):
	vendor = request.user.vendor
	cart = VendorCart(request)

	sub_brand = get_object_or_404(SubBrand, slug=sub_brand_slug)

	products = sub_brand.vendor_products.all()
	products = products.filter(vendor=vendor)
	products = products.filter(exist=True)

	return render(request, 'vendor\product\sub_brand.html', {'vendor': vendor,
															 'sub_brand': sub_brand,
															 'sub_brand_products': products,
															 'vendor_cart':cart,
															 'current_orders': vendor.get_current_orders})



@login_required()
def search(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	query = request.GET.get('query', '') # second is default parameter which is empty

	products_results = VendorProduct.objects.filter(Q(product__title__icontains=query)
												   | Q(product__description__icontains=query)
												   | Q(product__description__icontains=query)
												   | Q(subcategory__title__icontains=query)
													| Q(sub_brand__title__icontains=query))
	products_results = products_results.filter(exist=True)
	products_results = (product for product in products_results if product.vendor.name == vendor.name)


	original_products_results = Product.objects.filter(Q(title__icontains=query)
												   | Q(description__icontains=query)
												   | Q(brand__title__icontains=query)
												   | Q(subcategory__title__icontains=query)
													| Q(sub_brand__title__icontains=query))

	original_products_results = (product for product in original_products_results if product.brand in vendor.brands.all())


	retailers_results = Retailer.objects.filter(Q(user__username__icontains=query)
											| Q(name__icontains=query)
											| Q(manager_name__icontains=query))


	vendor_products_query = request.GET.get('vendor_products', '')
	local_products_query = request.GET.get('local_products', '')
	retailers_query = request.GET.get('retailers_results', '')

	# filter results
	if vendor_products_query:
		original_products_results = None
		retailers_results = None
	elif local_products_query:
		products_results = None
		retailers_results = None
	elif retailers_query:
		original_products_results = None
		products_results = None


	# for add retailer to cart from search page
	add_to_cart = request.GET.get('add_to_cart', '')
	retailer_slug = request.GET.get('retailer', '')
	if add_to_cart:
		cart.add_retailer(retailer_slug)
		cart.save()
		return redirect('vendor_products')


	return render(request, 'vendor\search.html', {'vendor': vendor,
												  'products': products_results,
												  'original_products': original_products_results,
												  'retailers': retailers_results,

												  'vendor_cart': cart,
												  'query': query,
												  'current_orders': vendor.get_current_orders})



@login_required
def retailers(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	retailers = dict()
	for city in vendor.cities.all():
		retailers[city.name] = dict()
		for region in city.region.all():
			retailers[city.name][region.name] = region.retailer.all()


	add_to_cart = request.GET.get('add_to_cart', '')
	retailer = request.GET.get('retailer', '')
	if add_to_cart:
		cart.add_retailer(retailer)
		cart.save()
		return redirect('vendor_products')


	return render(request, 'vendor\\retailer\\retailers.html', {'vendor': vendor, 'city_retailers':retailers,
																'vendor_cart': cart,
																'current_orders': vendor.get_current_orders})


def retailer_view(request, retailer_slug):
	vendor = request.user.vendor
	retailer = get_object_or_404(Retailer, slug=retailer_slug)
	orders = retailer.orders.all()
	cart = VendorCart(request)

	add_to_cart = request.GET.get('add_to_cart', '')
	if add_to_cart:
		cart.add_retailer(retailer.slug)
		cart.save()
		return redirect('vendor_products')

	return render(request, 'vendor\\retailer\\retailer_view.html', {'vendor': vendor, 'retailer': retailer, 'orders': orders,
																	'vendor_cart': cart,
																	'current_orders': vendor.get_current_orders})



@login_required()
def current_order_view(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	order_confirmation = request.GET.get('order_confirmation', '')
	if order_confirmation:
		order = Order.objects.get(id=order_confirmation)
		order.seller_confirmation = True
		order.save()
		return redirect('vendor_current_orders')

	return render(request, 'vendor\order\current_orders.html', {'vendor': vendor,
																'vendor_cart': cart,
																'orders': vendor.get_current_orders,
																'current_orders': vendor.get_current_orders})


@login_required()
def sending_order_view(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	return render(request, 'vendor\order\sending_orders.html', {'vendor': vendor,
																'orders': vendor.get_sending_orders,
																'vendor_cart': cart,
																'current_orders': vendor.get_current_orders})


@login_required()
def final_order_view(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	return render(request, 'vendor\order\\final_orders.html', {'vendor': vendor,
															   'orders': vendor.get_final_orders,
															   'vendor_cart':cart,
															   'current_orders': vendor.get_current_orders})


@login_required
def edit_vendor(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	if request.method == 'POST':
		name = request.POST.get('name', '')
		email = request.POST.get('email', '')
		username = request.POST.get('username', '')
		address = request.POST.get('address', '')
		phone = request.POST.get('phone', '')
		manager_name = request.POST.get('manager_name', '')
		manager_phone = request.POST.get('manager_phone', '')

		vendor.user.email = email
		vendor.user.username = username
		vendor.user.phone = phone
		vendor.user.save()

		vendor.name = name
		vendor.full_add = address
		vendor.manager_name = manager_name
		vendor.manager_phone = manager_phone
		vendor.save()
		return redirect('vendor_admin')

	return render(request, 'vendor/edit_vendor.html', {'vendor': vendor,
													   'vendor_cart':cart,
													   'current_orders': vendor.get_current_orders})


def settlement(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	if request.method == 'POST':
		cash_discount_percent = request.POST.get('cash_discount_percent', '')
		draft = request.POST.get('draft', '')
		draft_days = request.POST.get('draft_days', '')
		trust = request.POST.get('trust', '')
		trust_days = request.POST.get('trust_days', '')


		vendor.settlement.cash_discount_percent = cash_discount_percent
		vendor.settlement.draft = draft
		vendor.settlement.draft_days = draft_days
		vendor.settlement.trust = trust
		vendor.settlement.trust_days = trust_days
		vendor.settlement.save()

		return redirect('vendor_admin')

	return render(request, 'vendor/edit_settlement.html', {'vendor': vendor,
														   'settlement': vendor.settlement,
														   'vendor_cart':cart,
														   'current_orders': vendor.get_current_orders})


def vendor_cart(request):
	vendor = request.user.vendor
	cart = VendorCart(request)



	remove_product = request.GET.get('remove_product', '')  # get vendor product slug
	if remove_product:
		cart.remove_product(remove_product)
		return redirect('vendor_sell_cart')

	clear = request.GET.get('clear', '')  # get vendor product slug
	if clear:
		cart.clear()
		return redirect('vendor_products')


	change_quantity = request.GET.get('change_quantity', '')
	quantity = request.GET.get('quantity', 0)
	if change_quantity:
		cart.add_product(change_quantity, quantity=int(quantity), update_quantity=True)
		return redirect('vendor_sell_cart')

	change_discount = request.GET.get('change_discount', '')  # discounted product slug
	discount = request.GET.get('discount', 0)
	if change_discount:
		cart.add_product(change_discount, update_discount=True, discount=discount)
		return redirect('vendor_sell_cart')

	add_retailer = request.GET.get('add_retailer', '')
	if add_retailer:
		return redirect('vendor_retailers')

	remove_retailer = request.GET.get('remove_retailer', '')
	if remove_retailer:
		cart.remove_retailer()
		cart.save()
		return redirect('vendor_retailers')

	retailer = None
	if cart:
		retailer = cart.get_retailer()

	# create order from cart
	save_order = request.GET.get('save_order', '')
	if save_order:
		order = vendor_order_record(request)

		if order:
			cart.clear()
			#notify_vendor(order)
			#notify_retailer(order)
			return redirect('vendor_order_success')

	return render(request, 'vendor\cart\\vendor_cart.html', {'vendor': vendor,
															 'retailer': retailer,
															 'vendor_cart': cart,
														     'current_orders': vendor.get_current_orders })



@login_required()
def order_success(request):
	vendor = request.user.vendor
	cart = VendorCart(request)

	return render(request, 'vendor\cart\success.html', {'vendor_cart': cart,
														 'vendor': vendor,
														 'current_orders': vendor.get_current_orders})

def order_view(request, order_id):
	vendor = request.user.vendor
	cart = VendorCart(request)
	order = get_object_or_404(Order, id=order_id)
	retailer = order.buyer


	return render(request, 'vendor\order\order_view.html', {'vendor_cart': cart,
														 'vendor': vendor,
														'order': order,
														'retailer': retailer,
														 'current_orders': vendor.get_current_orders})

