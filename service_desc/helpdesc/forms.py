from django.forms import ModelForm, HiddenInput
from .models import Request, Comment


class RequestCreateForm(ModelForm):
    class Meta:
        model = Request
        fields = ('name', 'info', 'priority')


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class StatusUpdateForm(ModelForm):
    class Meta:
        model = Request
        fields = ('status',)
