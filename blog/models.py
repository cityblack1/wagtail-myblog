from django.db import models

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailsearch import index
from wagtail.wagtailadmin.edit_handlers import *
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.tags import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase

from comment.models import Comment
from .stream_field import DemoStreamBlock
# """
# 学习心得：

# wagtail 最大的特点就是将视图层（Ｖ），模型层（Ｍ）和映射管理（Ｃ）用一个Page类集成在了一起，
# 使得我们在ＭＶＣ开发模式中只用关注Page类的构造，而无需去定义每个层面具体的东西
# 同时它拥有人性化的内容管理系统，更加照顾编辑人员而不是开发人员
# wagtail为开发者提供了丰富的api，
# 本着不重复开发轮子的宗旨，尽量使用wagtail自带的api，以及其他插件
# 当wagtail不能满足需求或者学习成本过高的时候，也可以用django自带的功能完成开发需求
# 比如自定义标签和过滤器，自定义include模板片段等等，让django模板语言更加健壮，代码逻辑更加简练
#
# """

# 一个包含了若干字段的抽象类，用于一些model继承
class LinkFields(models.Model):
    link_external = models.URLField('拓展链接', blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        verbose_name='相关页面'
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+',
        verbose_name='相关文件'
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document')
    ]

    class Meta:
        abstract = True


# 在抽象类LinkFields的基础上对一些字段进行拓展，并重新定义panels
class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text='link title')

    # 使用MultiFieldPanel定义混合字段
    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "link")
    ]

    # 仍然定义为抽象类，让后面的model去继承
    class Meta:
        abstract = True


# Blog的索引页面


# 定义一个Orderable，让后面的InlineField引用
class BlogIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('blog.BlogIndexPage', related_name='related_links')


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro')
    ]

    @property
    def get_blogs(self):
        # 得到这个索引页面下的全部Blog子页面
        blogs = BlogPage.objects.live().descendant_of(self)
        blogs = blogs.order_by('-date')
        return blogs

    @property
    def get_all_blogs(self):
        return BlogPage.objects.all()

    def get_context(self, request, *args, **kwargs):
        # 如果是通过标签进来的，将显示符合条件的标签
        tag = request.GET.get('tag', '')
        date = request.GET.get('date', '')
        all = request.GET.get('all', '')
        query = request.GET.get('query', '')

        if tag:
            blogs = self.get_all_blogs.filter(tags__name=tag)

        elif query:
            blogs = self.get_all_blogs.filter(title__icontains=query)

        elif date:
            year, month = date.split('-')
            blogs = self.get_all_blogs.filter(date__month=month).filter(date__year=year)

        elif all:
            blogs = self.get_all_blogs

        else:
            blogs = self.get_blogs

        # override context 变量
        context = super(BlogIndexPage, self).get_context(request)
        context['blogs'] = blogs
        return context

BlogIndexPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('intro', classname='full'),
    InlinePanel('related_links', label='Related links')
]

# BlogIndexPage.promote_panels = Page.promote_panels


# blog 页面


# 封面轮播图, 这个功能只对特定页面有效
class PageCoverItem(LinkFields):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='相关图片'
    )

    panels = [
        ImageChooserPanel('image'),
        MultiFieldPanel(LinkFields.panels, "link")
    ]


class BlogPagePageCoverItem(Orderable, PageCoverItem):
    page = ParentalKey('blog.BlogPage', related_name='page_cover_item')


# 相关链接
class BlogPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('blog.BlogPage', related_name='related_links')


# django插件taggit的集成
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('blog.BlogPage', related_name='taggit_items')


class BlogPage(Page):
    body = StreamField(DemoStreamBlock)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    date = models.DateField('Post Date')
    read_times = models.IntegerField(default=0, verbose_name='阅读次数', blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+++'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body')
    ]

    def parent(self):
        parent = self.get_parent().specific
        return parent

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
        date_category = [blogs.filter(date__month=month).filter(date__year=year) for year, month in years_months if
                         blogs.filter(date__month=month).filter(date__year=year)]
        date_category = sorted(date_category, key=lambda x: x[0].date, reverse=True)
        return date_category

    def get_tags(self):
        from functools import reduce
        blogs = self.get_blogs
        all_tags = [blog.tags.all().results for blog in blogs if blog.tags.all()]
        tags_list = list(set(tag.name for tag in reduce(lambda x, y: x + y, all_tags)))
        return tags_list

    def get_comments(self):
        comments = Comment.objects.filter(blog__slug=self.slug)
        return comments

    def get_context(self, request, *args, **kwargs):
        self.read_times += 1
        self.save()
        full_width = request.GET.get('fullwidth', '')
        context = super(BlogPage, self).get_context(request)
        context['blogs'] = self.get_blogs
        context['blog_index'] = self.get_blog_index()
        context['date_categories'] = self.get_date_categories()
        context['tags_list'] = self.get_tags()
        context['fullwidth'] = full_width
        context['comments'] = self.get_comments()
        return context


BlogPage.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('date'),
    StreamFieldPanel('body'),
    InlinePanel('page_cover_item', label='轮播图'),
    InlinePanel('related_links', label="相关网页"),
]


BlogPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
    FieldPanel('tags')
]


class AboutPage(Page):
    body = StreamField(DemoStreamBlock())

AboutPage.content_panels = [
    FieldPanel('title', classname="full title"),
    StreamFieldPanel('body'),
]

AboutPage.promote_panels = Page.promote_panels


class ContactPage(Page):
    pass

ContactPage.content_panels = Page.content_panels
ContactPage.promote_panels = Page.promote_panels