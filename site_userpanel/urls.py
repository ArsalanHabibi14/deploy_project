
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.UserPanelDashboardPage.as_view(), name='userpanel_dashboard'),

    path('use-coupon/', views.use_coupon, name='use_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),

    path('wholesales', views.UserWholeSales.as_view(), name='userpanel_wholesales'),

    path('refund-request/', views.refund_request, name='refunud_request'),
    path('check-status/', views.check_status, name='check_status'),

    path('verify-phone/', views.verify_phone, name='userpanel_verify_phone'),
    path('set-phone/', views.set_phone, name='userpanel_set_phone'),
    path('confirm-phone/', views.confirm_phone, name='userpanel_confirm_phone'),

    path('verify-email/', views.verify_email, name='userpanel_verify_email'),
    path('set-email/', views.set_email, name='userpanel_set_email'),
    path('confirm-email/', views.confirm_email, name='userpanel_confirm_email'),

    path('edit-profile/', views.EditUserProfilePage.as_view(), name='userpanel_edit_profile'),

    path('contacts/', views.UserContacts.as_view(), name='userpanel_contacts'),

    path('orders/', views.UserOrders.as_view(), name='userpanel_orders'),
    path('orders/<slug>/', views.UserOrdersDetail.as_view(), name='userpanel_orders_detail'),

    path('recents/', views.UserRecents.as_view(), name='userpanel_recents'),

    path('bookmarks/', views.UserBookmarks.as_view(), name='userpanel_bookmarks'),
    path('bookmarks/add', views.add_to_bookmarks, name='userpanel_add_to_bookmarks'),
    path('bookmarks/remove-all', views.remove_all_bookmarks, name='userpanel_remove_all_bookmarks'),

    path('addresses/', views.UserAddresses.as_view(), name='userpanel_addresses'),
    path('addresses/remove-address', views.remove_address, name='userpanel_remove_addresses'),

    path('addresses/set-address-main', views.set_address_main, name='userpanel_set_addresses_main'),

    path('addresses/edit-address', views.edit_address, name='userpanel_edit_addresses'),
    path('addresses/edit-address-info', views.edit_address_info, name='userpanel_edit_addresses_info'),
    path('addresses/add-new-address', views.add_new_address, name='userpanel_add_new_addresses'),
    path('addresses/check-user-addresses-count', views.check_user_addresses_count, name='userpanel_check_user_addresses_count'),


    path('edit-password/', views.EditPasswordPage.as_view(), name='userpanel_edit_password'),
    path('set-password/', views.SetPasswordPage.as_view(), name='userpanel_set_password'),


    path('basket/', views.user_basket,name='user_basket_page'),
    path('basket/check-out/', views.user_checkout,name='user_checkout_page'),

    path('remove-order-detail/', views.remove_order_detail,name='remove-order-retail-ajax'),
    path('change-order-detail/', views.change_order_detail_count,name='change_order_detail_count_ajax'),
]

