from random import randint

from django.contrib import messages
from django.contrib.auth import logout, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from throttle.decorators import throttle

from site_setting.models import SiteSetting
from utils.email_service import send_email
from utils.phone_service import OTPService
from .models import User
# from .tasks import celery_send_otp, celery_send_email_otp


class LoginView(View):

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('home_page')
        request.session['login_by_phone_otp_user_pk'] = None
        request.session['login_by_password_user_pk'] = None

        request.session['register_by_phone_otp_number'] = None
        request.session['register_by_phone_otp_code'] = None

        request.session['login_by_email_otp_user_pk'] = None

        request.session['register_by_email_otp_address'] = None
        request.session['register_by_email_otp_code'] = None

        setting = SiteSetting.objects.filter(is_main=True).first()
        context = {
            'setting': setting
        }
        return render(request, 'site_account/login.html', context)


@throttle(zone='login_delay')
def AuthView(request):
    user_login_info = request.GET.get('info')
    if user_login_info:
        if user_login_info.isdigit():

            auth_by_phone = User.objects.filter(phone__iexact=user_login_info).first()
            if len(user_login_info) == 10:
                auth_by_phone = User.objects.filter(phone__iexact=f'0{user_login_info}').first()

            if auth_by_phone is not None:
                if auth_by_phone.check_password('VSX#!2pUsk13&&WyhbtY4ZK*w8kl%Q'):
                    auth_by_phone.phone_otp = randint(10000, 99999)
                    auth_by_phone.save()
                    OTPService(to=auth_by_phone.phone, code=auth_by_phone.phone_otp)
                    # celery_send_otp.delay(auth_by_phone.phone, auth_by_phone.phone_otp)

                    context = {
                        'phone_number': auth_by_phone.phone
                    }

                    request.session.set_expiry(180)
                    request.session['login_by_phone_otp_user_pk'] = auth_by_phone.pk

                    return JsonResponse({
                        'status': 'auth_by_phone_otp',
                        'phone_number': auth_by_phone.phone,
                        'body': render_to_string('site_account/sections/phone_otp_login_section.html', context),

                    })

                else:
                    request.session.set_expiry(180)
                    request.session['login_by_phone_otp_user_pk'] = auth_by_phone.pk

                    request.session.set_expiry(180)
                    request.session['login_by_password_user_pk'] = auth_by_phone.pk
                    return JsonResponse({
                        'status': 'login_by_password',
                        'body': render_to_string('site_account/sections/password_login_section.html'),

                    })
            else:
                if user_login_info.startswith(('9', '09')) and len(user_login_info) in (10, 11):
                    if len(user_login_info) == 10:
                        user_login_info = f'0{user_login_info}'
                    register_by_phone_otp = randint(10000, 99999)

                    request.session.set_expiry(180)
                    request.session['register_by_phone_otp_number'] = user_login_info

                    request.session.set_expiry(180)
                    request.session['register_by_phone_otp_code'] = register_by_phone_otp
                    OTPService(to=user_login_info, code=register_by_phone_otp)
                    # celery_send_otp.delay(user_login_info, register_by_phone_otp)

                    context = {
                        'phone_number': user_login_info
                    }
                    return JsonResponse({
                        'status': 'auth_by_phone_otp',
                        'phone_number': user_login_info,

                        'body': render_to_string('site_account/sections/phone_otp_login_section.html', context),

                    })
                else:
                    return JsonResponse({
                        'status': 'not_valid',
                        'title': 'لطفا شماره موبایل یا ایمیل معتبر وارد کنید',
                    })
        elif '@' and '.com' in user_login_info:
            auth_by_email = User.objects.filter(email__iexact=user_login_info).first()
            if auth_by_email is not None:
                if auth_by_email.check_password('VSX#!2pUsk13&&WyhbtY4ZK*w8kl%Q'):

                    request.session.set_expiry(180)
                    request.session['login_by_email_otp_user_pk'] = auth_by_email.pk

                    auth_by_email.email_otp = randint(10000, 99999)
                    auth_by_email.save()
                    send_email(to=auth_by_email.email, context={'code': auth_by_email.email_otp})
                    # celery_send_email_otp.delay(email=auth_by_email.email, code=auth_by_email.email_otp)
                    context = {
                        'email_address': auth_by_email.email
                    }
                    return JsonResponse({
                        'status': 'auth_by_email_otp',
                        'email_address': auth_by_email.email,
                        'body': render_to_string('site_account/sections/email_otp_login_section.html', context),

                    })

                else:
                    request.session.set_expiry(180)
                    request.session['login_by_email_otp_user_pk'] = auth_by_email.pk

                    request.session.set_expiry(180)
                    request.session['login_by_password_user_pk'] = auth_by_email.pk

                    return JsonResponse({
                        'status': 'login_by_password',
                        'body': render_to_string('site_account/sections/password_login_section.html'),

                    })

            else:
                register_by_email_otp = randint(10000, 99999)
                request.session.set_expiry(180)
                request.session['register_by_email_otp_address'] = user_login_info

                request.session.set_expiry(180)
                request.session['register_by_email_otp_code'] = register_by_email_otp
                send_email( to=user_login_info, context={'code': register_by_email_otp})
                # celery_send_email_otp.delay(email=user_login_info, code=register_by_email_otp)

                context = {
                    'email_address': user_login_info
                }
                return JsonResponse({
                    'status': 'auth_by_email_otp',
                    'email_address': user_login_info,

                    'body': render_to_string('site_account/sections/email_otp_login_section.html', context),

                })
        else:
            return JsonResponse({
                'status': 'not_valid',
                'title': 'لطفا شماره موبایل یا ایمیل معتبر وارد کنید',
            })





    else:
        return JsonResponse({
            'status': 'empty',
            'title': 'لطفا شماره موبایل یا ایمیل خود را وارد کنید',
        })


def SendToOTPSection(request):
    trying_to_login_with_phone_otp_user_id = request.session.get('login_by_phone_otp_user_pk')
    trying_to_login_with_email_otp_user_id = request.session.get('login_by_email_otp_user_pk')

    if trying_to_login_with_phone_otp_user_id is not None:
        the_user = User.objects.filter(pk=trying_to_login_with_phone_otp_user_id).first()
        OTPService(to=the_user.phone, code=the_user.phone_otp)
        # celery_send_otp.delay(the_user.phone, the_user.phone_otp)

        context = {
            'phone_number': the_user.phone
        }
        return JsonResponse({
            'status': 'sended_to_phone_section',
            'phone_number': the_user.phone,
            'body': render_to_string('site_account/sections/phone_otp_login_section.html', context),

        })
    if trying_to_login_with_email_otp_user_id is not None:
        the_user = User.objects.filter(pk=trying_to_login_with_email_otp_user_id).first()

        send_email(to=the_user.email, context={'code': the_user.email_otp})
        # celery_send_email_otp.delay(email=the_user.email, code=the_user.email_otp)

        context = {
            'email_address': the_user.email
        }

        return JsonResponse({
            'status': 'sended_to_email_section',
            'email_address': the_user.email,

            'body': render_to_string('site_account/sections/email_otp_login_section.html', context),

        })
    else:
        return JsonResponse({
            'status': 'home',

        })


def SendToResetPasswordSection(request):
    trying_to_login_with_phone_otp_user_id = request.session.get('login_by_phone_otp_user_pk')
    trying_to_login_with_email_otp_user_id = request.session.get('login_by_email_otp_user_pk')

    request.session.set_expiry(180)

    request.session['reset_password_after_login'] = True

    if trying_to_login_with_phone_otp_user_id is not None:
        the_user = User.objects.filter(pk=trying_to_login_with_phone_otp_user_id).first()
        the_user.save()
        OTPService(to=the_user.phone, code=the_user.phone_otp)
        # celery_send_otp.delay(the_user.phone, the_user.phone_otp)

        context = {
            'phone_number': the_user.phone
        }
        return JsonResponse({
            'status': 'sended_to_phone_section',
            'phone_number': the_user.phone,
            'body': render_to_string('site_account/sections/phone_otp_login_section.html', context),

        })
    if trying_to_login_with_email_otp_user_id is not None:
        the_user = User.objects.filter(pk=trying_to_login_with_email_otp_user_id).first()
        the_user.save()

        send_email( to=the_user.email, context={'code': the_user.email_otp})
        # celery_send_email_otp.delay(email=the_user.email, code=the_user.email_otp)

        context = {
            'email_address': the_user.email
        }

        return JsonResponse({
            'status': 'sended_to_email_section',
            'email_address': the_user.email,

            'body': render_to_string('site_account/sections/email_otp_login_section.html', context),

        })
    else:
        return JsonResponse({
            'status': 'home',

        })


def AuthPasswordView(request):
    User_id = request.session.get('login_by_password_user_pk')

    the_user = User.objects.filter(pk=User_id).first()
    entered_password = request.GET.get('password')

    if User_id is not None:
        if entered_password != "":
            check_password = the_user.check_password(entered_password)
            if check_password:
                login(request, the_user)
                messages.success(request, message="با موفقیت وارد شدید", extra_tags="success")

                return JsonResponse({
                    'status': 'success',
                    'title': 'با موفقیت وارد شدید',

                })
            else:
                return JsonResponse({
                    'status': 'wrong',
                    'title': 'کلمه عبور وارد شده اشتباه است',

                })
        else:
            return JsonResponse({
                'status': 'empty',
                'title': 'لطفا کلمه عبور خود را وارد کنید',

            })
    else:
        return JsonResponse({
            'status': 'home',

        })


# def AuthOTPView(request):
#     trying_to_login_with_phone_otp_user_id = request.session.get('login_by_phone_otp_user_pk')
#     register_by_phone_otp_number = request.session.get('register_by_phone_otp_number')
#     register_by_phone_otp_code = request.session.get('register_by_phone_otp_code')
#
#     trying_to_login_with_email_otp_user_id = request.session.get('login_by_email_otp_user_pk')
#     register_by_email_otp_address = request.session.get('register_by_email_otp_address')
#     register_by_email_otp_code = request.session.get('register_by_email_otp_code')
#
#
#     reset_password_after_login = request.session.get('reset_password_after_login')
#
#     entered_otp = request.GET.get('otp')
#     if trying_to_login_with_phone_otp_user_id is not None:
#         the_user = User.objects.filter(pk=trying_to_login_with_phone_otp_user_id).first()
#
#         if entered_otp != "":
#             if entered_otp == the_user.phone_otp:
#                 the_user.phone_otp = randint(10000, 99999)
#                 the_user.save()
#                 login(request, the_user)
#                 if reset_password_after_login:
#
#                     the_user.set_password('VSX#!2pUsk13&&WyhbtY4ZK*w8kl%Q')
#                     the_user.save()
#                     login(request, the_user)
#
#                     messages.success(request, message="با موفقیت وارد شدید لطفا کلمه عبور جدید خود را ثبت کنید", extra_tags="success")
#                     return JsonResponse({
#                         'status': 'reset_password',
#                         'title': 'با موفقیت وارد شدید',
#
#                     })
#                 else:
#                     messages.success(request, message="با موفقیت وارد شدید", extra_tags="success")
#                     return JsonResponse({
#                         'status': 'success',
#                         'title': 'با موفقیت وارد شدید',
#
#                     })
#
#             else:
#                 return JsonResponse({
#                     'status': 'wrong',
#                     'title': 'کد تایید وارد شده اشتباه میباشد',
#
#                 })
#         else:
#             return JsonResponse({
#                 'status': 'empty',
#                 'title': 'لطفا کد تایید ارسال شده را وارد کنید',
#
#             })
#     if register_by_phone_otp_code is not None or register_by_phone_otp_number is not None:
#         if entered_otp != "":
#             if entered_otp == str(register_by_phone_otp_code):
#                 new_user = User(
#                     phone=register_by_phone_otp_number,
#                     username=register_by_phone_otp_number,
#                 )
#                 new_user.set_password('VSX#!2pUsk13&&WyhbtY4ZK*w8kl%Q')
#                 new_user.save()
#                 login(request, new_user)
#                 messages.success(request, message="با موفقیت وارد شدید", extra_tags="success")
#                 return JsonResponse({
#                     'status': 'success',
#                     'title': 'با موفقیت وارد شدید',
#
#                 })
#             else:
#                 return JsonResponse({
#                     'status': 'wrong',
#                     'title': 'لطفا کد تایید ارسال شده را وارد کنید',
#
#                 })
#         else:
#             return JsonResponse({
#                 'status': 'empty',
#                 'title': 'لطفا کد تایید ارسال شده را وارد کنید',
#
#             })
#
#     if trying_to_login_with_email_otp_user_id is not None:
#         the_user = User.objects.filter(pk=trying_to_login_with_email_otp_user_id).first()
#
#         if entered_otp != "":
#             if entered_otp == the_user.email_otp:
#                 the_user.email_otp = randint(10000, 99999)
#                 the_user.save()
#                 login(request, the_user)
#
#                 if reset_password_after_login:
#                     the_user.set_password('VSX#!2pUsk13&&WyhbtY4ZK*w8kl%Q')
#                     the_user.save()
#                     login(request, the_user)
#
#                     messages.success(request, message="با موفقیت وارد شدید لطفا کلمه عبور جدید خود را ثبت کنید",
#                                      extra_tags="success")
#                     return JsonResponse({
#                         'status': 'reset_password',
#                         'title': 'با موفقیت وارد شدید',
#
#                     })
#                 else:
#                     messages.success(request, message="با موفقیت وارد شدید", extra_tags="success")
#                     return JsonResponse({
#                         'status': 'success',
#                         'title': 'با موفقیت وارد شدید',
#
#                     })
#
#             else:
#                 return JsonResponse({
#                     'status': 'wrong',
#                     'title': 'کد تایید وارد شده اشتباه میباشد',
#
#                 })
#         else:
#             return JsonResponse({
#                 'status': 'empty',
#                 'title': 'لطفا کد تایید ارسال شده را وارد کنید',
#
#             })
#     if register_by_email_otp_code is not None or register_by_email_otp_address is not None:
#         if entered_otp != "":
#             if entered_otp == str(register_by_email_otp_code):
#                 new_user = User(
#                     email=register_by_email_otp_address,
#                     username=register_by_email_otp_address,
#                 )
#                 new_user.set_password('VSX#!2pUsk13&&WyhbtY4ZK*w8kl%Q')
#                 new_user.save()
#                 login(request, new_user)
#                 messages.success(request, message="با موفقیت وارد شدید", extra_tags="success")
#                 return JsonResponse({
#                     'status': 'success',
#                     'title': 'با موفقیت وارد شدید',
#
#                 })
#             else:
#                 return JsonResponse({
#                     'status': 'wrong',
#                     'title': 'لطفا کد تایید ارسال شده را وارد کنید',
#
#                 })
#         else:
#             return JsonResponse({
#                 'status': 'empty',
#                 'title': 'لطفا کد تایید ارسال شده را وارد کنید',
#
#             })
#
#     else:
#         return JsonResponse({
#             'status': 'home',
#
#         })
def AuthOTPView(request):
    entered_otp = request.GET.get('otp')
    user_id = request.session.get('login_by_phone_otp_user_pk') or request.session.get('login_by_email_otp_user_pk')
    reset_password_after_login = request.session.get('reset_password_after_login')

    if user_id:
        the_user = User.objects.filter(pk=user_id).first()

        if entered_otp and entered_otp == the_user.phone_otp or entered_otp == the_user.email_otp:
            the_user.phone_otp = randint(10000, 99999)
            the_user.save()
            login(request, the_user)

            if reset_password_after_login:
                the_user.set_password('VSX#!2pUsk13&&WyhbtY4ZK*w8kl%Q')
                the_user.save()
                login(request, the_user)
                messages.success(request, message="با موفقیت وارد شدید لطفا کلمه عبور جدید خود را ثبت کنید",
                                 extra_tags="success")
                return JsonResponse({'status': 'reset_password', 'title': 'با موفقیت وارد شدید'})
            else:
                messages.success(request, message="با موفقیت وارد شدید", extra_tags="success")
                return JsonResponse({'status': 'success', 'title': 'با موفقیت وارد شدید'})
        else:
            return JsonResponse({'status': 'wrong', 'title': 'کد تایید وارد شده اشتباه میباشد'})
    elif entered_otp == "":
        return JsonResponse({'status': 'empty', 'title': 'لطفا کد تایید ارسال شده را وارد کنید'})
    else:
        pass


# @throttle(zone='resend_otp_delay')
# def ResendOTPView(request):
#     info = request.GET.get('info')
#     if info is not None:
#         if info.isdigit():
#             if len(info) == 10:
#                 info = f"0{info}"
#             user = User.objects.filter(phone__iexact=info).first()
#             if user is not None:
#                 user.phone_otp = randint(10000, 99999)
#                 user.save()
#                 OTPService(to=info, code=user.phone_otp)
#                 return JsonResponse({
#                     'status': 'success',
#                 })
#             else:
#                 new_code = randint(10000, 99999)
#                 request.session['register_by_phone_otp_code'] = new_code
#                 OTPService(to=info, code=new_code)
#                 return JsonResponse({
#                     'status': 'success',
#                 })
#         else:
#             user = User.objects.filter(email__iexact=info).first()
#             if user is not None:
#                 user.email_otp = randint(10000, 99999)
#                 user.save()
#                 send_email(subject='راکافا ', to=user.email, context={'code': user.email_otp},
#                            template_name='emails/email_otp.html')
#                 return JsonResponse({
#                     'status': 'success',
#                 })
#             else:
#                 new_code = randint(10000, 99999)
#                 request.session['registerbyemailaddressotp'] = new_code
#                 send_email(subject='راکافا ', to=info, context={'code': new_code},
#                            template_name='emails/email_otp.html')
#                 return JsonResponse({
#                     'status': 'success',
#                 })
#     else:
#         pass

@throttle(zone='resend_otp_delay')
def ResendOTPView(request):
    info = request.GET.get('info')
    if info is not None:
        from django.db.models import Q
        user = User.objects.filter(Q(phone__iexact=info) | Q(email__iexact=info)).first()
        if user is not None:
            if info.isdigit() and len(info) == 10:
                user.phone_otp = randint(10000, 99999)
                OTPService(to=f"0{info}", code=user.phone_otp)
                # celery_send_otp.delay(phone=f"0{info}", code=user.phone_otp)

            else:
                user.email_otp = randint(10000, 99999)
                send_email(to=info, context={'code': user.email_otp})
                # celery_send_email_otp.delay(email=info, code=user.email_otp)

            user.save()
        else:
            new_code = randint(10000, 99999)
            if info.isdigit() and len(info) == 10:
                request.session.set_expiry(180)

                request.session['register_by_phone_otp_code'] = new_code
                OTPService(to=f"0{info}", code=new_code)
                # celery_send_otp.delay(phone=f"0{info}", code=new_code)

            else:
                request.session.set_expiry(180)
                request.session['registerbyemailaddressotp'] = new_code
                send_email( to=info, context={'code': new_code})
                # celery_send_email_otp.delay(email=info, code=new_code)

        return JsonResponse({'status': 'success'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, message="با موفقیت خارج شدید", extra_tags="success")

        return redirect('home_page')
