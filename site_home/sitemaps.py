from django.contrib.sitemaps import Sitemap
from site_product.models import Product, ProductCategory, ProductSubCategory, ProductType
from site_blog.models import Blog
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "always"

    def items(self):
        return ['home_page', 'about_page', 'wholesale_page', 'contact_page', 'faq_page', 'blog_list']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Product.objects.all()


class ProductCategorySitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return ProductCategory.objects.all()


class ProductSubCategorySitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return ProductSubCategory.objects.all()



class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Blog.objects.all()
