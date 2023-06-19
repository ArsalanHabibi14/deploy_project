from django.contrib import messages
import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from site_form.models import ContactUs, WholeSale
from site_setting.models import SiteSetting
from .forms import EditPasswordForm, SetPasswordForm, EditProfileModelForm

from site_order.models import Order, OrderDetail
from site_product.models import Product, UserFavoriteProducts, ProductCategory, UserRecentVisitedProduct
from site_account.models import User
from site_account.models import UserAddresses as UserAddressesModel
from django.contrib.auth import logout, login
from django.utils.decorators import method_decorator
from random import randint
from utils.phone_service import OTPService, OrderStatusService
from utils.email_service import send_email
from django.forms import EmailField
from django.core.exceptions import ValidationError
from throttle.decorators import throttle

from coupon_management.validations import validate_coupon
from coupon_management.models import Coupon


@throttle(zone='use_coupon_delay')
@login_required
def use_coupon(request):
    coupon_code = request.GET.get("coupon_code")
    user = User.objects.get(id=request.user.id)

    if coupon_code != "":
        status = validate_coupon(coupon_code=coupon_code, user=user)
        if status['valid']:
            coupon = Coupon.objects.get(code=coupon_code)
            coupon.use_coupon(user=user)
            user_order = Order.objects.get(user_id=user.id, is_paid=False)
            user_order.coupon_code = coupon_code
            user_order.save()
            mainaddress = UserAddressesModel.objects.filter(user_id=request.user.id, is_main=True).first()
            current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                     user_id=request.user.id)
            total_amount = current_order.calculate_total_price
            total_amount_before_discount = current_order.calculate_total_price_before_discount

            user = User.objects.filter(id=request.user.id).first()
            context = {
                'theuser': user,
                'order': current_order,
                'sum': total_amount,
                'sum_before_discount': total_amount_before_discount,

                'mainaddress': mainaddress,
                'object_list': UserAddressesModel.objects.filter(user_id=request.user.id),
                'addresses_count': UserAddressesModel.objects.filter(user_id=request.user.id).all().count(),

            }

            return JsonResponse({
                'status': 'valid',
                "title": "کد تخفیف با موفقیت اعمال شد",
                'body': render_to_string('site_userpanel/content/user_basket_address_content.html', context),

            })

        if status['message'] == "Coupon does not exist!":
            return JsonResponse({
                "status": "not_valid",
                "title": "کد تخفیف وارد شده معتبر نمیباشد",
            })

        if status['message'] == "Invalid coupon!":
            return JsonResponse({
                "status": "not_valid",
                "title": "کد تخفیف وارد شده معتبر نمیباشد",
            })

        if status['message'] == "Invalid coupon for this user!":
            return JsonResponse({
                "status": "not_valid",
                "title": "کد تخفیف وارد شده برای شما مجاز نمیباشد",
            })

        if status['message'] == "Coupon uses exceeded for this user!":
            coupon = Coupon.objects.get(code=coupon_code)
            if coupon.ruleset.max_uses.uses_per_user == 1:
                return JsonResponse({
                    "status": "not_valid",
                    "title": f"کد تخفیف وارد شده تنها {coupon.ruleset.max_uses.uses_per_user} بار قابل استفاده میباشد",
                })
            else:
                return JsonResponse({
                    "status": "not_valid",
                    "title": f"کد تخفیف وارد شده فقط {coupon.ruleset.max_uses.uses_per_user} بار قابل استفاده میباشد",
                })
    else:
        return JsonResponse({
            "status": "empty",
            "title": "کد تخفیف خود را وارد کنید",
        })


@login_required
def remove_coupon(request):
    user = User.objects.get(id=request.user.id)
    the_order = Order.objects.get(user_id=user.id, is_paid=False)
    if the_order is not None:
        the_order.coupon_code = None
        the_order.save()

        mainaddress = UserAddressesModel.objects.filter(user_id=request.user.id, is_main=True).first()
        current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                 user_id=request.user.id)
        total_amount = current_order.calculate_total_price
        total_amount_before_discount = current_order.calculate_total_price_before_discount

        user = User.objects.filter(id=request.user.id).first()
        context = {
            'theuser': user,
            'order': current_order,
            'sum': total_amount,
            'sum_before_discount': total_amount_before_discount,

            'mainaddress': mainaddress,
            'object_list': UserAddressesModel.objects.filter(user_id=request.user.id),
            'addresses_count': UserAddressesModel.objects.filter(user_id=request.user.id).all().count(),

        }

        return JsonResponse({
            'status': 'success',
            "title": "کد تخفیف با موفقیت حذف شد",
            'body': render_to_string('site_userpanel/content/user_basket_address_content.html', context),

        })
    else:
        return JsonResponse({
            'status': 'error',
            "title": "درخواست شما با خطا مواجع شد",

        })


@method_decorator(login_required, name='dispatch')
class UserWholeSales(ListView):
    model = WholeSale
    paginate_by = 10
    template_name = 'site_userpanel/user_wholesales.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        queryset = queryset.filter(user_id=request.user.id).order_by('-id')
        return queryset


@login_required
def refund_request(request):
    detailid = request.GET.get('detailid')
    sku_id = request.GET.get('skuid')
    detail = OrderDetail.objects.filter(id=detailid, order__user_id=request.user.id).first()

    is_expired = datetime.date.today() - detail.order.payment_date

    if is_expired.days >= 10:
        return JsonResponse({
            'status': 'error',
            'icon': 'error',
            'title': '10 روز از خرید گذشته است',

        })

    elif detail.refundstatus == 'notrequested':
        detail.refundstatus = 'requested'
        detail.save()
        context = {
            'order': Order.objects.filter(user_id=request.user.id, is_paid=True, sku_id__iexact=sku_id).first(),
        }
        return JsonResponse({
            'status': 'success',
            'icon': 'success',
            'title': 'درخواست با موفقیت ثبت شد',
            'body': render_to_string('site_userpanel/content/user_refunds_content.html', context),

        })
    else:
        return JsonResponse({
            'status': 'error',
            'icon': 'error',
            'title': 'درخواست قبلا ثبت شده است',

        })


@throttle(zone='check_status_delay')
@login_required
def check_status(request):
    theuser = User.objects.filter(id=request.user.id).first()
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    the_user_addresses = UserAddressesModel.objects.filter(user_id=theuser.id).all()
    the_user_main_address = UserAddressesModel.objects.filter(user_id=theuser.id, is_main=True).first()
    if not theuser.phone:
        return JsonResponse({
            'status': 'no_phone_set',
            'title': 'شما شماره تلفنی ثبت نکرده اید لطفا به پنل کاربری خود رفته و اقدام به ثبت شماره تلفن نمایید',

        })
    if not the_user_addresses:
        return JsonResponse({
            'status': 'no_address_set',
            'title': 'شما آدرسی ثبت نکرده اید',

        })
    if the_user_main_address is None:
        return JsonResponse({
            'status': 'no_main_address_set',
            'title': 'شما آدرس پیش فرضی ثبت نکرده اید',

        })
    else:
        if current_order.calculate_total_price() > 0:
            return JsonResponse({
                'status': 'done',
                'title': 'درحال انتقال به صفحه پرداخت',
            })
        else:
            if current_order.coupon_code:
                paid_orders = Order.objects.filter(is_paid=True).all()

                current_order.is_paid = True
                current_order.payment_date = datetime.date.today()
                current_order.sku_id = 1000 + paid_orders.count()
                current_order.status = 'pending'

                stocksystem = current_order.orderdetail_set.all()
                for detail in stocksystem:
                    detail.product.stock -= detail.count
                    detail.product.save()

                for detail in current_order.orderdetail_set.all():
                    detail.final_price = detail.get_total_price()
                    detail.save()

                if current_order.user.phone:
                    OrderStatusService(to=str(current_order.user.phone), pattern='rczcnmv3pgodhte',
                                       id=str(current_order.sku_id))
                current_order.save()
                user_main_address = UserAddressesModel.objects.filter(user_id=current_order.user.id,
                                                                      is_main=True).first()
                if user_main_address is not None:
                    current_order.user_receiver_name = user_main_address.receiver_name
                    current_order.user_receiver_phone = user_main_address.receiver_phone
                    current_order.user_city = user_main_address.city
                    current_order.user_province = user_main_address.province
                    current_order.user_postalcode = user_main_address.postal_code
                    current_order.user_address = user_main_address.address

                    current_order.save()
                messages.success(request, "خرید شما با موفقیت انجام شد", extra_tags="success")

                return JsonResponse({
                    'status': 'done_free',
                    'title': 'درحال انجام عملیات پرداخت',
                })


@method_decorator(login_required, name='dispatch')
class UserContacts(ListView):
    model = ContactUs
    paginate_by = 10
    template_name = 'site_userpanel/user_contacts.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        queryset = queryset.filter(user_id=request.user.id).order_by('-id')
        for contact in queryset.all():
            contact.add_to_user_notify = False
            contact.save()
        return queryset


# phone section

@login_required
def verify_phone(request):
    the_phone = request.GET.get('phone')
    if len(the_phone) == 10:
        the_phone = f"0{the_phone}"
    is_exist = User.objects.filter(phone__iexact=the_phone).first()
    if the_phone == request.user.phone or f'0{the_phone}' == request.user.phone:
        return JsonResponse({
            'status': 'same'
        })
    if the_phone.isdigit():
        if len(the_phone) == 10 and the_phone[:1] == '9' or len(
                the_phone) == 11 and the_phone[:2] == '09':
            if is_exist:
                if the_phone == is_exist.phone:
                    return JsonResponse({
                        'status': 'exist',
                        'title': 'شماره وارد شده قبلا ثبت شده است',
                    })
            else:
                return JsonResponse({
                    'status': 'success',
                })
        else:
            return JsonResponse({
                'status': 'not_valid',
                'title': 'لطفا شماره موبایل معتبر وارد کنید',
            })
    else:
        return JsonResponse({
            'status': 'not_valid',
            'title': 'لطفا شماره موبایل معتبر وارد کنید',
        })


@throttle(zone='set_phone_delay')
@login_required
def set_phone(request):
    the_phone = request.GET.get('phone')
    is_exist = User.objects.filter(phone__iexact=the_phone).first()
    if the_phone == request.user.phone:
        return JsonResponse({
            'status': 'same'
        })
    if the_phone.isdigit():
        if len(the_phone) == 10 and the_phone[:1] == '9' or len(
                the_phone) == 11 and the_phone[:2] == '09':
            if is_exist:

                return JsonResponse({
                    'status': 'exist',
                    'title': 'شماره وارد شده قبلا ثبت شده است',
                })

            else:
                if len(the_phone) == 10:
                    the_phone = f"0{the_phone}"

                userotp = randint(10000, 99999)
                request.session['setphoneotp'] = userotp
                request.session['setphone'] = the_phone
                OTPService(to=the_phone, code=userotp)
                return JsonResponse({
                    'status': 'success',
                    'title': f'کد تایید به شماره {the_phone} ارسال شد',

                })
        else:
            return JsonResponse({
                'status': 'not_valid',
                'title': 'لطفا شماره موبایل معتبر وارد کنید',
            })
    else:
        return JsonResponse({
            'status': 'not_valid',
            'title': 'لطفا شماره موبایل معتبر وارد کنید',
        })


@login_required
def confirm_phone(request):
    otp = request.GET.get('otp')
    thephone = request.session.get('setphone')
    theotp = request.session.get('setphoneotp')
    if otp.isdigit():
        if int(otp) == theotp:
            request.user.phone = thephone
            request.user.username = thephone
            request.user.save()
            del request.session['setphone']
            del request.session['setphoneotp']

            return JsonResponse({
                'status': 'success',
                'title': 'با موفقیت ثبت شد',
            })
        else:
            return JsonResponse({
                'status': 'error',
                'title': 'کد تایید اشتباه است',
            })
    else:
        return JsonResponse({
            'status': 'error',
            'title': 'کد تایید اشتباه است',
        })


# email section
@login_required
def verify_email(request):
    the_email = request.GET.get('email')
    is_exist = User.objects.filter(email__iexact=the_email).first()
    try:
        EmailField().clean(the_email)
        valid_email = True
    except ValidationError:
        valid_email = False

    if the_email == request.user.email:
        return JsonResponse({
            'status': 'same'
        })
    if valid_email and '.com' in the_email:
        if is_exist:
            if the_email != is_exist.email:
                return JsonResponse({
                    'status': 'exist',
                    'title': 'ایمیل وارد شده قبلا ثبت شده است',
                })
        else:
            return JsonResponse({
                'status': 'success',
            })
    else:
        return JsonResponse({
            'status': 'not_valid',
            'title': 'لطفا ایمیل معتبر وارد کنید',
        })


@throttle(zone='set_email_delay')
@login_required
def set_email(request):
    the_email = request.GET.get('email')
    is_exist = User.objects.filter(email__iexact=the_email).first()
    try:
        EmailField().clean(the_email)
        valid_email = True
    except ValidationError:
        valid_email = False

    if the_email == request.user.email:
        return JsonResponse({
            'status': 'same'
        })
    if valid_email and '.com' in the_email:
        if is_exist:
            if the_email != is_exist.email:
                return JsonResponse({
                    'status': 'exist',
                    'title': 'ایمیل وارد شده قبلا ثبت شده است',
                })
        else:
            useremailotp = randint(10000, 99999)
            request.session['setemailotp'] = useremailotp
            request.session['setemail'] = the_email
            send_email(subject='راکافا ', to=the_email, context={'code': useremailotp},
                       template_name='emails/email_otp.html')
            return JsonResponse({
                'status': 'success',
                'title': f'کد تایید به ایمیل {the_email} ارسال شد',

            })
    else:
        return JsonResponse({
            'status': 'not_valid',
            'title': 'لطفا ایمیل معتبر وارد کنید',
        })


@login_required
def confirm_email(request):
    emailotp = request.GET.get('emailotp')
    theemail = request.session.get('setemail')
    theotp = request.session.get('setemailotp')
    if emailotp.isdigit():
        if int(emailotp) == theotp:
            request.user.email = theemail
            request.user.username = theemail
            request.user.save()
            del request.session['setemail']
            del request.session['setemailotp']

            return JsonResponse({
                'status': 'success',
                'title': 'با موفقیت ثبت شد',
            })

        else:
            return JsonResponse({
                'status': 'error',
                'title': 'کد تایید اشتباه است',
            })
    else:
        return JsonResponse({
            'status': 'error',
            'title': 'کد تایید اشتباه است',
        })


@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'site_userpanel/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        userorders = Order.objects.filter(user_id=request.user.id, is_paid=True).all().order_by('-payment_date')[:6]
        context['orders'] = userorders
        userbookmarks = UserFavoriteProducts.objects.filter(user_id=request.user.id).all().order_by('-id')[:3]
        context['bookmarks'] = userbookmarks
        context['setting'] = SiteSetting.objects.get(is_main=True)
        return context


@method_decorator(login_required, name='dispatch')
class EditUserProfilePage(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'form': edit_form,
            'current_user': current_user,
            'setting': SiteSetting.objects.get(is_main=True)

        }
        return render(request, 'site_userpanel/edit_profile.html', context)

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
            messages.success(request, message="تغییرات با موفقیت ثبت شد", extra_tags="success")
            return redirect('userpanel_edit_profile')

        context = {
            'form': edit_form,
            'current_user': current_user
        }

        return render(request, 'site_userpanel/edit_profile.html', context)

    

@method_decorator(login_required, name='dispatch')
class UserOrders(ListView):
    model = Order
    paginate_by = 9
    template_name = 'site_userpanel/user_orders.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        queryset = queryset.filter(user_id=request.user.id, is_paid=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        all_orders = Order.objects.filter(user_id=request.user.id, is_paid=True).all().order_by('-sku_id')
        context['all_orders'] = all_orders
        context['setting'] = SiteSetting.objects.get(is_main=True)
        return context


@method_decorator(login_required, name='dispatch')
class UserOrdersDetail(DetailView):
    model = Order
    template_name = 'site_userpanel/user_orders_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context['setting'] = SiteSetting.objects.get(is_main=True)
        return context


@method_decorator(login_required, name='dispatch')
class UserRecents(ListView):
    model = UserRecentVisitedProduct
    paginate_by = 10
    template_name = 'site_userpanel/user_recents.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        queryset = queryset.filter(user_id=request.user.id).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context['setting'] = SiteSetting.objects.get(is_main=True)
        return context


@method_decorator(login_required, name='dispatch')
class UserBookmarks(ListView):
    model = UserFavoriteProducts
    paginate_by = 10
    template_name = 'site_userpanel/user_bookmarks.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        queryset = queryset.filter(user_id=request.user.id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        favorite_count = UserFavoriteProducts.objects.filter(user_id=request.user.id).all().count()
        context['favorite_count'] = favorite_count
        context['setting'] = SiteSetting.objects.get(is_main=True)

        return context


@throttle(zone='bookmark_delay')
def add_to_bookmarks(request):
    product_id = int(request.GET.get('product_id'))
    product = Product.objects.filter(id=product_id).first()
    if request.user.is_authenticated:
        if product is not None:
            is_exist = UserFavoriteProducts.objects.filter(user_id=request.user.id, product_id=product.id).first()
            if is_exist is not None:
                is_exist.delete()
                favorite_count = UserFavoriteProducts.objects.filter(user_id=request.user.id).all().count()
                userbookmarks = UserFavoriteProducts.objects.filter(user_id=request.user.id).all().order_by('-id')[:3]

                context = {
                    'favorite_count': favorite_count,
                    'object_list': UserFavoriteProducts.objects.filter(user_id=request.user.id),
                    'bookmarks': userbookmarks

                }
                return JsonResponse({
                    'status': 'removed',
                    'body': render_to_string('site_userpanel/content/user_bookmarks_content.html', context),
                    'body2': render_to_string('site_userpanel/content/user_bookmarks_dashboard_content.html', context),

                })
            else:
                new_favorite = UserFavoriteProducts(user_id=request.user.id, product_id=product.id)
                new_favorite.save()
                return JsonResponse({
                    'status': 'success',

                })
        else:
            return JsonResponse({
                'status': 'not_found',
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
        })


@login_required
def remove_all_bookmarks(request):
    theuser = User.objects.filter(id=request.user.id).first()
    user_favorites = theuser.userfavoriteproducts_set.all()
    if user_favorites is not None:
        for item in user_favorites:
            item.delete()
        favorite_count = UserFavoriteProducts.objects.filter(user_id=request.user.id).all().count()

        context = {
            'favorite_count': favorite_count,
            'object_list': UserFavoriteProducts.objects.filter(user_id=request.user.id)
        }
        return JsonResponse({
            'status': 'success',
            'body': render_to_string('site_userpanel/content/user_bookmarks_content.html', context),

        })
    return JsonResponse({
        'status': 'not_found',
    })


@method_decorator(login_required, name='dispatch')
class UserAddresses(ListView):
    model = UserAddressesModel
    template_name = 'site_userpanel/user_addresses.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.request
        queryset = queryset.filter(user_id=request.user.id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        mainaddress = UserAddressesModel.objects.filter(user_id=request.user.id, is_main=True).first()
        addresses = UserAddressesModel.objects.filter(user_id=request.user.id).all()
        context['mainaddress'] = mainaddress
        context['addresses_count'] = addresses.count()
        context['setting'] = SiteSetting.objects.get(is_main=True)

        return context


@login_required
@throttle(zone='addresses_delay')
def add_new_address(request):
    receiver_name = request.GET.get('receivername')
    receiver_phone = request.GET.get('receiverphone')
    province = request.GET.get('province')
    city = request.GET.get('city')
    postalcode = request.GET.get('postalcode')
    address = request.GET.get('address')

    addresses_count = UserAddressesModel.objects.filter(user_id=request.user.id).all().count()
    if int(addresses_count) > 4:
        return JsonResponse({
            'status': 'full',
            'title': 'شما نمیتوانید بیش از 4 آدرس ثبت کنید',
        })
    if receiver_name == "":
        return JsonResponse({
            'status': 'error',
            'title': 'فیلد نام تحویل گیرنده خالی است',
        })
    if receiver_phone == "":
        return JsonResponse({
            'status': 'error',
            'title': 'فیلد شماره تماس تحویل گیرنده خالی است',
        })
    if len(receiver_phone) == 10 and receiver_phone[:1] == '9' or len(
            receiver_phone) == 11 and receiver_phone[:2] == '09':
        pass
    else:
        return JsonResponse({
            'status': 'error',
            'title': 'فیلد شماره تماس وارد شده معتبر نمیباشد',
        })
    if province == "" or province == "0":
        return JsonResponse({
            'status': 'error',
            'title': 'فیلد استان خالی است',
        })
    if city == "" or city == "0":
        return JsonResponse({
            'status': 'error',
            'title': 'فیلد شهر خالی است',
        })
    if len(postalcode) != 10:
        return JsonResponse({
            'status': 'error',
            'title': 'کد پستی معتبر نمیباشد',
        })
    if address == "":
        return JsonResponse({
            'status': 'error',
            'title': 'فیلد آدرس خالی است',
        })
    else:
        new_address = UserAddressesModel(user_id=request.user.id, province=province, city=city, postal_code=postalcode,
                                         address=address, receiver_name=receiver_name, receiver_phone=receiver_phone)
        if addresses_count == 0:
            new_address.is_main = True
        new_address.save()
        mainaddress = UserAddressesModel.objects.filter(user_id=request.user.id, is_main=True).first()
        current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                 user_id=request.user.id)
        total_amount = current_order.calculate_total_price
        total_amount_before_discount = current_order.calculate_total_price_before_discount

        user = User.objects.filter(id=request.user.id).first()
        context = {
            'theuser': user,
            'order': current_order,
            'sum': total_amount,
            'sum_before_discount': total_amount_before_discount,

            'mainaddress': mainaddress,
            'object_list': UserAddressesModel.objects.filter(user_id=request.user.id),
            'addresses_count': UserAddressesModel.objects.filter(user_id=request.user.id).all().count(),

        }
        return JsonResponse({
            'status': 'success',
            'title': 'آدرس جدید با موفقیت ثبت شد',
            'body': render_to_string('site_userpanel/content/user_addresses_content.html', context),
            'body2': render_to_string('site_userpanel/content/user_basket_address_content.html', context),

        })


@login_required
def check_user_addresses_count(request):
    addresses_count = UserAddressesModel.objects.filter(user_id=request.user.id).all().count()
    if int(addresses_count) >= 4:
        return JsonResponse({
            'status': 'error',
            'title': 'شما نمیتوانید بیش از 4 آدرس ثبت کنید',
        })
    else:
        return JsonResponse({
            'status': 'success',
        })


@login_required
def remove_address(request):
    address_id = request.GET.get('address_id')

    address = UserAddressesModel.objects.filter(user_id=request.user.id, id=address_id).first()
    if address:
        address.delete()
        mainaddress = UserAddressesModel.objects.filter(user_id=request.user.id, is_main=True).first()
        current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                 user_id=request.user.id)
        total_amount = current_order.calculate_total_price
        total_amount_before_discount = current_order.calculate_total_price_before_discount

        user = User.objects.filter(id=request.user.id).first()
        context = {
            'theuser': user,
            'order': current_order,
            'sum': total_amount,
            'sum_before_discount': total_amount_before_discount,

            'mainaddress': mainaddress,
            'object_list': UserAddressesModel.objects.filter(user_id=request.user.id),
            'addresses_count': UserAddressesModel.objects.filter(user_id=request.user.id).all().count(),

        }
        return JsonResponse({
            'status': 'success',
            'title': 'با موفقیت حذف شد',
            'body': render_to_string('site_userpanel/content/user_addresses_content.html', context),
            'body2': render_to_string('site_userpanel/content/user_basket_address_content.html', context),

        })
    else:
        return JsonResponse({
            'status': 'error',
            'title': 'آدرس مورد نظر یافت نشد',

        })


@login_required
def edit_address(request):
    address_id = request.GET.get('address_id')

    receiver_name = request.GET.get('receivername')
    receiver_phone = request.GET.get('receiverphone')
    province = request.GET.get('province')
    city = request.GET.get('city')
    postalcode = request.GET.get('postalcode')
    address = request.GET.get('address')

    theaddress = UserAddressesModel.objects.filter(user_id=request.user.id, id=address_id).first()
    if address:
        if receiver_name == "":
            return JsonResponse({
                'status': 'error',
                'title': 'فیلد نام تحویل گیرنده خالی است',
            })
        if receiver_phone == "":
            return JsonResponse({
                'status': 'error',
                'title': 'فیلد شماره تماس تحویل گیرنده خالی است',
            })
        if len(receiver_phone) == 10 and receiver_phone[:1] == '9' or len(
                receiver_phone) == 11 and receiver_phone[:2] == '09':
            pass
        else:
            return JsonResponse({
                'status': 'error',
                'title': 'فیلد شماره تماس وارد شده معتبر نمیباشد',
            })
        if province == "" or province == "0":
            return JsonResponse({
                'status': 'error',
                'title': 'فیلد استان خالی است',
            })

        if city == "" or city == "0":
            return JsonResponse({
                'status': 'error',
                'title': 'فیلد شهر خالی است',
            })
        if len(postalcode) != 10:
            return JsonResponse({
                'status': 'error',
                'title': 'کد پستی معتبر نمیباشد',
            })
        if address == "":
            return JsonResponse({
                'status': 'error',
                'title': 'فیلد آدرس خالی است',
            })
        else:
            theaddress.receiver_name = receiver_name
            theaddress.receiver_phone = receiver_phone
            theaddress.province = province
            theaddress.city = city
            theaddress.postalcode = postalcode
            theaddress.address = address
            theaddress.save()

            mainaddress = UserAddressesModel.objects.filter(user_id=request.user.id, is_main=True).first()
            current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                     user_id=request.user.id)
            total_amount = current_order.calculate_total_price
            total_amount_before_discount = current_order.calculate_total_price_before_discount

            user = User.objects.filter(id=request.user.id).first()
            context = {
                'theuser': user,
                'order': current_order,
                'sum': total_amount,
                'sum_before_discount': total_amount_before_discount,

                'mainaddress': mainaddress,
                'object_list': UserAddressesModel.objects.filter(user_id=request.user.id),
                'addresses_count': UserAddressesModel.objects.filter(user_id=request.user.id).all().count(),

            }
            return JsonResponse({
                'status': 'success',
                'title': 'آدرس با موفقیت ویرایش شد',
                'body': render_to_string('site_userpanel/content/user_addresses_content.html', context),
                'body2': render_to_string('site_userpanel/content/user_basket_address_content.html', context),

            })


@login_required
def edit_address_info(request):
    address_id = request.GET.get('address_id')

    address = UserAddressesModel.objects.filter(user_id=request.user.id, id=address_id).first()
    if address:
        return JsonResponse({
            'status': 'success',
            'receivername': address.receiver_name,
            'receiverphone': address.receiver_phone,
            'province': address.province,
            'city': address.city,
            'postalcode': address.postal_code,
            'address': address.address,

        })


@login_required
@throttle(zone='addresses_delay')
def set_address_main(request):
    address_id = request.GET.get('address_id')

    is_main_address = UserAddressesModel.objects.filter(user_id=request.user.id, id=address_id).first()
    if is_main_address.is_main:
        return None
    theaddress = UserAddressesModel.objects.filter(user_id=request.user.id).all()
    if theaddress:
        for add in theaddress:
            add.is_main = False
            add.save()

    set_main_address = UserAddressesModel.objects.filter(user_id=request.user.id, id=address_id).first()

    if set_main_address:
        set_main_address.is_main = True
        set_main_address.save()

        mainaddress = UserAddressesModel.objects.filter(user_id=request.user.id, is_main=True).first()
        current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                 user_id=request.user.id)
        total_amount = current_order.calculate_total_price
        total_amount_before_discount = current_order.calculate_total_price_before_discount

        user = User.objects.filter(id=request.user.id).first()
        context = {
            'theuser': user,
            'order': current_order,
            'sum': total_amount,
            'sum_before_discount': total_amount_before_discount,

            'mainaddress': mainaddress,
            'object_list': UserAddressesModel.objects.filter(user_id=request.user.id),
            'addresses_count': UserAddressesModel.objects.filter(user_id=request.user.id).all().count(),

        }

        return JsonResponse({
            'status': 'success',
            'title': 'آدرس پیش فرض با موفقیت تغییر کرد',
            'body': render_to_string('site_userpanel/content/user_addresses_content.html', context),
            'body2': render_to_string('site_userpanel/content/user_basket_address_content.html', context),

        })


@method_decorator(login_required, name='dispatch')
class EditPasswordPage(View):
    def get(self, request):
        if self.request.user.check_password('VSX#!2pUsk13&&WyhbtY4ZK*w8kl%Q'):
            return redirect('userpanel_set_password')
        form = EditPasswordForm()
        context = {
            'form': form,
            'setting': SiteSetting.objects.get(is_main=True)

        }
        return render(request, 'site_userpanel/change_password.html', context)

    def post(self, request):
        form = EditPasswordForm(request.POST)
        if form.is_valid():
            current_user = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('confirm_password'))
                current_user.save()
                logout(request)
                login(request, current_user)
                messages.success(request, "کلمه عبور شما با موفقیت تغییر داده شد", extra_tags='success')

                return redirect('userpanel_dashboard')
            else:
                form.add_error('current_password', 'کلمه عبور وارد شده اشتباه است')

        context = {
            'form': form,

            'setting': SiteSetting.objects.get(is_main=True)

        }
        return render(request, 'site_userpanel/change_password.html', context)


@method_decorator(login_required, name='dispatch')
class SetPasswordPage(View):
    def get(self, request):
        if not self.request.user.check_password('VSX#!2pUsk13&&WyhbtY4ZK*w8kl%Q'):
            return redirect('userpanel_dashboard')
        form = SetPasswordForm()
        context = {
            'form': form,
            'setting': SiteSetting.objects.get(is_main=True)

        }
        return render(request, 'site_userpanel/set_password.html', context)

    def post(self, request):
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            current_user = User.objects.filter(id=request.user.id).first()
            current_user.set_password(form.cleaned_data.get('confirm_password'))
            current_user.save()
            logout(request)
            login(request, current_user)
            messages.success(request, message="کلمه عبور جدید شما با موفقیت ثبت شد", extra_tags="success")
            messages.success(request, message="با موفقیت وارد شدید", extra_tags="success")

            return redirect('userpanel_dashboard')

        context = {
            'form': form,
            'setting': SiteSetting.objects.get(is_main=True)

        }
        return render(request, 'site_userpanel/set_password.html', context)


@login_required
def userpanel_menu_component(request):
    current_user = User.objects.filter(id=request.user.id).first()
    status = current_user.check_password('VSX#!2pUsk13&&WyhbtY4ZK*w8kl%Q')
    orders_count = Order.objects.filter(user_id=current_user.id, is_paid=True).all()
    favorites_count = UserFavoriteProducts.objects.filter(user_id=current_user.id).all()
    contact_notify = ContactUs.objects.filter(user_id=request.user.id, add_to_user_notify=True).all().count()
    wholesale_notify = WholeSale.objects.filter(user_id=request.user.id, add_to_user_notify=True).all().count()

    context = {
        'current_user': current_user,
        'status': status,
        'orders_count': orders_count.count(),
        'favorites_count': favorites_count.count(),
        'contact_notify': contact_notify,
        'wholesale_notify': wholesale_notify,

    }
    return render(request, 'site_userpanel/component/userpanel_menu_component.html', context)


@login_required
def user_basket(request):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)

    total_amount = current_order.calculate_total_price

    user = User.objects.filter(id=request.user.id).first()
    mainaddress = UserAddressesModel.objects.filter(user_id=request.user.id, is_main=True).first()

    for detail in current_order.orderdetail_set.all():
        detail.save()
    if not current_order.orderdetail_set.all():
        messages.success(request, message="سبد خرید شما خالی میباشد", extra_tags="error")

        return redirect('home_page')

    if not current_order.is_paid:
        current_order.coupon_code = None
        current_order.save()
    context = {
        'theuser': user,
        'order': current_order,
        'sum': total_amount,
        'mainaddress': mainaddress,
        'object_list': UserAddressesModel.objects.filter(user_id=request.user.id),
        'setting': SiteSetting.objects.get(is_main=True)

    }
    return render(request, 'site_userpanel/user_basket.html', context)


@login_required
def user_checkout(request):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)

    total_amount = current_order.calculate_total_price
    total_amount_before_discount = current_order.calculate_total_price_before_discount

    user = User.objects.filter(id=request.user.id).first()
    mainaddress = UserAddressesModel.objects.filter(user_id=request.user.id, is_main=True).first()

    for detail in current_order.orderdetail_set.all():
        detail.save()
    if not current_order.orderdetail_set.all():
        messages.success(request, message="سبد خرید شما خالی میباشد", extra_tags="error")

        return redirect('home_page')
    if not current_order.is_paid:
        current_order.coupon_code = None
        current_order.save()
    addresses = UserAddressesModel.objects.filter(user_id=request.user.id).all()
    context = {
        'theuser': user,
        'order': current_order,
        'sum': total_amount,
        'sum_before_discount': total_amount_before_discount,
        'mainaddress': mainaddress,
        'object_list': UserAddressesModel.objects.filter(user_id=request.user.id),
        'addresses_count': addresses.count(),
        'setting': SiteSetting.objects.get(is_main=True)

    }
    return render(request, 'site_userpanel/user_basket_checkout.html', context)


@login_required
def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                             order__user_id=request.user.id).delete()
    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('site_userpanel/content/user_basket_content.html', context),
        'body2': render_to_string('shared/content/basket_content.html', context),
        'body3': render_to_string('shared/content/m_basket_content.html', context),
        'body4': render_to_string('shared/content/m_basket_content_count.html', context),

    })


@login_required
@throttle(zone='change_order_count_delay')
def change_order_detail_count(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')

    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_state'
        })
    order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()

    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })
    if state == 'increase':
        if order_detail.count < order_detail.product.stock and order_detail.count < 5:
            order_detail.count += 1
            order_detail.save()
        else:
            return JsonResponse({
                'status': 'invalid_state'
            })

    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'invalid_state'
        })
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = current_order.calculate_total_price

    context = {
        'order': current_order,
        'sum': total_amount
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('site_userpanel/content/user_basket_content.html', context),
        'body2': render_to_string('shared/content/basket_content.html', context),
        'body3': render_to_string('shared/content/m_basket_content.html', context),
        'body4': render_to_string('shared/content/m_basket_content_count.html', context),

    })


def header_component(request):
    category = ProductCategory.objects.all()

    setting = SiteSetting.objects.filter(is_main=True).first()

    context = {
        'category': category,
        'setting': setting,

    }

    return render(request, 'site_userpanel/shared/header_component.html', context)


def footer_component(request):
    context = {

    }
    return render(request, 'site_userpanel/shared/footer_component.html', context)
