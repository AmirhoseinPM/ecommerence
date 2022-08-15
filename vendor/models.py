from django.db import models
from accounts.models import Account, City, Region
from product.models import Product, Brand, Category, SubCategory, SubBrand
from django.utils.timezone import now
from django_jalali.db import models as jmodels

# Create your models here.
class Vendor(models.Model):
    user         = models.OneToOneField(Account, related_name='vendor', on_delete=models.CASCADE, primary_key=True)  # فیلدهای عمومی

    # other fields
    name = models.CharField('نام', max_length=255, blank=True)

    city         = models.ForeignKey(City, null=True, verbose_name='شهر', related_name='vendor_city', on_delete=models.CASCADE)
    eco_num      = models.CharField(' کد اقتصادی ', max_length=12, blank=False, unique=True)  # شماره اقتصادی
    post_code    = models.CharField(' کد پستی ', default='', max_length=10, blank=False)  # کد پستی
    full_add     = models.CharField(' آدرس کامل ', default='', max_length=150, null=True, blank=True)  # آدرس کامل

    manager_name    = models.CharField('نام مدیر', default='', blank=True, max_length=30)
    manager_phone   = models.CharField(' شماره مدیر', default='', max_length=20, blank=False)

    brands      = models.ManyToManyField(Brand, related_name='vendor')
    cities      = models.ManyToManyField(City, related_name='vendor')
    slug        = models.SlugField(max_length=55, null=True, unique=True)

    def __str__(self):
        return self.name

    def get_exist_product(self):
        products = self.vendor_products.all()
        products = products.filter(exist=True)
        return products

    def get_discounted_products(self):
        return (discount.product for discount in self.discount.all() if discount.product.exist)

    def get_current_orders(self):
        orders = self.orders.all()
        current_orders = orders.filter(seller_confirmation=False)
        return current_orders

    def get_final_orders(self):
        orders = self.orders.all()
        orders = orders.filter(buyer_confirmation=True)
        return orders

    def get_sending_orders(self):
        orders = self.orders.all()
        orders = orders.filter(seller_confirmation=True)
        orders = orders.filter(buyer_confirmation=False)
        return orders

class VendorSettlement(models.Model):
    vendor       = models.OneToOneField(Vendor, related_name='settlement', on_delete=models.CASCADE, primary_key=True)
    date_added   = jmodels.jDateField('تاریخ درج', auto_now_add=True)

    cash         = models.BooleanField('پرداخت هنگام تحوبل', default=True)
    cash_discount_percent = models.DecimalField('درصد تخفیف تسویه نقدی', default=0, max_digits=2, decimal_places=0)

    draft        = models.BooleanField('پرداخت چک', default=False)
    draft_days   = models.DecimalField('حداکثر مهلت چک', max_digits=2, decimal_places=0, default=0)

    trust        = models.BooleanField('پرداخت اعتباری', default=False)
    trust_days   = models.DecimalField('حداکثر مهلت پرداخت اعتباری', max_digits=2, decimal_places=0, default=0)

    def __str__(self):
        return self.vendor.name



class VendorProduct(models.Model):
    vendor          = models.ForeignKey(Vendor, related_name="vendor_products", on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, related_name='vendor_products', on_delete=models.CASCADE)
    slug            = models.SlugField(max_length=55, null=True, unique=True)

    brand           = models.ForeignKey(Brand, related_name="vendor_products", on_delete=models.CASCADE, null=True)
    sub_brand        = models.ForeignKey(SubBrand, related_name="vendor_products", on_delete=models.CASCADE, null=True)
    category        = models.ForeignKey(Category, related_name='vendor_products', on_delete=models.CASCADE, null=True)
    subcategory     = models.ForeignKey(SubCategory, related_name='vendor_products', on_delete=models.CASCADE, null=True)
    date_added      = jmodels.jDateField(' تاریخ ثبت کالا ', default=now)

    # قیمت گذاری
    manufacturer_price  = models.DecimalField('قیمت تولید کننده', max_digits=8, decimal_places=0, null=True)
    consumer_price      = models.DecimalField('قیمت مصرف کننده', max_digits=8, decimal_places=0, null=True)
    price               = models.DecimalField('قیمت توزیع', max_digits=8, decimal_places=0)

    total_number        = models.DecimalField('تعداد در واحد عمده ', max_digits=3, decimal_places=0)
    weight              = models.DecimalField(' وزن خرد کالا بر حسب گرم ', max_digits=5, decimal_places=0, null=True)

    expire_date         = models.DateField('تاریخ انقضای کالا', null=True)
    exist               = models.BooleanField(' موجود ', default=True)

    def __str__(self):
        return self.product.title


class Discount(models.Model):
    vendor          = models.ForeignKey(Vendor, related_name='discount', on_delete=models.CASCADE, null=True)
    product         = models.ForeignKey(VendorProduct, related_name='discount', on_delete=models.CASCADE)
    date_added      = jmodels.jDateField(' تاریخ ثبت تخفیف ', default=now)

    # تاریخ انقضای تخفیف
    expire          = jmodels.jDateField('تا تاریخ')

    # تخفیف پله اول
    step_one_number     = models.DecimalField(' بیشتر از ', max_digits=2, decimal_places=0)
    step_one_percent    = models.DecimalField(' درصد تخفیف اول ', max_digits=2, decimal_places=0)

    # تخفیف پله دوم
    step_two_number     = models.DecimalField(' بیشتر از ', max_digits=2, decimal_places=0)
    step_two_percent    = models.DecimalField(' درصد تخفیف دوم ', max_digits=2, decimal_places=0)

    def __str__(self):
        return self.product.product.title


