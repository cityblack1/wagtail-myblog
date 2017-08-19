from django.db import models

# Create your models here.


class Comment(models.Model):
    name = models.CharField(max_length=20, verbose_name='名字')
    email = models.EmailField(max_length=100, verbose_name='邮箱')
    url = models.CharField(max_length=100, verbose_name='网址', blank=True)
    comment = models.TextField(verbose_name='评论')
    blog = models.ForeignKey('blog.BlogPage', on_delete = models.CASCADE, verbose_name='博文')
    date = models.DateTimeField(auto_now_add=True, verbose_name='发布日期', null=True, blank=True)

    class Meta:
        ordering = ['-date']


class Contact(models.Model):
    name = models.CharField(max_length=20, verbose_name='名字')
    email = models.EmailField(max_length=100, verbose_name='邮箱')
    subject = models.CharField(max_length=20, blank=True, verbose_name='专业')
    message = models.TextField(verbose_name='消息')
    date = models.DateTimeField(auto_now_add=True, verbose_name='发布日期', null=True, blank=True)

    class Meta:
        ordering = ['-date']