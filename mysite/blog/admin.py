from django.contrib import admin
from .models import Blog_Type,Blog

@admin.register(Blog_Type)
class Blog_TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'blog_type','author','created_time','last_updated_time','get_read_num')
