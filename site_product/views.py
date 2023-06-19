from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView,View
from site_product.models import Product, ProductVisit, ProductCategory, ProductComment, \
    ProductSubCategory, ProductType, ProductAttribute, UserRecentVisitedProduct
from utils.http_service import get_client_ip
from django.db.models import Max, Min, Count, Avg
from django.template.loader import render_to_string
from .forms import AddProductComment

from throttle.decorators import throttle
# API Section


# Views Section

@throttle(zone='filter_product_delay')
def filter_data(request):

    category = request.GET.getlist('category[]')
    subcategory = request.GET.getlist('subcategory[]')
    isoffer = request.GET.getlist('isoffer[]')
    types = request.GET.getlist('type[]')
    onlyQuantity = request.GET.getlist('onlyQuantity[]')
    onlySpecial = request.GET.getlist('onlySpecial[]')

    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']

    minPrice = minPrice.replace(',','')
    maxPrice = maxPrice.replace(',','')
    # sortBy = request.GET['selectSort']
    allProducts = Product.objects.annotate(
        visit_count=Count('productvisit')).order_by('-visit_count').all()
    allProducts = allProducts.order_by('-quantity')
    allProducts.filter(productattribute__special_price__isnull=False)
    allProducts = allProducts.filter(productattribute__final_price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__final_price__lte=maxPrice)

    if len(category) > 0:
        allProducts = allProducts.filter(category_id__in=category).distinct()
    if len(subcategory) > 0:
        allProducts = allProducts.filter(subcategory_id__in=subcategory).distinct()
    if len(types) > 0:
        allProducts = allProducts.filter(type_id__in=types).distinct()



    if len(isoffer) > 0:
        allProducts = allProducts.filter(productattribute__special_price__isnull=False)

    if len(onlyQuantity) > 0:
        allProducts = allProducts.filter(quantity=True)

    if len(onlySpecial) > 0:
        allProducts = allProducts.filter(productattribute__special_price__isnull=False)


    # if sortBy is not None:
    #     if sortBy == "sort-by-bought":
    #         allProducts=allProducts.annotate(
    #         order_count=Sum(
    #             'orderdetail__count'
    #         )).order_by('-order_count')
    #
    #     elif sortBy == "sort-by-view":
    #         allProducts = allProducts.annotate(
    #         visit_count=Count('productvisit')).order_by('-visit_count')
    #
    #     elif sortBy == "sort-by-new":
    #         allProducts = allProducts.order_by('-create_date')
    #
    #     elif sortBy == "sort-by-lth":
    #         allProducts = allProducts.order_by('productattribute__price')
    #
    #     elif sortBy == "sort-by-htl":
    #         allProducts = allProducts.order_by('-productattribute__price')
    #
    #     else:
    #         pass
    t = render_to_string('ajax/product_list.html', {'data': allProducts})
    return JsonResponse({
        'data': t,
    })

class ProductListView(ListView):
    template_name = 'site_product/product_list.html'
    model = Product
    context_object_name = 'products'

    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        category_name = self.kwargs.get('category')
        subcategory_name = self.kwargs.get('subcategory')
        max_price = ProductAttribute.objects.aggregate(Max('final_price'))
        context['maxprice'] = max_price

        if category_name is not None:
            cat = ProductCategory.objects.filter(url_title__iexact=category_name).first()
            context['types'] = ProductType.objects.filter(
                subcategory__category__url_title__iexact=category_name).distinct()
            context['subcats'] = ProductSubCategory.objects.filter(category__url_title__exact=category_name).all()

            if cat is not None:
                context['currentcat'] = cat
            else:
                raise Http404
        if subcategory_name is not None:
            subcat = ProductSubCategory.objects.filter(url_title__iexact=subcategory_name).first()
            context['types'] = ProductType.objects.filter(subcategory__url_title__iexact=subcategory_name).distinct()

            if subcat is not None:
                context['currentsubcat'] = subcat
            else:
                raise Http404


        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset().order_by('-create_date', '-stock')

        category_name = self.kwargs.get('category')
        subcategory_name = self.kwargs.get('subcategory')

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        if subcategory_name is not None:
            query = query.filter(subcategory__url_title__iexact=subcategory_name)


        return query


class ProductDetailView(DetailView):
    template_name = 'site_product/product_detail.html'
    model = Product


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object


        product: Product = kwargs.get('object')



        context['form'] = AddProductComment()

        context['comments'] = ProductComment.objects.filter(product_id=product.id,
                                                            accept_by_admin=True).prefetch_related(
            'product__productcomment_set').order_by('-create_date')

        context['commentscount'] = ProductComment.objects.all().filter(product_id=product.id,
                                                                       accept_by_admin=True).prefetch_related(
            'productcomment_set').count()

        context['related_products'] = Product.objects.filter(type_id=loaded_product.type_id).exclude(
            pk=loaded_product.id).all()[:10]

        weights = ProductAttribute.objects.filter(product_id=product.id, is_quantity=True).values('weight_id',
                                                                                                  'weight__title',
                                                                                                  'price',
                                                                                                  'final_price',
                                                                                                  'special_price',
                                                                                                  'special_price_percent').distinct()

        context['weights'] = weights

        if self.request.user.is_authenticated:
            new_visit_product_exist = UserRecentVisitedProduct.objects.filter(product_id=product.id,
                                                                              user_id=self.request.user.id).exists()
            if not new_visit_product_exist:
                visited_products_count = UserRecentVisitedProduct.objects.filter(user_id=self.request.user.id).count()
                if visited_products_count > 10:
                    UserRecentVisitedProduct.objects.filter(user_id=self.request.user.id).order_by('pk')[0].delete()
                new_visit_product = UserRecentVisitedProduct(product_id=product.id, user_id=self.request.user.id)
                new_visit_product.save()

        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context


class SearchProductView(ListView):
    template_name = 'site_product/product_list.html'
    context_object_name = 'products'

    paginate_by = 20

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')
        if query is not None:
            return Product.objects.search(query)

        return Product.objects.filter(is_active=True,quantity=True).order_by('-quantity')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchProductView, self).get_context_data()
        category_name = self.kwargs.get('category')
        subcategory_name = self.kwargs.get('subcategory')
        type_name = self.kwargs.get('type')
        max_price = ProductAttribute.objects.aggregate(Max('price'))

        context['maxprice'] = max_price
        context['issearched'] = True

        if category_name is not None:
            cat = ProductCategory.objects.filter(url_title__iexact=category_name).first()
            context['types'] = ProductType.objects.filter(
                subcategory__category__url_title__iexact=category_name).distinct()

            context['subcats'] = ProductSubCategory.objects.filter(category__url_title__exact=category_name).all()

            if cat is not None:
                context['currentcat'] = cat
            else:
                raise Http404
        if subcategory_name is not None:
            subcat = ProductSubCategory.objects.filter(url_title__iexact=subcategory_name).first()
            context['types'] = ProductType.objects.filter(subcategory__url_title__iexact=subcategory_name).distinct()

            if subcat is not None:
                context['currentsubcat'] = subcat
            else:
                raise Http404

        return context


@throttle(zone='comments_delay')
@login_required
def add_product_comment(request):
    product_id = request.GET.get('product_id')

    product_comment = request.GET.get('product_comment')
    if len(product_comment) <= 10:
        return JsonResponse({
            'status': 'error',
            'icon': 'error',
            'title': 'متن نظر باید بالای 10 کاراکتر باشد',
        })
    comment_score = request.GET.get('comment_score')
    comment_suggest = request.GET.get('comment_suggest')

    new_comment = ProductComment(product_id=product_id, user_id=request.user.id, comment=product_comment,
                                 score=comment_score, suggest=comment_suggest)

    new_comment.save()
    return JsonResponse({
        'status': 'success',
        'title': 'نظر شما با موفقیت ثبت و در انتظار تایید میباشد',
    })
