from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Request, Comment
from .forms import RequestCreateForm, CommentCreateForm, StatusUpdateForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone


class RequestList(ListView):
    model = Request
    template_name = 'helpdesc/index.html'
    paginate_by = 100

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({
            'request_create_form': RequestCreateForm
        })
        return context


class RequestCreate(LoginRequiredMixin, CreateView):
    model = Request
    success_url = '/'
    form_class = RequestCreateForm
    template_name = 'helpdesc/request_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class RequestUpdate(LoginRequiredMixin, UpdateView):
    model = Request
    success_url = '/'
    form_class = RequestCreateForm
    template_name = 'helpdesc/request_update.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        comments = self.object.comment_set.all()
        context.update({
            'comments': comments,
            'comment_create_form': CommentCreateForm,
            'status_update_form': StatusUpdateForm
        })
        return context


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    http_method_names = ['post']
    success_url = '/'
    form_class = CommentCreateForm
    template_name = 'helpdesc/comment_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.request = Request.objects.get(pk=self.request.POST.get("request"))
        self.object.save()
        return super().form_valid(form)


class StatusUpdate(LoginRequiredMixin, UpdateView):
    model = Request
    success_url = '/'
    form_class = StatusUpdateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.date_last_update = timezone.now()
        self.object.save()
        return super().form_valid(form)
