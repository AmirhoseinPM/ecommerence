from django.db import models
from accounts.models import Account, City, Region


# Create your models here.
class Retailer(models.Model):
    user         = models.OneToOneField(Account, related_name='retailer', on_delete=models.CASCADE, primary_key=True)  # فیلدهای عمومی
    # other fields
    name = models.CharField('نام', max_length=255, blank=True)
    slug = models.SlugField(max_length=55, null=True, unique=True)

    city         = models.ForeignKey(City, null=True, verbose_name='شهر', related_name='retailer', on_delete=models.CASCADE)
    eco_num      = models.CharField(' کد اقتصادی ', max_length=12, blank=False, unique=True)  # شماره اقتصادی
    post_code    = models.CharField(' کد پستی ', default='', max_length=10, blank=False)  # کد پستی
    region       = models.ForeignKey(Region, null=True, verbose_name='منطقه', related_name='retailer', on_delete=models.CASCADE)  # منطقه
    full_add     = models.CharField(' آدرس کامل ', default='', max_length=150, null=True, blank=True)  # آدرس کامل


    manager_name = models.CharField('نام مدیر', default='', blank=True, max_length=30)
    manager_phone = models.CharField(' شماره مدیر', default='', max_length=20, blank=False)

    def __str__(self):
        return self.name
