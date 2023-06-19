from django.contrib import admin
from . import models


class SiteMainSliders(admin.StackedInline):
    model = models.SiteMainSliders
    extra = 0

class SiteMainBanners(admin.StackedInline):
    model = models.MainBanners
    extra = 0
class SiteBlogBanners(admin.StackedInline):
    model = models.BlogBanners
    extra = 0

class SiteSettingAdmin(admin.ModelAdmin):
    inlines = [SiteMainSliders,SiteMainBanners,SiteBlogBanners]

admin.site.register(models.SiteSetting, SiteSettingAdmin)








class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ['title','url','position']

