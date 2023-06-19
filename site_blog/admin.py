from django.contrib import admin
from django.http import HttpRequest

from . import models

# Register your models here.
from .models import Blog



class BlogAdmin(admin.ModelAdmin):
    list_display = ['title_ir', 'slug', 'is_active', 'author']
    list_editable = ['is_active']

    def save_model(self, request: HttpRequest, obj: Blog, form, change):
        if not change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'create_date', 'parent']


admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.BlogComment, ArticleCommentAdmin)
