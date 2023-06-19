from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from  site_product.models import Product

class ContactForm(forms.Form):
    email = forms.CharField(required=False,widget=forms.TextInput(
                            attrs={'class': 'input-element site-form', 'placeholder': 'ایمیل شما' ,'id':'contactformemail'}),
                            validators=[
                                validators.EmailValidator('ایمیل وارد شده معتبر نمیباشد')
                            ]

                            )

    phone = forms.CharField(required=False,widget=forms.TextInput(
                                attrs={'class': 'input-element site-form', 'placeholder': 'شماره تماس شما','id':'contactformphone'}),

                            )

    subject = forms.CharField(required=False,widget=forms.TextInput(
                                  attrs={'class': 'input-element site-form', 'placeholder': 'عنوان شما ( بین 5 تا 50 کاراکتر )','id':'contactformsubject'}),
                              validators=[
                                  validators.MaxLengthValidator(50, 'متن عنوان باید بین 5 تا 50 کاراکتر باشد'),
                                  validators.MinLengthValidator(5, 'متن عنوان باید بین 5 تا 50 کاراکتر باشد'),
                              ]

                              )


    message = forms.CharField(required=False,widget=forms.Textarea(
                                  attrs={'class': 'input-element site-form', 'placeholder': 'پیام شما ( بین 10 تا 255 کاراکتر )','id':'contactformmessage'}),
                              validators=[
                                  validators.MaxLengthValidator(255, 'متن پیام باید بین 10 تا 255 کاراکتر باشد'),
                                  validators.MinLengthValidator(10, 'متن پیام باید بین 10 تا 255 کاراکتر باشد'),
                              ]

                              )

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) == 0:
            self.add_error('email','این فیلد ضروری میباشد')
        return email
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) == 0:
            self.add_error('phone','این فیلد ضروری میباشد')
        elif len(phone) == 10 and phone[:1] == '9' or len(
                    phone) == 11 and phone[:2] == '09':
            return phone
        else:
            self.add_error('phone','شماره تماس وارد شده معتبر نمیباشد')
    def clean_subject(self):
        subject = self.cleaned_data['subject']
        if len(subject) == 0:
            self.add_error('subject','این فیلد ضروری میباشد')
        return subject
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) == 0:
            self.add_error('message','این فیلد ضروری میباشد')
        return message

all_products = Product.objects.filter(category__url_title__iexact='rice').all()
products_tuple = (

)
# if all_products is not None:
#     for p1 in all_products:
#         products_tuple += (p1.title_ir, p1.title_ir),

RICE_MODELS = (
    ('هنوز انتخاب نکردم', 'هنوز انتخاب نکردم'),

)
RICE_MODELS+= products_tuple



class WholeSaleForm(forms.Form):
    email = forms.CharField(label='ایمیل ',required=False,
                            widget=forms.TextInput(
                                attrs={'class': 'input-element', 'placeholder': 'ایمیل شما','id':'wholesaleformemail'}),

                            )

    phone = forms.CharField(label='شماره تماس ',required=False,
                            widget=forms.TextInput(
                                attrs={'class': 'input-element', 'placeholder': 'شماره تماس شما','id':'wholesaleformphone'}),

                            )
    company = forms.CharField(label='نام شرکت (اختیاری)',required=False,
                              widget=forms.TextInput(
                                  attrs={'class': 'input-element', 'placeholder': 'نام شرکت شما'}),

                              )

    province = forms.CharField(label='استان ',required=False,
                               widget=forms.TextInput(
                                   attrs={'class': 'input-element', 'placeholder': 'استان','id':'wholesaleformprovince'}),

                               )

    city = forms.CharField(label='شهر ',required=False,
                           widget=forms.TextInput(
                               attrs={'class': 'input-element', 'placeholder': 'شهر','id':'wholesaleformcity'}),

                           )

    rice = forms.ChoiceField(label='نوع برنج ',required=True, choices=RICE_MODELS,error_messages={'required':'این فیلد ضروری میباشد','invalid_choice':'نوع برنج انتخابی معتبر نمیباشد'},
                             widget=forms.Select(
                                 attrs={'class': 'input-element', 'placeholder': 'نوع برنج'}),

                             )

    amount = forms.IntegerField(label='مقدار ',required=True,error_messages={'required':'این فیلد ضروری میباشد'},
                                widget=forms.NumberInput(
                                    attrs={'class': 'input-element', 'placeholder': 'مقدار (به کیلوگرم)','id':'wholesaleformamount','value':1}),

                                )
    description = forms.CharField(label='توضیحات ',required=False,
                                  widget=forms.Textarea(
                                      attrs={'class': 'input-element', 'placeholder': 'توضیحات اضافی'}),
                                  )
    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) == 0:
            self.add_error('email','این فیلد ضروری میباشد')
        return email
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            self.add_error('amount','مقدار وارد شده معتبر نمیباشد')
        return amount



    def clean_province(self):
        province = self.cleaned_data['province']
        if len(province) == 0:
            self.add_error('province','این فیلد ضروری میباشد')
        return province

    def clean_city(self):
        city = self.cleaned_data['city']
        if len(city) == 0:
            self.add_error('city', 'این فیلد ضروری میباشد')
        return city


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if len(phone) == 0:
            self.add_error('phone','این فیلد ضروری میباشد')
        elif len(phone) == 10 and phone[:1] == '9' or len(
                    phone) == 11 and phone[:2] == '09':
            return phone
        else:
            self.add_error('phone','شماره تماس وارد شده معتبر نمیباشد')




