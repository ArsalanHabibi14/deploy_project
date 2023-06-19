from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('search/', views.SearchBlogView.as_view(), name='blog_search'),

    path('add-blog-comment/', views.add_blog_comment, name='add_blog_comment'),

    path('<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
]
