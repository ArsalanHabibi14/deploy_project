from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from site_home.sitemaps import ProductSitemap, BlogSitemap, StaticViewSitemap, ProductCategorySitemap, \
    ProductSubCategorySitemap

sitemaps = {
    'static': StaticViewSitemap,
    'productscategory': ProductCategorySitemap,
    'productssubcategory': ProductSubCategorySitemap,
    'products': ProductSitemap,
    'blogs': BlogSitemap,
}

urlpatterns = [
    # path('api/', include('api.urls')),
    path('', include('site_home.urls')),
    path('', include('site_account.urls')),

    path('panel/', include('site_userpanel.urls')),

    path('products/', include('site_product.urls')),
    path('order/', include('site_order.urls')),
    path('blog/', include('site_blog.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('robots.txt', include('robots.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('api-auth/', include('rest_framework.urls')),
    path('adminstrator/', include('site_admin.urls')),

    path('admin/', admin.site.urls),
]
handler404 = 'site_home.views.handle_404_error'

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
