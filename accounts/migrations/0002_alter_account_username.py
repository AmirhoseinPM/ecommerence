# Generated by Django 4.1 on 2022-08-13 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='نام کاربری'),
        ),
    ]