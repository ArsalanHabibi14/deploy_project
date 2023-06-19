from django.db import models
from django.db.models import Q
from django.urls import reverse

from site_account.models import User
from site_product.models import Product, ProductAttribute
from utils.phone_service import *
from coupon_management.models import Coupon
from coupon_management.validations import validate_coupon


class OrderManager(models.Manager):
    def search(self, query):
        lookup = Q(sku_id__icontains=query)
        return self.get_queryset().filter(lookup).distinct()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    coupon_code = models.CharField(max_length=20, blank=True, null=True)
    is_paid = models.BooleanField()
    slug = models.SlugField(db_index=True, null=True, blank=True, editable=False)
    sku_id = models.CharField(max_length=10, null=True, blank=True)
    STATUS_CHOICE = (
        ('canceled', 'لغو شده'),
        ('pending', 'در انتظار تایید'),
        ('processing', 'درحال پردازش'),
        ('sent', 'ارسال شد'),
        ('delivered', 'تحویل داده شده'),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, blank=True, null=True)
    payment_date = models.DateField(null=True, blank=True)
    user_receiver_name = models.CharField(max_length=100, null=True, blank=True)
    user_receiver_phone = models.CharField(max_length=11, null=True, blank=True)
    user_city = models.CharField(max_length=100, null=True, blank=True)
    user_province = models.CharField(max_length=100, null=True, blank=True)
    user_postalcode = models.CharField(max_length=100, null=True, blank=True)
    user_address = models.TextField(null=True, blank=True)
    objects = OrderManager()
    def __str__(self):
        return f"{self.sku_id}"

    def get_absolute_url(self):
        return reverse('userpanel_orders_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = self.sku_id
        paid_orders = Order.objects.filter(is_paid=True)

        if self.is_paid:
            if self.sku_id is None:
                self.sku_id = 1000 + paid_orders.count()

        if self.status == 'processing':
            OrderStatusService(to=self.user.phone, pattern='z0lefyrpe670s58', id=self.sku_id)

        if self.status == 'sent':
            OrderStatusService(to=self.user.phone, pattern='ygg1nm5hlhfi50c', id=self.sku_id)

        super().save(*args, **kwargs)

    def calculate_total_price(self):
        total_amount = 0

        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count

            if self.coupon_code is not None:
                status = validate_coupon(coupon_code=self.coupon_code, user=self.user)
                if status['valid'] or status['message'] == "Invalid coupon!":
                    coupon = Coupon.objects.get(code=self.coupon_code)
                    total_amount = int(coupon.get_discounted_value(initial_value=total_amount))
                else:
                    self.coupon_code = None
                    self.save()
        else:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.product_price * order_detail.count

            if self.coupon_code is not None:
                status = validate_coupon(coupon_code=self.coupon_code, user=self.user)
                if status['valid']:
                    coupon = Coupon.objects.get(code=self.coupon_code)
                    total_amount = int(coupon.get_discounted_value(initial_value=total_amount))
                else:
                    self.coupon_code = None
                    self.save()

        return total_amount

    def calculate_total_price_before_discount(self):
        total_amount = 0

        for order_detail in self.orderdetail_set.all():
            total_amount += order_detail.product_price * order_detail.count
        return total_amount

    def calculate_discount_price(self):
        total_amount = 0
        for order_detail in self.orderdetail_set.all():
            total_amount += order_detail.product_price * order_detail.count

        discount_price = total_amount - self.calculate_total_price()

        return discount_price


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    final_price = models.IntegerField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)
    STATUS_CHOICE = (
        ('notrequested', 'درخواست نشده'),
        ('requested', 'در انتظار تایید'),
        ('accepted', 'تایید شده'),
        ('notaccepted', 'درخواست رد شد'),
    )

    refundstatus = models.CharField(max_length=100, choices=STATUS_CHOICE, default='notrequested')
    product_price = models.IntegerField(null=True, blank=True)
    weight = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        the_price = ProductAttribute.objects.filter(product_id=self.product.id,
                                                    weight__title__iexact=self.weight).first()
        self.product_price = the_price.final_price

        super().save(*args, **kwargs)

    def get_total_price(self):
        return self.count * self.product_price

    def __str__(self):
        return f"{self.order.sku_id}"
