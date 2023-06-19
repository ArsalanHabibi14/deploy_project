# from celery import shared_task
#
# from utils.email_service import send_email
# from utils.phone_service import OTPService
#
# from rakafaproject.celery import app
#
#
# @app.task(name="Send Phone Otp")
# def celery_send_otp(phone, code):
#     OTPService(to=phone, code=code)
#
#
# @app.task(name="Send Email Otp")
# def celery_send_email_otp(email, code):
#     print(f"{email} : {code}")
#     send_email(to=email, context={'code': code})
