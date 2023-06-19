from django.contrib import admin
from . import models


# Product Attribute
class ProductVisitInline(admin.TabularInline):
    model = models.ProductVisit
    readonly_fields = ('ip', 'user')
    extra = 0

class WeightAdmin(admin.ModelAdmin):
    list_display = ['title', ]


admin.site.register(models.Weight, WeightAdmin)


class AttributeInLine(admin.StackedInline):
    model = models.ProductAttribute
    extra = 1


class PropertyInLine(admin.StackedInline):
    model = models.ProductProperty
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_filter = ['category', 'is_active']
    list_display = ['title_ir', 'stock', 'type', 'is_active', 'suggested']
    list_editable = ['stock', 'type', 'is_active', 'suggested']
    search_fields = ['title_ir', 'title_en']
    inlines = [AttributeInLine, PropertyInLine,ProductVisitInline]
    readonly_fields = ('visit_count',)
    def visit_count(self, obj):
        return obj.productvisit_set.count()
    visit_count.short_description = 'Visit Count'


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title']
    list_editable = ['url_title']


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'weight')


class ProductSubcategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_display_links = ('title',)


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductSubCategory, ProductSubcategoryModelAdmin)
admin.site.register(models.ProductType)
admin.site.register(models.ProductComment)

admin.site.register(models.ProductAttribute, ProductAttributeAdmin)
admin.site.register(models.UserRecentVisitedProduct)
