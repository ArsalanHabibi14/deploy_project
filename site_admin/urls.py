from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns= [
    path('dashboard/',views.Dashboard.as_view(),name='admin_dashboard'),

    #Setting
    path('setting/', views.SiteSettingListView.as_view(), name='admin_setting_list'),
    path('setting/edit/<pk>/', views.SiteSettingEditView.as_view(), name='admin_setting_edit'),

    #products
    path('products/',views.ProductListView.as_view(),name='admin_productlist'),
    path('products/add/',views.ProductCreateView.as_view(),name='admin_addproduct'),
    path('products/edit/<pk>/',views.ProductEditView.as_view(),name='admin_editproduct'),
    path('products/delete/<pk>/',views.ProductDeleteView.as_view(),name='admin_deleteproduct'),
    path('products/search-expenses/',csrf_exempt(views.product_search),name='admin_searchproduct'),

    #blogs
    path('blogs/',views.BlogListView.as_view(),name='admin_bloglist'),
    path('blogs/add/',views.BlogCreateView.as_view(),name='admin_addblog'),
    path('blogs/edit/<pk>/',views.BlogEditView.as_view(),name='admin_editblog'),
    path('blogs/delete/<pk>/',views.BlogDeleteView.as_view(),name='admin_deleteblog'),
    path('blogs/search/', views.SearchBlogView.as_view(), name='admin_searchblog'),

    #comments
    path('product/comments/', views.ProductCommentListView.as_view(), name='admin_product_comment_list'),
    path('product/comments/edit/<pk>/', views.ProductCommentEditView.as_view(), name='admin_product_comment_edit'),
    path('product/comments/delete/<pk>/', views.ProductCommentDeleteView.as_view(), name='admin_product_comment_delete'),

    path('blog/comments/', views.BlogCommentListView.as_view(), name='admin_blog_comment_list'),
    path('blog/comments/edit/<pk>/', views.BlogCommentEditView.as_view(), name='admin_blog_comment_edit'),
    path('blog/comments/delete/<pk>/', views.BlogCommentDeleteView.as_view(), name='admin_blog_comment_delete'),

    #users
    path('users/',views.UserListVeiw.as_view(),name='admin_userlist'),
    path('users/add/',views.UserCreateView.as_view(),name='admin_adduser'),
    path('users/edit/<pk>',views.UserEditView.as_view(),name='admin_edituser'),
    path('users/delete/<pk>',views.UserDeleteView.as_view(),name='admin_deleteuser'),
    path('users/search/', views.SearchUserView.as_view(), name='admin_searchuser'),

    #orders
    path('orders/',views.OrderListVeiw.as_view(),name='admin_orderlist'),
    path('orders/add/',views.OrderCreateView.as_view(),name='admin_addorder'),
    path('orders/edit/<pk>/',views.OrderEditView.as_view(),name='admin_editorder'),
    path('orders/search/', views.SearchOrderView.as_view(), name='admin_searchorder'),

    # Refunds
    path('refunds/', views.RefundsListVeiw.as_view(), name='admin_refundslist'),
    path('refunds/edit/<pk>/', views.RefundsEditView.as_view(), name='admin_editrefunds'),
    path('refunds/delete/<pk>/', views.RefundsDeleteView.as_view(), name='admin_deleterefunds'),

    #Contacts
    path('contacts/',views.ContactListVeiw.as_view(),name='admin_contactslist'),
    path('contacts/edit/<pk>/',views.ContactEditView.as_view(),name='admin_editcontacts'),
    path('contacts/delete/<pk>/',views.ContactDeleteView.as_view(),name='admin_deletecontacts'),

    # Wholesales
    path('wholesales/', views.WholesaleListVeiw.as_view(), name='admin_wholesaleslist'),
    path('wholesales/edit/<pk>/', views.WholesaleEditView.as_view(), name='admin_editwholesales'),
    path('wholesales/delete/<pk>/', views.WholesaleDeleteView.as_view(), name='admin_deletewholesales'),
    path('wholesales/search/', views.SearchWholesaleView.as_view(), name='admin_searchwholesale'),

]