from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View
from throttle.decorators import throttle

from site_form.forms import ContactForm, WholeSaleForm
from site_form.models import ContactUs, SignEmails, WholeSale
from site_order.models import Order
from site_product.models import Product, ProductCategory, ProductSubCategory, UserRecentVisitedProduct
from site_setting.models import SiteSetting
from site_setting.models import SiteVisit
from utils.http_service import get_client_ip
import json


def product_search(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Product.objects.filter(title_ir__icontains=search_str) | Product.objects.filter(
            title_en__icontains=search_str)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


class HomeView(TemplateView):
    template_name = 'site_home/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = SiteSetting.objects.filter(is_main=True).first()

        context['setting'] = setting

        suggested_products = Product.objects.filter(is_active=True, is_delete=False, suggested=True,
                                                    quantity=True).order_by('-id')
        latest_products = Product.objects.filter(is_active=True, is_delete=False, quantity=True).order_by('-id')[:10]
        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True, quantity=True).annotate(
            order_count=Sum(
                'orderdetail__count'
            )).order_by('-order_count')[:15]
        context['suggested_products'] = suggested_products
        context['latest_products'] = latest_products
        context['most_bought_products'] = most_bought_products
        context['user_recent_visited_products'] = UserRecentVisitedProduct.objects.filter(
            user_id=self.request.user.id).all().distinct().order_by('-product__quantity')
        context['ricesubcats'] = ProductSubCategory.objects.filter(category__url_title__iexact='rice').all()

        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = SiteVisit.objects.filter(ip__iexact=user_ip).exists()
        if not has_been_visited:
            new_visit = SiteVisit(ip=user_ip, user_id=user_id)
            new_visit.save()
        return context


class RulesView(TemplateView):
    template_name = 'site_home/rules_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = SiteSetting.objects.filter(is_main=True).first()
        context['setting'] = setting
        return context


class TermsView(TemplateView):
    template_name = 'site_home/terms_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = SiteSetting.objects.filter(is_main=True).first()
        context['setting'] = setting
        return context


class WholeSaleView(View):
    def get(self, request):
        form = WholeSaleForm()
        setting = SiteSetting.objects.filter(is_main=True).first()
        context = {
            'form': form,
            'setting': setting,

        }
        return render(request, 'site_home/wholesale_page.html', context)

    def post(self, request):
        form = WholeSaleForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            company = form.cleaned_data.get('company')
            province = form.cleaned_data.get('province')
            city = form.cleaned_data.get('city')
            rice = form.cleaned_data.get('rice')
            amount = form.cleaned_data.get('amount')
            description = form.cleaned_data.get('description')

            if self.request.user.is_authenticated:
                new_wholesale = WholeSale(user_id=self.request.user.id, email=email, phone=phone, company=company,
                                          province=province, city=city, rice=rice, amount=amount,
                                          description=description)
                new_wholesale.save()
                messages.success(request, "با موفقیت ثبت شد وضعیت را میتوانید در پنل کاربری خود مشاهده کنید",
                                 extra_tags="success")

                return redirect('wholesale_page')
            else:
                new_wholesale = WholeSale(email=email, phone=phone, company=company,
                                          province=province, city=city, rice=rice, amount=amount,
                                          description=description)
                new_wholesale.save()
                messages.success(request, "با موفقیت ثبت شد", extra_tags="success")

                return redirect('wholesale_page')
        setting = SiteSetting.objects.filter(is_main=True).first()

        context = {
            'form': form,
            'setting': setting,

        }
        return render(request, 'site_home/wholesale_page.html', context)


class FaqView(TemplateView):
    template_name = 'site_home/faq_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = SiteSetting.objects.filter(is_main=True).first()
        context['setting'] = setting
        return context


class AboutView(TemplateView):
    template_name = 'site_home/about_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = SiteSetting.objects.filter(is_main=True).first()
        context['setting'] = setting
        return context


class WhyUsView(TemplateView):
    template_name = 'site_home/whyus_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = SiteSetting.objects.filter(is_main=True).first()
        context['setting'] = setting
        context['ricesubcats'] = ProductSubCategory.objects.filter(category__url_title__iexact='rice').all()

        return context


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        setting = SiteSetting.objects.filter(is_main=True).first()

        context = {
            'form': form,
            'setting': setting

        }
        return render(request, 'site_home/contact_page.html', context)

    @throttle(zone='contact_delay')
    def post(self, request):
        form = ContactForm(request.POST or None)
        setting = SiteSetting.objects.filter(is_main=True).first()

        if form.is_valid():

            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            if self.request.user.is_authenticated:

                new_contact = ContactUs(user_id=self.request.user.id, email=email, phone=phone, subject=subject,
                                        message=message)
                new_contact.save()
                messages.success(request, "با موفقیت ثبت شد وضعیت را میتوانید در پنل کاربری خود مشاهده کنید",
                                 extra_tags="success")

                return redirect('contact_page')

            else:

                new_contact = ContactUs(email=email,
                                        phone=phone, subject=subject, message=message)
                new_contact.save()
                messages.success(request, "با موفقیت ثبت شد", extra_tags="success")

                return redirect('contact_page')

        context = {
            'form': form,
            'setting': setting
        }
        return render(request, 'site_home/contact_page.html', context)




@throttle(zone='email_sign_delay')
def submit_sign_email(request):
    email = request.GET.get('email')
    if '@' and '.com' not in email:
        return JsonResponse({
            'status': 'success',
            'title': 'با موفقیت ثبت شد',
        })
    theEmail = SignEmails.objects.filter(email__iexact=email).first()

    if theEmail:
        return JsonResponse({
            'status': 'success',
            'title': 'با موفقیت ثبت شد',
        })
    else:
        new_email = SignEmails(email=email)
        new_email.save()
        return JsonResponse({
            'status': 'success',
            'title': 'با موفقیت ثبت شد',
        })


def header_component(request):
    category = ProductCategory.objects.all()
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)

    total_amount = current_order.calculate_total_price
    user_contact_notify = ContactUs.objects.filter(user_id=request.user.id, add_to_user_notify=True).all().count()

    setting = SiteSetting.objects.filter(is_main=True).first()
    user_notify = user_contact_notify

    for detail in current_order.orderdetail_set.all():
        detail.save()

    subcategory_for_search = ProductSubCategory.objects.all()[:4]

    context = {
        'category': category,
        'order': current_order,
        'sum': total_amount,
        'setting': setting,
        'user_notify': user_notify,
        'subcategory_for_search': subcategory_for_search,
        'product': Product.objects.all(),

    }

    return render(request, 'shared/components/header.html', context)


def header_references_component(request):
    setting = SiteSetting.objects.filter(is_main=True).first()
    context = {
        'setting': setting
    }
    return render(request, 'shared/references/header.html', context)


def basket_content(request):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)

    total_amount = current_order.calculate_total_price
    for detail in current_order.orderdetail_set.all():
        detail.save()
    context = {
        'order': current_order,
        'sum': total_amount,

    }
    return render(request, 'shared/content/basket_content.html', context)


def footer_component(request):
    subcats = ProductSubCategory.objects.all()
    setting = SiteSetting.objects.filter(is_main=True).first()
    context = {
        'subcats': subcats,
        'setting': setting,

    }
    return render(request, 'shared/components/footer.html', context)


def handle_404_error(request, exception):
    return render(request, 'shared/pages/404.html')
