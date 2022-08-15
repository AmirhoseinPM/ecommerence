from django.db import models

# Create your models here.
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField('نام دسته', max_length=60)
    ordering = models.IntegerField(default=0)
    slug = models.SlugField(max_length=55, null=True, unique=True)
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='category/', blank=True, null=True) # Change uploads to thumbnails


    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url

            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'

    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategory', on_delete=models.CASCADE, null=True)
    title = models.CharField('نام زیردسته', max_length=60)
    slug = models.SlugField(max_length=55, null=True, unique=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True) # Change uploads to thumbnails


    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url

            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'

    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Brand(models.Model):
    title = models.CharField('نام برند', max_length=60)
    ordering = models.IntegerField(default=0)
    slug = models.SlugField(max_length=55, null=True, unique=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True) # Change uploads to thumbnails

    def __str__(self):
        return self.title


    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url

            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'

    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class SubBrand(models.Model):
    brand = models.ForeignKey(Brand, related_name='subbrand', on_delete=models.CASCADE, null=True)
    title = models.CharField('نام مدل', max_length=60)
    slug = models.SlugField(max_length=55, null=True, unique=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)  # Change uploads to thumbnails


    class Meta:
        ordering = ['slug']

    def __str__(self):
        return self.title

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url

            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'

    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE, null=True)
    brand = models.ForeignKey(Brand, related_name="products", on_delete=models.CASCADE)
    sub_brand = models.ForeignKey(SubBrand, related_name='products', on_delete=models.CASCADE, null=True)
    title = models.CharField('نام کالا', max_length=60)
    slug = models.SlugField(max_length=55, null=True, unique=True)

    kg_retail_unit = models.BooleanField('واحد خرد کالا کیلوگرم', default=False)
    packet_retail_unit = models.BooleanField('واحد خرد کالا عدد', default=True)
    description = models.TextField('توضیحات', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True) # Change uploads to thumbnails

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title


    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url

            else:
                # Default Image
                return 'https://via.placeholder.com/240x180.jpg'

    # Generating Thumbnail - Thumbnail is created when get_thumbnail is called
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
