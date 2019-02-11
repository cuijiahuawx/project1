from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from read_statics.models import ReadDetail
from read_statics.models import ReadNumExpand

class Blog_Type(models.Model):
    type_name = models.CharField(max_length=15)

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name

    def blog_count(self):
        return self.blog_set.count()

class Blog(models.Model,ReadNumExpand):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(Blog_Type,on_delete=models.DO_NOTHING)
    content = RichTextUploadingField('正文', config_name='my_ckeditor')
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =  ['-created_time']
        verbose_name = '博客'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '<Blog: %s>'%self.title

