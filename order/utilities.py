from cart.cart import Cart, VendorCart
from .models import Order, OrderItem
from retailer.models import Retailer

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string


def retailer_order_record(request, vendor_slug):
    retailer = request.user.retailer
    cart = Cart(request)

    for vendor_cart in cart:
        if vendor_cart['vendor'].slug == vendor_slug:
            vendor = vendor_cart['vendor']
            paid_amount = int(vendor_cart['total_cost']) - int(vendor_cart['total_discount'])
            total_number = int(vendor_cart['total_number'])

            if vendor_cart['settlement'] == 'cash':
                order = Order.objects.create(buyer=retailer, seller=vendor, paid_amount=paid_amount, total_number=total_number, cash_settlement=True)
            elif vendor_cart['settlement'] == 'draft':
                order = Order.objects.create(buyer=retailer, seller=vendor, paid_amount=paid_amount, total_number=total_number, draft_settlement=True)
            elif vendor_cart['settlement'] == 'trust':
                order = Order.objects.create(buyer=retailer, seller=vendor, paid_amount=paid_amount, total_number=total_number, trust_settlement=True)


            for item in vendor_cart['products'].values():

                discount_percent = 0
                if item['product'].discount.all():
                    discount = item['product'].discount.all()[0]
                    if item['quantity'] > discount.step_two_number:
                        discount_percent = discount.step_two_percent
                    elif item['quantity'] > discount.step_one_number:
                        discount_percent = discount.step_one_percent

                OrderItem.objects.create(order=order, product=item['product'],
                                             price=item['product'].price, quantity=item['quantity'],
                                             discount_percent=discount_percent)
            return order


def vendor_order_record(request):
    vendor = request.user.vendor
    cart = VendorCart(request)
    retailer = cart.get_retailer()

    paid_amount = cart.get_total_cost() - cart.get_total_discount()
    total_number = cart.get_total_number()

    order = Order.objects.create(buyer=retailer, seller=vendor,
                                 paid_amount=paid_amount, total_number=total_number,
                                 cash_settlement=False, seller_confirmation=True)

    for item in cart:
         OrderItem.objects.create(order=order, product=item['product'],
                                             price=item['product'].price, quantity=item['quantity'],
                                             discount_percent=item['discount'])
    return order



def notify_vendor(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    if order:
        to_email = order.seller.user.email
        subject = f'سفارش جدید از {order.buyer.name}'
        text_content = 'برای اطمینان خریدار از پیگیری سفارش، لطفا با مراجعه به حساب کاربری خود در سامانه AD ، سفارش را تایید نمایید + (آدرس ورود به سامانه))'
        html_content = render_to_string('order/email_notify_vendor.html', {'order': order})

        send_mail(subject, text_content, from_email, (to_email,))


def notify_retailer(order):
    from_email = settings.DEFAULT_EMAIL_FROM

    to_email = order.buyer.user.email
    subject = 'ثبت سفارش'
    text_content = 'سفارش شما ثبت شد.'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})

    send_mail(subject, text_content, from_email, (to_email,), )

def retailer_orders_record(request):
    retailer = request.user.retailer
    cart = Cart(request)

    for vendor_cart in cart:
        vendor = vendor_cart['vendor']
        paid_amount = int(vendor_cart['total_cost']) - int(vendor_cart['total_discount'])
        total_number = int(vendor_cart['total_number'])

        if vendor_cart['settlement'] == 'cash':
            order = Order.objects.create(buyer=retailer, seller=vendor, paid_amount=paid_amount, total_number=total_number, cash_settlement=True)
        elif vendor_cart['settlement'] == 'draft':
            order = Order.objects.create(buyer=retailer, seller=vendor, paid_amount=paid_amount, total_number=total_number, draft_settlement=True)
        elif vendor_cart['settlement'] == 'trust':
            order = Order.objects.create(buyer=retailer, seller=vendor, paid_amount=paid_amount, total_number=total_number, tust_settlement=True)




        for item in vendor_cart['products'].values():

            discount_percent = 0
            if item['product'].discount.all():
                discount = item['product'].discount.all()[0]
                if item['quantity'] > discount.step_two_number:
                    discount_percent = discount.step_two_percent
                elif item['quantity'] > discount.step_one_number:
                    discount_percent = discount.step_one_percent

            OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['product'].price, quantity=item['quantity'],
                                         discount_percent=discount_percent)

    return order

