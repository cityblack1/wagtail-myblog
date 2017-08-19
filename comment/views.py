from django.shortcuts import redirect, render
from blog.models import BlogPage

from .forms import CommentForm, ContactForm

# Create your views here.


def comment_view(request, slug):
    try:
        blog = BlogPage.objects.get(slug=slug)
        url = blog.get_url()
        if request.method == 'POST':
            comment_forms = CommentForm(request.POST)
            if comment_forms.is_valid():
                comment = comment_forms.save(commit=False)
                comment.blog = blog
                comment.save()
                return redirect(url)
            else:
                render(request, 'blog/blog_page.html', context={'comment_forms': comment_forms})
        return redirect(url)
    except:
        return redirect('/')


STAT = 0


def contact_view(request):
    global STAT
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            STAT = 1
            return redirect(request.path)
        else:
            return render(request, 'blog/contact_page.html', {'contact_form': contact_form, 'message': None})

    if request.method == 'GET':
        if STAT:
            STAT = 0
            return render(request, 'blog/contact_page.html', {'message': '1'})
        return render(request, 'blog/contact_page.html', {'message': None})

    else:
        return redirect('/')

