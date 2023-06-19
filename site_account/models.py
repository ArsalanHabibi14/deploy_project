from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from random import randint
import os
from django.utils.crypto import get_random_string


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{get_random_string(30)}-{instance.id}{ext}"
    return f"images/profile/{final_name}"


class User(AbstractUser):
    avatar = models.ImageField(upload_to=upload_gallery_image_path, default='images/profile/default_profile.png')
    phone = models.CharField(max_length=11, null=True, blank=True, unique=True)
    national_code = models.CharField(max_length=10, null=True, blank=True)
    home_phone = models.CharField(max_length=10, null=True, blank=True, unique=True)
    s = RegexValidator

    is_premium = models.BooleanField(default=False)

    email_otp = models.CharField(max_length=5, blank=True, null=True, default="")

    phone_otp = models.CharField(max_length=5, blank=True, null=True, default="")

    email_reset_otp = models.CharField(max_length=5, blank=True, null=True, default="")
    phone_reset_otp = models.CharField(max_length=5, blank=True, null=True, default="")

    refsystem = models.IntegerField(default=0)

    def save(self, *args, **kwargs):

        if self.email_otp is None:
            self.email_otp = randint(10000, 99999)

        if self.phone_otp is None:
            self.phone_otp = randint(10000, 99999)

        if self.email_reset_otp is None:
            self.email_reset_otp = randint(10000, 99999)

        if self.phone_reset_otp is None:
            self.phone_reset_otp = randint(10000, 99999)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class UserAddresses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_main = models.BooleanField(blank=True, null=True, default=False)
    receiver_name = models.CharField(max_length=100, blank=True, null=True)
    receiver_phone = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} {self.province} {self.city}"
