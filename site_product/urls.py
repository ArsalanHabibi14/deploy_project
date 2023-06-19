from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.SearchProductView.as_view(), name='product_search'),

    path('filter-data/', views.filter_data, name='product_filter_data'),


    path('category/<category>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('category/<category>/<subcategory>/', views.ProductListView.as_view(), name='product_list_by_subcategory'),
    path('category/<category>/<subcategory>/<type>/', views.ProductListView.as_view(), name='product_list_by_type'),


    path('add-product-comment/', views.add_product_comment, name='add_product_comment'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),




    # API Section
    path('/', views.ProductDetailView.as_view(), name='product_detail'),


]
