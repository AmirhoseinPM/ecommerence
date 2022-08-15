from django.conf import settings
from vendor.models import VendorProduct, Discount, Vendor
from product.models import Product
from django.shortcuts import get_object_or_404
from retailer.models import Retailer
from django.core import serializers




class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for vendor_slug in self.cart.keys():
            self.cart[str(vendor_slug)]['vendor'] = Vendor.objects.get(slug=vendor_slug)
            for product_slug in self.cart[vendor_slug]['products'].keys():
                self.cart[str(vendor_slug)]['products'][str(product_slug)]['product'] = VendorProduct.objects.get(slug=product_slug)

        for vendor_slug, vendor_cart in self.cart.items():
            for item in vendor_cart['products'].values():
                item['total_price'] = item['product'].price * item['product'].total_number * item['quantity']
                item['discount'] = 0
                if item['product'].discount.all():
                    discount = item['product'].discount.all()[0]
                    if item['quantity'] > discount.step_two_number:
                        item['discount'] = item['total_price'] * (discount.step_two_percent / 100)
                    elif item['quantity'] > discount.step_one_number:
                        item['discount'] = item['total_price'] * (discount.step_one_percent / 100)
            vendor_cart['total_cost'] = self.get_total_vendor_cost(vendor_slug)
            vendor_cart['total_discount'] = self.get_total_discount(vendor_slug)
            vendor_cart['total_number'] = self.get_total_number(vendor_slug)
            yield vendor_cart

    def __len__(self):
        cart_length = 0
        for vendor in self.cart.values():
            cart_length += sum(int(item['quantity']) for item in vendor['products'].values())
        return cart_length

    def add(self, vendor_slug, product_slug, quantity=1, update_quantity=False):
        product_slug = str(product_slug)
        vendor_slug = str(vendor_slug)

        if vendor_slug not in self.cart:
            self.cart[vendor_slug] = {'products': {}, 'vendor': vendor_slug, 'settlement': 'cash'}
            self.cart[vendor_slug]['products'][product_slug] = {'quantity': quantity, 'product_slug': product_slug}
        elif product_slug not in self.cart[vendor_slug]['products']:
            self.cart[vendor_slug]['products'][product_slug] = {'quantity': quantity, 'product_slug': product_slug}

        if update_quantity:
            self.cart[vendor_slug]['products'][product_slug]['quantity'] += int(quantity)

            if self.cart[vendor_slug]['products'][product_slug]['quantity'] == 0:
                self.remove_product(vendor_slug, product_slug)

        self.save()


    def remove_product(self, vendor_slug, product_slug):
        if product_slug in self.cart[vendor_slug]['products']:
            del self.cart[vendor_slug]['products'][product_slug]
            self.save()


    def remove_vendor(self, vendor_slug):
        if str(vendor_slug) in self.cart.keys():
            del self.cart[str(vendor_slug)]
            self.save()


    def add_settlement(self, vendor_slug, settlement):
        if vendor_slug in self.cart:
            self.cart[vendor_slug]['settlement'] = settlement


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


    def get_total_vendor_cost(self, vendor_slug):
        for product_slug in self.cart[vendor_slug]['products'].keys():
            self.cart[vendor_slug]['products'][str(product_slug)]['product'] = get_object_or_404(VendorProduct, slug=product_slug)

        return sum(item['total_price'] for item in self.cart[vendor_slug]['products'].values())


    def get_total_discount(self, vendor_slug):
        for product_slug in self.cart[vendor_slug]['products'].keys():
            self.cart[vendor_slug]['products'][str(product_slug)]['product'] = get_object_or_404(VendorProduct, slug=product_slug)

        return sum(item['discount'] for item in self.cart[vendor_slug]['products'].values())


    def get_total_number(self, vendor_slug):
        return sum(item['quantity'] for item in self.cart[vendor_slug]['products'].values())


    def get_settlement(self, vendor_slug, settlement):
        self.cart[vendor_slug]['settlement'] = settlement
        return settlement


class VendorCart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for slug in self.cart['products'].keys():
            self.cart['products'][str(slug)]['product'] = VendorProduct.objects.get(slug=slug)


        for item in self.cart['products'].values():
            if not item['vol_discounted']:
                if item['product'].discount.all():
                    discount = item['product'].discount.all()[0]
                    if item['quantity'] > discount.step_two_number:
                        item['discount'] += int(discount.step_two_percent)
                        item['vol_discounted'] = True
                    elif item['quantity'] > discount.step_one_number:
                        item['discount'] += (discount.step_one_percent)
                        item['vol_discounted'] = True
            item['final_price'] = int(round(int(item['product'].price) * int(item['product'].total_number) *\
                                  int(item['quantity']) * (1 - (item['discount'] / 100))))

            yield item

    def __len__(self):
        if self.cart.keys():
            # if just add retailer to cart
            if not self.cart['products'].values() and self.cart['retailer']:
                return True
            return sum(item['quantity'] for item in self.cart['products'].values())
        else:
            return False

    def add_product(self, product_slug, quantity=0, update_quantity=False, update_discount=False, discount=0):
        product_slug = str(product_slug)

        if 'retailer' not in self.cart.keys():
            self.cart['retailer'] = None
        if 'products' not in self.cart.keys():
            self.cart['products'] = {}

        if product_slug not in self.cart['products']:
            self.cart['products'][product_slug] = {'quantity': 0, 'product': product_slug,
                                                   'discount': 0, 'vol_discounted': False}

        if update_quantity:
            self.cart['products'][product_slug]['quantity'] += int(quantity)

            if self.cart['products'][product_slug]['quantity'] == 0:
                self.remove_product(product_slug)

        if update_discount:
            self.cart['products'][product_slug]['discount'] += int(discount)

        self.save()


    def add_retailer(self, retailer_slug):
        if 'products' not in self.cart.keys():
            self.cart['products'] = {}
        self.cart['retailer'] = retailer_slug
        self.save()

    def get_retailer(self):
        if self.cart['retailer']:
            return Retailer.objects.get(slug=self.cart['retailer'])

    def remove_retailer(self):
        self.cart['retailer'] = None
        self.save()

    def remove_product(self, product_slug):
        if product_slug in self.cart['products']:
            del self.cart['products'][product_slug]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        for slug in self.cart['products'].keys():
            self.cart['products'][str(slug)]['product'] = VendorProduct.objects.get(slug=slug)

        return sum(int(item['quantity'] * item['product'].price * item['product'].total_number) for item in self.cart['products'].values())


    def get_total_discount(self):
        for slug in self.cart['products'].keys():
            self.cart['products'][str(slug)]['product'] = VendorProduct.objects.get(slug=slug)

        return sum(int(round((item['discount'] / 100) * int(item['product'].price)
                   * int(item['product'].total_number) * int(item['quantity']))) for item in self.cart['products'].values())


    def get_total_number(self):
        return sum(item['quantity'] for item in self.cart['products'].values())

