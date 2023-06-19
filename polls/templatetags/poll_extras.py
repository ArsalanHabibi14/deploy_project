from django import template
from jalali_date import date2jalali

register = template.Library()


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int):
    return '{:,}'.format(value) + ' تومان'


@register.filter(name='three_digits_currency_with_out_toman')
def three_digits_currency_with_out_toman(value: int):
    return '{:,}'.format(value)

@register.filter(name='show_jalali_date')
def show_jalali_date(value):
    return date2jalali(value)

@register.simple_tag()
def multiply(quantity,price,*args,**kwargs):

    return three_digits_currency(quantity*price)