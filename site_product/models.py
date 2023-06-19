import os

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from site_account.models import User

from django.db.models.signals import post_delete
from django.dispatch import receiver






def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{get_random_string(30)}-{instance.id}{ext}"
    return f"images/products/{final_name}"


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True)
    url_title = models.CharField(max_length=300, db_index=True)
    is_active = models.BooleanField(verbose_name='Active')

    def __str__(self):
        return f'{self.title} - {self.url_title}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.url_title])


class ProductSubCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True)
    url_title = models.CharField(max_length=300, db_index=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)

    is_active = models.BooleanField(verbose_name='Active')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'

    def get_absolute_url(self):
        return reverse('product_list_by_subcategory', args=[self.category.url_title, self.url_title])


class ProductType(models.Model):
    title = models.CharField(max_length=300, db_index=True)
    url_title = models.CharField(max_length=300, db_index=True)
    subcategory = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, blank=True, null=True, )
    is_active = models.BooleanField(verbose_name='Active')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

    def get_absolute_url(self):
        return reverse('product_list_by_type',
                       args=[self.subcategory.category.url_title, self.subcategory.url_title, self.url_title])


class ProductManager(models.Manager):
    def search(self, query):
        lookup = Q(title_ir__icontains=query) | Q(title_en__icontains=query) | Q(

            description__icontains=query) | Q(
            subcategory__title__icontains=query) | Q(

            type__title__icontains=query) | Q(
            category__title__icontains=query) | Q(
            subcategory__url_title__icontains=query) | Q(

            category__url_title__icontains=query) | Q(
            type__url_title__icontains=query)
        return self.get_queryset().filter(lookup).distinct()


# Weight
class Weight(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Product(models.Model):
    image = models.ImageField(upload_to=upload_gallery_image_path, default='images/products/default_product.png',
                              null=True,
                              blank=True)
    title_ir = models.CharField(max_length=300)
    title_en = models.CharField(max_length=300)
    stock = models.IntegerField(default=0)
    quantity = models.BooleanField(default=True)
    suggested = models.BooleanField(default=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, db_index=True, unique=True, default="", max_length=300)
    rkc = models.IntegerField(blank=True, null=True, unique=True)
    create_date = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
    last_update = models.DateField(auto_now=True)
    is_delete = models.BooleanField(null=True, blank=True, default=False)
    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if self.rkc is None:
            self.rkc = Product.objects.all().count() + 1000

        self.slug = slugify(self.title_en)
        if self.stock <= 0:
            self.quantity = False
            self.stock = 0
        if self.stock != 0:
            self.quantity = True
        # users = User.objects.filter(order__orderdetail__product_id__exact=self.id, order__is_paid=False).all()
        #
        # if self.stock == 0:
        #     for user in users:
        #         for order in user.order_set.filter(orderdetail__product_id=self.id, is_paid=False).all():
        #             detail = order.orderdetail_set.first()
        #             detail.delete()
        # if users is not None:
        #     if self.stock != 0:
        #         for user in users:
        #             if user:
        #                 for order in user.order_set.filter(orderdetail__product_id=self.id, is_paid=False):
        #                     if order:
        #                         for detail in order.orderdetail_set.all():
        #
        #                             if detail.count:
        #                                 if detail.count > self.stock:
        #                                     detail.count = self.stock
        #                                     detail.save()

        users = User.objects.filter(order__orderdetail__product_id__exact=self.id, order__is_paid=False).all()
        if self.stock == 0:
            for user in users:
                for order in user.order_set.filter(orderdetail__product_id=self.id, is_paid=False):
                    order.orderdetail_set.first().delete()
        elif self.stock != 0:
            for user in users:
                for order in user.order_set.filter(orderdetail__product_id=self.id, is_paid=False):
                    for detail in order.orderdetail_set.all():
                        detail.count = min(detail.count, self.stock)
                        detail.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_ir

@receiver(post_delete, sender=Product)
def order_delete_handler(sender, **kwargs):
    product = kwargs['instance']
    print(f"product with id {product.id} has been deleted.")



# Product Attribute
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.ForeignKey(Weight, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    special_price = models.PositiveIntegerField(null=True, blank=True)
    final_price = models.PositiveIntegerField(default=0, null=True, blank=True, editable=False)
    special_price_percent = models.PositiveIntegerField(null=True, blank=True, editable=False)

    is_quantity = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title_ir

    def save(self, *args, **kwargs):
        if self.special_price is not None:
            decreaseValue = self.price - self.special_price
            self.special_price_percent = decreaseValue / self.price * 100

            self.final_price = self.special_price
        else:

            self.special_price_percent = None
            self.final_price = self.price

        super().save(*args, **kwargs)


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    ip = models.CharField(max_length=30, verbose_name='user ip')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title_en} / {self.ip}'

    class Meta:
        verbose_name = 'product visit'
        verbose_name_plural = 'product visit'


class ProductProperty(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    property = models.CharField(max_length=200, null=True, blank=True)
    value = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.property


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    suggest = models.CharField(max_length=30, null=True, blank=True)
    score = models.CharField(max_length=10, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    accept_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class UserFavoriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class UserRecentVisitedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} {self.product.title_ir}"
