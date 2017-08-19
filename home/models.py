from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import *
from blog.models import BlogPage, BlogIndexPage


class HomePage(Page):
    intro = RichTextField(default='', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('title', classname='full title'),
        RichTextFieldPanel('intro'),
    ]

    @property
    def get_blogs(self):
        blogs = BlogPage.objects.order_by('-date')
        return blogs

    def get_blog_index(self):
        blog_index = BlogIndexPage.objects.order_by('-first_published_at')
        return blog_index

    def get_date_categories(self):
        blogs = self.get_blogs
        years = set(blog.date.year for blog in blogs)
        months = set(blog.date.month for blog in blogs)
        years_months = [(year, month) for year in years for month in months]
        date_category = [blogs.filter(date__month=month).filter(date__year=year) for year, month in years_months if blogs.filter(date__month=month).filter(date__year=year)]
        date_category = sorted(date_category, key=lambda x:x[0].date, reverse=True)
        return date_category

    def get_tags(self):
        from functools import reduce
        blogs = self.get_blogs
        all_tags = [blog.tags.all().results for blog in blogs if blog.tags.all()]
        tags_list = list(set(tag.name for tag in reduce(lambda x, y: x + y, all_tags)))
        return tags_list


    def get_context(self, request, *args, **kwargs):
        context = super(HomePage, self).get_context(request)
        context['blogs'] = self.get_blogs
        context['blog_index'] = self.get_blog_index()
        context['date_categories'] = self.get_date_categories()
        context['tags_list'] = self.get_tags()
        return context
