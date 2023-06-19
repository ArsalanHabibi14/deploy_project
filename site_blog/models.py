from django.db import models
from django.db.models import Q

from django.urls import reverse
from site_account.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
import os
from django.utils.crypto import get_random_string



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_gallery_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{get_random_string(30)}-{instance.id}{ext}"
    return f"images/blog/{final_name}"

class Blog(models.Model):
    image = models.ImageField(upload_to=upload_gallery_image_path)
    title_ir = models.CharField(max_length=300)
    title_en = models.CharField(max_length=300)
    short_description = RichTextUploadingField(blank=True,null=True)
    description = RichTextUploadingField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,editable=False)
    slug = models.SlugField(max_length=400,db_index=True,allow_unicode=True,null=True, blank=True,unique=True)
    create_date = models.DateTimeField(auto_now_add=True,editable=False)


    def __str__(self):
        return self.title_ir
    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    parent = models.ForeignKey('BlogComment',null=True,blank=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    accept_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class BlogVisit(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    ip = models.CharField(max_length=30, verbose_name='user ip')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.blog.title_en} / {self.ip}'

