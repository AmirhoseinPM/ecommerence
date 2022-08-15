from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_jalali.db import models as jmodels

def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image():
    return 'defaults/default_profileimage.png'

# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_user(self, email, phone, password=None):
        if not email:
            raise ValueError(' لطفا ایمیل خود را وارد نمایید')
        if not phone:
            raise ValueError('لطفا شماره تماس خود را وارد نمایید')
        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            phone=phone,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class City(models.Model):
    code = models.PositiveSmallIntegerField('کد شهر', unique=True)
    name = models.CharField('نام شهر', unique=True, blank=True, null=False, max_length=20)

    def __str__(self):
        return self.name


class Region(models.Model):
    code = models.PositiveSmallIntegerField('کد منطقه', unique=True)
    name = models.CharField('نام منطقه', max_length=60, blank=True, default='')
    city = models.ForeignKey(City, verbose_name='شهر', null=True, related_name='region', on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Account(AbstractBaseUser):

    email               = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    username            = models.CharField(verbose_name='نام کاربری', max_length=30, unique=True, blank=True, null=True)
    date_joined         = jmodels.jDateField(verbose_name='Date joined', auto_now_add=True)
    last_login          = jmodels.jDateTimeField(verbose_name='Last Login', auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_vendor           = models.BooleanField('نماینده توزیع', default=False)
    is_retailer         = models.BooleanField('فروشگاه', default=False)
    profile_image       = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email          = models.BooleanField(default=True)

    phone               = models.CharField(' شماره تماس ', max_length=20,  blank=False, unique=True)  # شماره همراه اصلی

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'username']

    # خروجی شی
    def __str__(self):
        return self.username

    # استعلام ادمین بودن
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image.index('profile_images/{self.pk}/')):]

