from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.list import ListView
from throttle.decorators import throttle

from site_setting.models import BlogBanners, SiteSetting
# from site_setting.models import SiteBanner,BlogBanners
from utils.http_service import get_client_ip
from .models import Blog, BlogComment, BlogVisit


class SearchBlogView(ListView):
    template_name = 'site_blog/blog_list.html'
    context_object_name = 'blog'

    paginate_by = 20
    def get_queryset(self):
        request = self.request
        query = request.GET.get('b')
        if query is not None:
            return Blog.objects.search(query)

        return Blog.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super(SearchBlogView, self).get_context_data()

        most_visit_blogs = Blog.objects.filter(is_active=True).annotate(
            visit_count=Count('blogvisit')).order_by('-visit_count')[:1].first()

        # context['blogbanner'] = BlogBanners.objects.all()

        context['most_visited_blog'] = most_visit_blogs
        return context

class BlogListView(ListView):
    model = Blog
    paginate_by = 10
    template_name = 'site_blog/blog_list.html'

    def get_queryset(self):
        query = super(BlogListView, self).get_queryset()
        query = query.filter(is_active=True)
        return query
    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data()
        setting = SiteSetting.objects.filter(is_main=True).first()

        context['setting'] = setting
        most_visit_blogs = Blog.objects.filter(is_active=True).annotate(
            visit_count=Count('blogvisit')).order_by('-visit_count')[:5]

        context['most_visited_blog'] = most_visit_blogs
        context['blogbanner'] = BlogBanners.objects.all()



        return context

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'site_blog/blog_detail.html'

    def get_queryset(self):
        query = super(BlogDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data()
        loaded_blog = self.object
        blog: Blog = kwargs.get('object')

        context['comments'] = BlogComment.objects.filter(blog_id=blog.id, accept_by_admin=True,
                                                         parent=None).prefetch_related('blogcomment_set').order_by('-create_date')
        context['commentscount'] = BlogComment.objects.all().filter(blog_id=blog.id, accept_by_admin=True).prefetch_related('blogcomment_set').count()

        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = BlogVisit.objects.filter(ip__iexact=user_ip, blog_id=loaded_blog.id).exists()
        if not has_been_visited:
            new_visit = BlogVisit(ip=user_ip, user_id=user_id, blog_id=loaded_blog.id)
            new_visit.save()

        return context

@throttle(zone='comments_delay')
@login_required
def add_blog_comment(request):
    blog_id = request.GET.get('blog_id')
    parent_id = request.GET.get('parent_id')
    blog_comment = request.GET.get('blog_comment')

    if len(blog_comment) <= 10:
        return JsonResponse({
            'status': 'error',
            'icon': 'error',
            'title': 'متن نظر باید بالای 10 کاراکتر باشد',
        })

    new_comment = BlogComment(parent_id=parent_id,blog_id=blog_id,comment=blog_comment,user_id=request.user.id)
    new_comment.save()
    return JsonResponse({
        'status': 'success',
        'title': 'نظر شما با موفقیت ثبت و در انتظار تایید میباشد',
    })
def BlogSidebarComponent(request):
    most_visit_blogs = Blog.objects.filter(is_active=True).annotate(
        visit_count=Count('blogvisit')).order_by('-visit_count')[:5]
    # banners = SiteBanner.objects.filter(is_active=True,
    #                                                position__iexact=SiteBanner.SiteBannerPositions.blog_list)

    context = {
        'most_visit_blogs': most_visit_blogs,
        # 'banners': banners,
    }
    return render(request, 'site_blog/component/blog_sidebar.html', context)
