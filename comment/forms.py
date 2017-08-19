from django.forms.models import ModelForm

from .models import Comment, Contact


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'url', 'email', 'comment']


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'message', 'email', 'subject']
