# Generated by Django 4.1 on 2022-08-13 14:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=55, null=True, unique=True)),
                ('date_added', django_jalali.db.models.jDateField(default=django.utils.timezone.now, verbose_name=' تاریخ ثبت کالا ')),
                ('manufacturer_price', models.DecimalField(decimal_places=0, max_digits=8, null=True, verbose_name='قیمت تولید کننده')),
                ('consumer_price', models.DecimalField(decimal_places=0, max_digits=8, null=True, verbose_name='قیمت مصرف کننده')),
                ('price', models.DecimalField(decimal_places=0, max_digits=8, verbose_name='قیمت توزیع')),
                ('total_number', models.DecimalField(decimal_places=0, max_digits=3, verbose_name='تعداد در واحد عمده ')),
                ('weight', models.DecimalField(decimal_places=0, max_digits=5, null=True, verbose_name=' وزن خرد کالا بر حسب گرم ')),
                ('expire_date', models.DateField(null=True, verbose_name='تاریخ انقضای کالا')),
                ('exist', models.BooleanField(default=True, verbose_name=' موجود ')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_products', to='product.brand')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_products', to='product.category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_products', to='product.product')),
                ('sub_brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_products', to='product.subbrand')),
                ('subcategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_products', to='product.subcategory')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_products', to='vendor.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', django_jalali.db.models.jDateField(default=django.utils.timezone.now, verbose_name=' تاریخ ثبت تخفیف ')),
                ('expire', django_jalali.db.models.jDateField(verbose_name='تا تاریخ')),
                ('step_one_number', models.DecimalField(decimal_places=0, max_digits=2, verbose_name=' بیشتر از ')),
                ('step_one_percent', models.DecimalField(decimal_places=0, max_digits=2, verbose_name=' درصد تخفیف اول ')),
                ('step_two_number', models.DecimalField(decimal_places=0, max_digits=2, verbose_name=' بیشتر از ')),
                ('step_two_percent', models.DecimalField(decimal_places=0, max_digits=2, verbose_name=' درصد تخفیف دوم ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount', to='vendor.vendorproduct')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discount', to='vendor.vendor')),
            ],
        ),
    ]