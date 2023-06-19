from django.contrib import admin

from . import models

admin.site.register(models.ContactUs)
admin.site.register(models.WholeSale)

admin.site.register(models.SignEmails)