from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape, mark_safe

from wagtail.wagtailcore.models import Page


import markdown


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def escape_space(value):
    return value.ljust(10).replace(' ', '&nbsp;')


@register.filter(name='markdown_code')
def markdown_code(value):
    value.value = markdown.markdown(value.value,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                    ])
    return None

query_dict = {
    '首页': 'home_page',
    '博客': 'blog',
    '联系': 'contact',
    '关于': 'about',
}

@register.simple_tag(takes_context=True)
def focus_text(context, value):
    current_name = query_dict[value]
    template_name = context.template_name.split('/')[-1]
    if current_name in template_name:
        return mark_safe('<font color="#d2691e">{}</font>'.format(value))
    return value


@register.inclusion_tag('blog/includes/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True).filter(depth__gt=2)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }