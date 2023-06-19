import json

import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from site_product.models import Product, ProductAttribute
from utils.phone_service import OrderStatusService
from .models import Order, OrderDetail
from django.contrib import messages
from site_account.models import UserAddresses as UserAddressesModel
from throttle.decorators import throttle

MERCHANT = '67e48342-e795-428c-8d90-0682988cf8c7'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما "  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


@throttle(zone='basket_delay')
def add_product_to_order(request):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    wight_id = int(request.GET.get('weight'))

    productstock = Product.objects.filter(id=product_id).first()
    if count < 1:
        return JsonResponse({
            'status': 'invalid_count',
            'title': 'تعداد وارد شده باید بیشتر از 1 باشد',

        })
    if count > productstock.stock:
        return JsonResponse({
            'status': 'invalid_count_number',
            'title': 'تعداد وارد شده در انبار موجود نمیباشد',

        })
    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        the_weight = ProductAttribute.objects.filter(weight_id=wight_id, product_id=product_id,
                                                     is_quantity=True).first()

        if product is not None or the_weight is not None:

            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id,
                                                                        weight=the_weight.weight.title).first()

            if current_order_detail is not None:

                if current_order_detail.count >= productstock.stock:
                    current_order_detail.count = productstock.stock
                else:
                    current_order_detail.count += count
                    if current_order_detail.count >= productstock.stock:
                        current_order_detail.count = productstock.stock
                current_order_detail.final_price = current_order_detail.product_price
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count,
                                         weight=the_weight.weight.title, product_price=the_weight.final_price)
                # new_detail.final_price = new_detail.product_price
                new_detail.save()

            current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                                     user_id=request.user.id)
            total_amount = current_order.calculate_total_price
            context = {
                'order': current_order,
                'sum': total_amount,

            }
            return JsonResponse({
                'status': 'success',
                'body': render_to_string('shared/content/basket_content.html', context),
                'body2': render_to_string('shared/content/m_basket_content.html', context),
                'body3': render_to_string('shared/content/m_basket_content_count.html', context),

            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'title': 'محصول مورد نظر یافت نشد'
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'icon': 'error',
            'title': 'برای افزودن محصول به سبد خرید ابتدا وارد شوید'
        })


@login_required
def request_payment(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()
    detail_count = current_order.orderdetail_set.all().count()

    if detail_count == 0:
        return redirect('user_basket_page')
    if total_price > 0 and total_price < 1000:
        total_price = 1000
    user_main_address = UserAddressesModel.objects.filter(user_id=current_order.user.id,
                                                          is_main=True).first()
    if user_main_address is not None:
        current_order.user_receiver_name = user_main_address.receiver_name
        current_order.user_receiver_phone= user_main_address.receiver_phone
        current_order.user_city = user_main_address.city
        current_order.user_province = user_main_address.province
        current_order.user_postalcode = user_main_address.postal_code
        current_order.user_address = user_main_address.address

        current_order.save()


    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}

    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)

    authority = req.json()['data']['authority']

    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required
def verify_payment(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_price()

    paid_orders = Order.objects.filter(is_paid=True).all()

    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
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
                messages.success(request, "خرید شما با موفقیت انجام شد", extra_tags="success")
                context = {
                    'order':current_order,
                }
                return render(request,'site_userpanel/payment_result/success.html',context)
            elif t_status == 101:
                messages.success(request, "تراکنش قبلا پرداخت شده است", extra_tags="success")

                context = {
                    'order': current_order,
                }
                return render(request, 'site_userpanel/payment_result/success.html', context)

            else:
                error = str(req.json()['data']['message'])
                messages.success(request, message=error, extra_tags="error")
                return render(request, 'site_userpanel/payment_result/failed.html')


        else:
            e_message = req.json()['errors']['message']
            messages.success(request, message=e_message, extra_tags="error")

            return render(request, 'site_userpanel/payment_result/failed.html')


    else:
        messages.success(request, message="شما از پرداخت منصرف شده اید", extra_tags="error", )

        return redirect('user_basket_page')

