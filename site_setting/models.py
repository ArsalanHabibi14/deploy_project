from django.db import models

# Create your models here.
from site_account.models import User
from ckeditor.fields import RichTextField


class SiteSetting(models.Model):
    is_main = models.BooleanField(default=False)
    site_logo = models.ImageField(upload_to='images/logo', null=True, blank=True)
    site_icon = models.ImageField(upload_to='images/logo', null=True, blank=True)
    site_name = models.CharField(max_length=100, null=True, blank=True)
    site_title = models.CharField(max_length=200, null=True, blank=True)
    site_instagram = models.CharField(max_length=200, null=True, blank=True)
    site_twitter = models.CharField(max_length=200, null=True, blank=True)
    site_whatsapp = models.CharField(max_length=200, null=True, blank=True)
    site_phone = models.CharField(max_length=20, null=True, blank=True)
    site_email = models.CharField(max_length=50, null=True, blank=True)
    site_address = models.CharField(max_length=200, null=True, blank=True)
    site_short_about = RichTextField(blank=True, null=True)
    site_about = RichTextField(blank=True, null=True)
    site_copyright = models.CharField(max_length=100, null=True, blank=True)
    site_rules = RichTextField(blank=True, null=True)
    site_terms = RichTextField(blank=True, null=True)
    site_whyus = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.site_name


class SiteVisit(models.Model):
    ip = models.CharField(max_length=30, verbose_name='user ip')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip


class SiteMainSliders(models.Model):
    setting = models.ForeignKey(SiteSetting, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    url_title = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='images/sliders')

    def __str__(self):
        return self.title


class MainBanners(models.Model):
    setting = models.ForeignKey(SiteSetting, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    url_title = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='images/banners')

    def __str__(self):
        return self.title


class BlogBanners(models.Model):
    setting = models.ForeignKey(SiteSetting, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    url_title = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='images/banners')

    def __str__(self):
        return self.title
