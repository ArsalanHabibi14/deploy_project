from django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from site_account.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'national_code', 'home_phone']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'input-element'}),

            'first_name': forms.TextInput(attrs={'class': 'input-element'}),
            'last_name': forms.TextInput(attrs={'class': 'input-element'}),
            'national_code': forms.TextInput(attrs={'class': 'input-element'}),
            'home_phone': forms.TextInput(attrs={'class': 'input-element'}),
        }
        labels = {

            'first_name': 'نام ',
            'last_name': 'نام خانوادگی ',
            'avatar': 'تصویر پروفایل ',
            'national_Code': 'کد ملی ',
            'home_phone': 'تلفن ثابت ',
        }

    def clean_home_phone(self):
        home_phone = self.cleaned_data.get('home_phone')
        if home_phone is not None:
            if len(home_phone) != 10:
                self.add_error('home_phone', 'تلفن ثابت وارد شده معتبر نمیباشد')
            else:
                return home_phone

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        if national_code is not None:

            if len(national_code) != 10:
                self.add_error('national_code', 'کد ملی وارد شده معتبر نمیباشد')
            else:
                return national_code


class EditPasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی ',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'کلمه عبور فعلی خود را وارد نمایید', 'class': 'input-element inputpassword'})
    )
    password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'کلمه عبور جدید خود را وارد نمایید', 'class': 'input-element inputpassword'}),
        validators=[
            validators.MaxLengthValidator(30, 'کلمه عبور باید بین 6 تا 30 کاراکتر باشد'),
            validators.MinLengthValidator(6, 'کلمه عبور باید بین 6 تا 30 کاراکتر باشد')
        ]
    )
    confirm_password = forms.CharField(
        label='تایید کلمه عبور جدید ',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'کلمه عبور جدید خود را مجددا وارد نمایید', 'class': 'input-element inputpassword'}),
        validators=[
            validators.MaxLengthValidator(30, 'کلمه عبور باید بین 6 تا 30 کاراکتر باشد'),
            validators.MinLengthValidator(6, 'کلمه عبور باید بین 6 تا 30 کاراکتر باشد')
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه های عبور جدید یکسان نمیباشند')


class SetPasswordForm(forms.Form):
    password = forms.CharField(
        label='ثبت کلمه عبور',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'کلمه عبور جدید خود را وارد نمایید', 'class': 'input-element inputpassword'}),
        validators=[
            validators.MaxLengthValidator(30, 'کلمه عبور باید بین 6 تا 30 کاراکتر باشد'),
            validators.MinLengthValidator(6, 'کلمه عبور باید بین 6 تا 30 کاراکتر باشد')
        ]
    )
    confirm_password = forms.CharField(
        label='تایید کلمه عبور  ',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'کلمه عبور جدید خود را مجددا وارد نمایید', 'class': 'input-element inputpassword'}),
        validators=[
            validators.MaxLengthValidator(30, 'کلمه عبور باید بین 6 تا 30 کاراکتر باشد'),
            validators.MinLengthValidator(6, 'کلمه عبور باید بین 6 تا 30 کاراکتر باشد')
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه های عبور جدید یکسان نمیباشند')
