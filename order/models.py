from django.db import models
from vendor.models import Vendor, VendorProduct
from retailer.models import Retailer
from django_jalali.db import models as jmodels


# Create your models here.
class Order(models.Model):
    seller                  = models.ForeignKey(Vendor,verbose_name='فروشنده', related_name="orders", on_delete=models.CASCADE)
    buyer                   = models.ForeignKey(Retailer, verbose_name='خریدار', related_name='orders', on_delete=models.CASCADE)
    created_at              = jmodels.jDateField('تاریخ سفارش', auto_now_add=True)

    paid_amount             = models.DecimalField('مبلغ قابل پرداخت', max_digits=11, decimal_places=0, null=True)
    total_number            = models.DecimalField('تعداد کالا', max_digits=4, decimal_places=0)

    seller_confirmation      = models.BooleanField('تایید نماینده', default=False)
    buyer_confirmation       = models.BooleanField('تایید فروشگاه', default=False)

    cash_settlement         = models.BooleanField('پرداخت هنگام تحوبل', default=False)
    draft_settlement        = models.BooleanField('پرداخت چک', default=False)
    trust_settlement        = models.BooleanField('پرداخت اعتباری', default=False)



    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        return sum(int(item.price) * int(item.product.total_number) * int(item.quantity)
                   for item in self.order_items.all())

    def get_total_discount(self):
        return int(round(sum(int(item.price) * int(item.product.total_number) * int(item.quantity)
                   * float(int(item.discount_percent) / 100)
                   for item in self.order_items.all())))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(VendorProduct, related_name="order_items", on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    quantity = models.IntegerField(default=1)
    discount_percent = models.DecimalField(max_digits=2, decimal_places=0, default=0)

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        return int(self.price) * int(self.product.total_number) * int(self.quantity)

    def get_total_discount(self):
        return int(round(int(self.price) * int(self.product.total_number) * int(self.quantity)
                   * float(int(self.discount_percent) / 100)))
