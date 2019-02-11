from django.shortcuts import render_to_response,get_object_or_404
from .models import Blog,Blog_Type
from django.core.paginator import Paginator
from read_statics.utils import read_once,get_seven_nums_data,get_today_hot_data,get_yesterday_hot_data
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Sum
import datetime

def date_count():
    blog_dates = Blog.objects.dates('created_time','month',order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    return blog_dates_dict

def get_week_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=date) \
                        .values('id','title') \
                        .annotate(read_num_sum=Sum('read_details__read_num')) \
                        .order_by('-read_num_sum')
    return blogs[:5]

def get_month_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=30)
    blogs = Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=date) \
                        .values('id','title') \
                        .annotate(read_num_sum=Sum('read_details__read_num')) \
                        .order_by('-read_num_sum')
    return blogs[:5]

def test(request):
    return render_to_response('text.html')
def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_nums_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    #获取缓存
    hot_blogs_for_week_days = cache.get('hot_blogs_for_week_days')
    if hot_blogs_for_week_days is None:
        hot_blogs_for_week_days = get_week_hot_blogs()
        cache.set('hot_blogs_for_week_days',hot_blogs_for_week_days,3600)
        print('calc')
    else:
        print('use cache')

    hot_blogs_for_month_days = cache.get('hot_blogs_for_month_days')
    if hot_blogs_for_month_days is None:
        hot_blogs_for_month_days = get_month_hot_blogs()
        cache.set('hot_blogs_for_month_days',hot_blogs_for_month_days,3600)
        print('calc')
    else:
        print('use cache')
    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = today_hot_data
    context['yesterday_hot_data'] = yesterday_hot_data
    context['week_hot_data'] = get_week_hot_blogs()
    context['month_hot_data'] = get_month_hot_blogs()
    return render_to_response('home.html', context)

def blog_list(request):
    blogs = Blog.objects.all()
    blog_type = Blog_Type.objects.all()
    page_num = request.GET.get('page',1)#获取页码参数
    paginator = Paginator(blogs,15)#完成分页，实例paginator
    page = paginator.page(page_num)#实例page
    current_page = int(page_num)
    last_page = paginator.page_range[-1]
    if current_page <= 3:
        page_range = [1,2,3,4,5]
    else:
        if paginator.page_range[-3] <= current_page:
            page_range = [paginator.page_range[-5], paginator.page_range[-4], paginator.page_range[-3],
                          paginator.page_range[-2], paginator.page_range[-1]]
        else:
            page_range = [current_page - 2, current_page - 1, current_page, current_page + 1, current_page + 2]
    context = {}
    context['paginator'] = paginator
    context['page'] = page
    context['page_range'] = page_range
    context['last_page'] = last_page
    context['blogs'] = page.object_list
    context['blog_type'] = blog_type
    context['blog_dates'] = date_count()
    return render_to_response('blog_list.html',context)

def blogs_with_type(request,blog_type_pk):
    blog_types = Blog_Type.objects.all()
    blog_type = get_object_or_404(Blog_Type,pk=blog_type_pk)
    blogs_of_type = Blog.objects.filter(blog_type=blog_type)
    page_num = request.GET.get('page', 1)  # 获取页码参数
    paginator = Paginator(blogs_of_type, 5)  # 完成分页，实例paginator
    page = paginator.page(page_num)  # 实例page
    current_page = int(page_num)
    last_page = paginator.page_range[-1]
    if current_page <= 3:
        page_range = [1,2,3,4,5]
    else:
        if paginator.page_range[-3] <= current_page:
            page_range = [paginator.page_range[-5], paginator.page_range[-4], paginator.page_range[-3],
                          paginator.page_range[-2], paginator.page_range[-1]]
        else:
            page_range = [current_page - 2, current_page - 1, current_page, current_page + 1, current_page + 2]
    context = {}
    context['paginator'] = paginator
    context['page'] = page
    context['page_range'] = page_range
    context['last_page'] = last_page
    context['blogs'] = page.object_list
    context['blog_types'] = blog_types
    context['blog_type'] = blog_type
    context['blog_dates'] = date_count()
    return render_to_response('blog_with_type.html',context)

def blogs_with_date(request,year,month):
    blog_types = Blog_Type.objects.all()
    blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)
    page_num = request.GET.get('page', 1)  # 获取页码参数
    paginator = Paginator(blogs, 5)  # 完成分页，实例paginator
    page = paginator.page(page_num)  # 实例page
    current_page = int(page_num)
    last_page = paginator.page_range[-1]
    if current_page <= 3:
        page_range = [1,2,3,4,5]
    else:
        if paginator.page_range[-3] <= current_page:
            page_range = [paginator.page_range[-5], paginator.page_range[-4], paginator.page_range[-3],
                          paginator.page_range[-2], paginator.page_range[-1]]
        else:
            page_range = [current_page - 2, current_page - 1, current_page, current_page + 1, current_page + 2]
    context = {}
    context['paginator'] = paginator
    context['page'] = page
    context['page_range'] = page_range
    context['last_page'] = last_page
    context['blogs'] = page.object_list
    context['blog_types'] = blog_types
    context['blog_dates'] = date_count()
    return render_to_response('blog_with_date.html',context)

def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_once(request,blog)
    context = {}
    context['blog'] = get_object_or_404(Blog,pk=blog_pk)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    response = render_to_response('blog_detail.html',context)
    response.set_cookie(read_cookie_key,'true')
    return response

