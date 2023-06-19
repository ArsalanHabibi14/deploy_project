from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView

from site_account.models import User
from site_blog.models import Blog, BlogComment
from site_form.models import ContactUs, WholeSale
from site_order.models import Order, OrderDetail
from site_product.models import Product, ProductComment
from site_setting.models import SiteVisit, SiteSetting, SiteMainSliders
from utils.my_decorators import permission_checker_decorator_factory
import json
from django.http import JsonResponse
from extra_views import CreateWithInlinesView, InlineFormSetView, UpdateWithInlinesView, InlineFormSetFactory, \
    FormSetSuccessMessageMixin




def admin_sidebar_component(request):
    not_read_contacts_count = ContactUs.objects.filter(is_read_by_admin=False).count()
    pending_wholesale_requests_count = WholeSale.objects.filter(status='pending').count()

    forms_notifications = not_read_contacts_count + pending_wholesale_requests_count

    pending_orders_count = Order.objects.filter(status='pending').count()
    pending_refunds_count = OrderDetail.objects.filter(refundstatus='requested').count()
    orders_notification = pending_orders_count + pending_refunds_count
    pending_products_comment_count = ProductComment.objects.filter(accept_by_admin=False).count()
    pending_blogs_comment_count =     BlogComment.objects.filter(accept_by_admin=False).count()

    comments_notification = pending_products_comment_count + pending_blogs_comment_count
    setting = SiteSetting.objects.filter(is_main=True).first()

    context = {
        # orders
        'pending_orders_count': pending_orders_count,
        'pending_refunds_count': pending_refunds_count,
        'orders_notification': orders_notification,
        # forms
        'not_read_contacts_count': not_read_contacts_count,
        'pending_wholesale_requests_count': pending_wholesale_requests_count,
        'forms_notifications': forms_notifications,
        # comments
        'pending_products_comment_count': pending_products_comment_count,
        'pending_blogs_comment_count': pending_blogs_comment_count,
        'comments_notification': comments_notification,
        'setting': setting,

    }
    return render(request, 'site_admin/shared/admin_sidebar.html', context)


def admin_header_component(request):
    not_read_contacts_count = ContactUs.objects.filter(is_read_by_admin=False).count()
    pending_orders_count = Order.objects.filter(status='pending').count()
    pending_refunds_count = OrderDetail.objects.filter(refundstatus='requested').count()
    notifications = pending_refunds_count + pending_orders_count + not_read_contacts_count
    setting = SiteSetting.objects.filter(is_main=True).first()
    context = {
        'notifications': notifications,
        'not_read_contacts_count': not_read_contacts_count,
        'pending_orders_count': pending_orders_count,
        'pending_refunds_count': pending_refunds_count,
        'setting': setting,

    }
    return render(request, 'site_admin/shared/admin_header.html', context)


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class Dashboard(TemplateView):
    template_name = 'site_admin/dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(is_paid=True)
        ordersprofit = Order.objects.filter(is_paid=True).all()

        profit = 0
        for buy in ordersprofit:
            profit += buy.calculate_total_price()

        context['userscount'] = User.objects.all().count()
        context['orders'] = orders
        context['profit'] = profit
        context['visit'] = SiteVisit.objects.all().count()

        return context


# site Setting
@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class SiteSettingListView(ListView):
    model = SiteSetting
    template_name = 'site_admin/setting/site_setting_list.html'


class SettingItemInline(InlineFormSetFactory):
    model = SiteMainSliders
    fields = ['image', 'url_title', 'title']


class SiteSettingEditView(SuccessMessageMixin, UpdateWithInlinesView):
    model = SiteSetting
    inlines = [SettingItemInline, ]
    fields = "__all__"
    success_message = 'اضافه شد'
    template_name = 'site_admin/setting/site_setting_edit.html'
    success_url = '/admin/setting/'


# @method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
# class SiteSettingEditView(SuccessMessageMixin, UpdateView):
#     model = SiteSetting
#     template_name = 'site_admin/setting/site_setting_edit.html'
#
#     fields = '__all__'
#     success_message = 'اضافه شد'
#
#     success_url = reverse_lazy('admin_productlist')


# products section
@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'site_admin/products/products_list.html'
    paginate_by = 20


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ProductEditView(SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'site_admin/products/products_edit.html'

    fields = 'image', 'title_ir', 'title_en', 'stock', 'suggested', 'category', 'subcategory', 'type', 'description', 'is_active'
    success_message = 'ذخیره شد'
    success_url = reverse_lazy('admin_productlist')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ProductCreateView(SuccessMessageMixin, CreateView):
    model = Product
    template_name = 'site_admin/products/products_add.html'

    fields =  'image', 'title_ir', 'title_en', 'stock', 'suggested', 'category', 'subcategory', 'type', 'description', 'is_active'
    success_message = 'اضافه شد'

    success_url = reverse_lazy('admin_productlist')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ProductDeleteView(SuccessMessageMixin, DeleteView):
    model = Product
    success_message = 'حذف شد'

    success_url = reverse_lazy('admin_productlist')
    template_name = 'site_admin/shared/delete.html'


def product_search(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Product.objects.filter(title_ir__icontains=search_str) | Product.objects.filter(
            title_en__icontains=search_str)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


# blog section
@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class BlogListView(ListView):
    model = Blog
    template_name = 'site_admin/blogs/blogs_list.html'
    paginate_by = 20


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class BlogEditView(SuccessMessageMixin, UpdateView):
    model = Blog
    template_name = 'site_admin/blogs/blogs_edit.html'

    fields = 'image', 'title_ir', 'title_en', 'short_description', 'description', 'is_active'
    success_message = 'ذخیره شد'

    success_url = reverse_lazy('admin_bloglist')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class BlogCreateView(SuccessMessageMixin, CreateView):
    model = Blog
    template_name = 'site_admin/blogs/blogs_add.html'
    success_message = 'اضافه شد'

    fields = 'image', 'title_ir', 'title_en', 'short_description', 'description', 'is_active'

    success_url = reverse_lazy('admin_bloglist')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class BlogDeleteView(SuccessMessageMixin, DeleteView):
    model = Blog
    success_message = 'حذف شد'

    success_url = reverse_lazy('admin_bloglist')
    template_name = 'site_admin/shared/delete.html'


class SearchBlogView(ListView):
    template_name = 'site_admin/blogs/blogs_list.html'
    context_object_name = 'Blog'

    paginate_by = 20

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return Blog.objects.search(query)

        return Blog.objects.filter()


# comments section
@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ProductCommentListView(ListView):
    model = ProductComment
    template_name = 'site_admin/comments/product_comment_list.html'
    paginate_by = 20

    def get_queryset(self):
        query = super(ProductCommentListView, self).get_queryset()
        data = query.all().order_by('accept_by_admin')
        return data


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ProductCommentEditView(SuccessMessageMixin, UpdateView):
    model = ProductComment
    template_name = 'site_admin/comments/product_comment_Edit.html'

    fields = 'accept_by_admin', 'score', 'suggest', 'comment',
    success_message = 'ذخیره شد'

    success_url = reverse_lazy('admin_bloglist')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ProductCommentDeleteView(SuccessMessageMixin, DeleteView):
    model = ProductComment
    success_message = 'حذف شد'

    success_url = reverse_lazy('admin_product_comment_list')
    template_name = 'site_admin/shared/delete.html'


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class BlogCommentListView(ListView):
    model = BlogComment
    template_name = 'site_admin/comments/blog_commet_list.html'
    paginate_by = 20

    def get_queryset(self):
        query = super(BlogCommentListView, self).get_queryset()
        data = query.all().order_by('accept_by_admin')
        return data


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class BlogCommentEditView(SuccessMessageMixin, UpdateView):
    model = BlogComment
    template_name = 'site_admin/comments/blog_comment_edit.html'

    success_message = 'ذخیره شد'

    fields = 'accept_by_admin', 'comment',

    success_url = reverse_lazy('admin_blog_comment_list')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class BlogCommentDeleteView(SuccessMessageMixin, DeleteView):
    model = BlogComment
    success_message = 'حذف شد'

    success_url = reverse_lazy('admin_blog_comment_list')
    template_name = 'site_admin/shared/delete.html'


# users section
@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class UserListVeiw(ListView):
    model = User
    template_name = 'site_admin/users/users_list.html'
    paginate_by = 20


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class UserEditView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'site_admin/users/users_edit.html'
    fields = 'avatar', 'username', 'email', 'phone', 'password', 'is_superuser'
    success_message = 'ذخیره شد'

    success_url = reverse_lazy('admin_userlist')



@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'site_admin/users/users_add.html'
    fields = 'avatar', 'username', 'email', 'phone', 'password', 'is_superuser'
    success_message = 'اضافه شد'

    success_url = reverse_lazy('admin_userlist')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    success_message = 'حذف شد'

    success_url = reverse_lazy('admin_userlist')

    template_name = 'site_admin/shared/delete.html'


class SearchUserView(ListView):
    template_name = 'site_admin/users/users_list.html'
    context_object_name = 'User'

    paginate_by = 20

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return User.objects.filter(username__icontains=query) | User.objects.filter(
                first_name__icontains=query) | User.objects.filter(last_name__icontains=query) | User.objects.filter(
                phone__icontains=query)| User.objects.filter(email__icontains=query)| User.objects.filter(national_code__icontains=query)| User.objects.filter(home_phone__icontains=query)

        return User.objects.filter()


# orders section
@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class OrderListVeiw(ListView):
    model = Order
    template_name = 'site_admin/orders/orders_list.html'
    paginate_by = 20

    def get_queryset(self):
        query = super(OrderListVeiw, self).get_queryset()
        data = query.filter(is_paid=True)
        return data


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class OrderEditView(SuccessMessageMixin, UpdateView):
    model = Order
    template_name = 'site_admin/orders/orders_edit.html'
    fields = 'status',
    success_message = 'ذخیره شد'

    success_url = reverse_lazy('admin_orderlist')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class OrderCreateView(SuccessMessageMixin, CreateView):
    model = Order
    template_name = 'site_admin/users/users_add.html'
    fields = 'avatar', 'username', 'email', 'phone', 'password', 'is_superuser'
    success_message = 'اضافه شد'

    success_url = reverse_lazy('admin_orderlist')


class SearchOrderView(ListView):
    template_name = 'site_admin/orders/orders_list.html'
    context_object_name = 'Order'

    paginate_by = 20

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return Order.objects.search(query)

        return Order.objects.filter(is_paid=True)


# Contact Form section
@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ContactListVeiw(ListView):
    model = ContactUs
    template_name = 'site_admin/forms/contacts_list.html'
    paginate_by = 20

    def get_queryset(self):
        query = super(ContactListVeiw, self).get_queryset()
        data = query.all().order_by('is_read_by_admin')
        return data


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ContactEditView(SuccessMessageMixin, UpdateView):
    model = ContactUs
    template_name = 'site_admin/forms/contacts_edit.html'
    fields = 'subject', 'message', 'email', 'phone', 'is_read_by_admin', 'admin_answer', 'add_to_user_notify',
    success_message = 'ذخیره شد'

    success_url = reverse_lazy('admin_contactslist')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class ContactDeleteView(SuccessMessageMixin, DeleteView):
    model = ContactUs
    success_message = 'حذف شد'

    success_url = reverse_lazy('admin_contactslist')

    template_name = 'site_admin/shared/delete.html'


# Refund Requests section
@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class RefundsListVeiw(ListView):
    model = OrderDetail
    template_name = 'site_admin/orders/refunds_list.html'
    paginate_by = 20

    def get_queryset(self):
        query = super(RefundsListVeiw, self).get_queryset()
        data = query.filter(refundstatus='requested')
        return data


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class RefundsEditView(SuccessMessageMixin, UpdateView):
    model = OrderDetail
    template_name = 'site_admin/orders/refunds_edit.html'
    fields = 'refundstatus',
    success_message = 'ذخیره شد'

    success_url = reverse_lazy('admin_refundslist')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class RefundsDeleteView(SuccessMessageMixin, DeleteView):
    model = OrderDetail
    success_message = 'حذف شد'

    success_url = reverse_lazy('admin_refundslist')

    template_name = 'site_admin/shared/delete.html'


# class SearchRefundView(ListView):
#     template_name = 'site_admin/orders/refunds_list.html'
#     context_object_name = 'OrderDetail'
#
#     paginate_by = 20
#     def get_queryset(self):
#         request = self.request
#         query = request.GET.get('q')
#         if query is not None:
#             return OrderDetail.objects.filter()
#
#         return OrderDetail.objects.filter(refundstatus='requested')

# WholeSale Form section
@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class WholesaleListVeiw(ListView):
    model = WholeSale
    template_name = 'site_admin/forms/wholesale_list.html'
    paginate_by = 20


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class WholesaleEditView(SuccessMessageMixin, UpdateView):
    model = WholeSale
    template_name = 'site_admin/forms/wholesale_edit.html'
    fields = 'email', 'phone', 'company', 'rice', 'status', 'city', 'province', 'amount', 'description', 'admin_answer', 'add_to_user_notify',
    success_message = 'ذخیره شد'

    success_url = reverse_lazy('admin_wholesaleslist')


@method_decorator(permission_checker_decorator_factory({'permission_name': 'article_list'}), name='dispatch')
class WholesaleDeleteView(SuccessMessageMixin, DeleteView):
    model = WholeSale
    success_message = 'حذف شد'

    success_url = reverse_lazy('admin_wholesaleslist')

    template_name = 'site_admin/shared/delete.html'


class SearchWholesaleView(ListView):
    template_name = 'site_admin/forms/wholesale_list.html'
    context_object_name = 'WholeSale'

    paginate_by = 20

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return WholeSale.objects.filter(id=query)

        return WholeSale.objects.all()
