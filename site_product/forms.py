from django import forms
from django.core import validators


SCORE = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)
SUGGEST= (
    ('suggested', 'پیشنهاد میکنم'),
    ('notsuggested', 'پیشنهاد نمی کنم'),
)

class AddProductComment(forms.Form):
    score = forms.ChoiceField(label='امتیاز شما ', required=True, choices=SCORE,
                             error_messages={'required': 'این فیلد ضروری است',
                                             'invalid_choice': 'گزینه انتخابی معتبر نمیباشد'},
                             widget=forms.Select(
                                 attrs={'class': 'input-element my-2','id':'productCommentScore' }),

                             )
    suggest = forms.ChoiceField(label='خرید این محصول را برای دیگران ', required=True, choices=SUGGEST,
                              error_messages={'required': 'این فیلد ضروری است',
                                              'invalid_choice': 'گزینه انتخابی معتبر نمیباشد'},
                              widget=forms.Select(
                                  attrs={'class': 'input-element my-2','id':'productCommentSuggest' }),

                              )
    message = forms.CharField(label='متن دیدگاه ',required=False,widget=forms.Textarea(
                                  attrs={'class': 'input-element my-2', 'placeholder': 'دیدگاه شما حداقل 10 کاراکتر','id':'productCommentMessage'}),
                              validators=[
                                  validators.MaxLengthValidator(200, 'متن دیدگاه باید بین 10 تا 200 کاراکتر باشد'),
                                  validators.MinLengthValidator(10, 'متن دیدگاه باید بین 10 تا 200 کاراکتر باشد'),
                              ]

                              )
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) == 0:
            self.add_error('message','این فیلد ضروری میباشد')
        return message

