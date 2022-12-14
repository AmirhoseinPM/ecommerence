# Generated by Django 4.1 on 2022-08-13 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='نام برند')),
                ('ordering', models.IntegerField(default=0)),
                ('slug', models.SlugField(max_length=55, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
            ],
            options={
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='نام دسته')),
                ('ordering', models.IntegerField(default=0)),
                ('slug', models.SlugField(max_length=55, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='category/')),
            ],
            options={
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='نام زیردسته')),
                ('slug', models.SlugField(max_length=55, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='product.category')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='SubBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='نام مدل')),
                ('slug', models.SlugField(max_length=55, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subbrand', to='product.brand')),
            ],
            options={
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60, verbose_name='نام کالا')),
                ('slug', models.SlugField(max_length=55, null=True, unique=True)),
                ('kg_retail_unit', models.BooleanField(default=False, verbose_name='واحد خرد کالا کیلوگرم')),
                ('packet_retail_unit', models.BooleanField(default=True, verbose_name='واحد خرد کالا عدد')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category')),
                ('sub_brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.subbrand')),
                ('subcategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.subcategory')),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
    ]
