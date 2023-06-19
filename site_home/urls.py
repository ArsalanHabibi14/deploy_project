from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.HomeView.as_view(),name='home_page'),
    path('contact/', views.ContactView.as_view(), name='contact_page'),
    path('why-rakafa/', views.WhyUsView.as_view(), name='whyus_page'),
    path('faq/', views.FaqView.as_view(), name='faq_page'),
    path('about/', views.AboutView.as_view(), name='about_page'),
    path('wholesale/', views.WholeSaleView.as_view(), name='wholesale_page'),
    path('rules/', views.RulesView.as_view(), name='rules_page'),
    path('terms/', views.TermsView.as_view(), name='terms_page'),

    path('submit-sign-email/', views.submit_sign_email, name='submit_sign_email'),

    path('search-expenses/', csrf_exempt(views.product_search), name='home_search_product'),

]