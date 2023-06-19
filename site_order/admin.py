from django.contrib import admin
from . import models


class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']

admin.site.register(models.Order,OrderAdmin)
admin.site.register(models.OrderDetail)
