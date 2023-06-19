from django.db import models
from site_account.models import User


class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    is_read_by_admin = models.BooleanField(default=False)
    add_to_user_notify = models.BooleanField(default=False,null=True,blank=True)
    admin_answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if self.admin_answer:
            self.is_read_by_admin = True

        super().save(*args, **kwargs)

class SignEmails(models.Model):
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.email



class WholeSale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    company = models.CharField(max_length=50, null=True, blank=True)

    rice = models.CharField(max_length=50)
    STATUS_CHOICE = (
        ('canceled', 'لغو شده'),
        ('pending', 'در انتظار تایید'),
        ('accepted', 'تایید شده'),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICE,default="pending")
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    amount = models.IntegerField()
    description = models.TextField(null=True,blank=True)
    add_to_user_notify = models.BooleanField(default=False,null=True,blank=True)
    admin_answer = models.TextField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.admin_answer:
            self.is_read_by_user = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.rice
